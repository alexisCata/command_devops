#!/usr/bin/env python3
import datetime
import json
import logging
import pprint
import sys

from clinner.command import command, Type as CommandType
from clinner.run import Main

from builder.builder import Builder
from builder.email import Email
from builder.git_repository import GitRepository
from builder.utils import bool_input

logger = logging.getLogger('cli')


@command(command_type=CommandType.PYTHON,
         args=((('--config',), {'help': 'Config file', 'default': 'config.json'}),),
         parser_opts={'help': 'Run builder'})
def build(*args, **kwargs):
    with open(kwargs['config']) as f:
        config = json.load(f)

    print('This is your current config:\n{}'.format(pprint.pformat(config, indent=2, width=120)))
    if bool_input('Do you want to continue?'):

        last_execution = datetime.datetime.strptime(config["last_execution"], "%Y-%m-%d %H:%M:%S.%f") \
            if config["last_execution"] else datetime.datetime(1900, 1, 1)

        builder = Builder(config["git"]["repo_path"], config["target"]["target_path"])

        origin_repo = GitRepository(config["git"]["repo_path"], config["git"]["git_repo"])
        target_repo = GitRepository(config["target"]["target_path"],
                                    config["target"]["git_target"].format(config["git"]["git_user"],
                                                                          config["git"]["git_pass"]))

        if builder.build(config["target"]["build_file"]):

            builder.handle_built(config["target"]["files"], origin_repo, target_repo)

            config["last_execution"] = str(datetime.datetime.now())

            with open(kwargs['config'], "w") as f:
                json.dump(config, f)
                print("Success")
        else:
            handle_error(origin_repo, last_execution, config, builder.stdout, builder.stderr)


def handle_error(origin_repo, last_execution, config, stdout, stderr):
    log_to_send = origin_repo.changelog_from(last_execution)

    email = Email(config["email"]["smtp_server"],
                  config["email"]["smtp_port"],
                  config["email"]["username"],
                  config["email"]["password"], )

    email.send(config["email"]["email_from"],
               config["email"]["email_to"],
               config["email"]["subject"],
               email.body_from_builder_output(log_to_send, stdout, stderr))

    print("==ERROR==")
    print(stderr)
    print("Email sent")


if __name__ == '__main__':
    main = Main()
    sys.exit(main.run())
