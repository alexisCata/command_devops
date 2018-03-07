#!/usr/bin/env python3
import datetime
import json
import pprint
import sys

from clinner.command import command, Type as CommandType
from clinner.run import Main

from builder.builder import Builder
from builder.email import Email
from builder.git_repository import GitRepository
from builder.utils import bool_input


@command(command_type=CommandType.PYTHON,
         args=((('--config',), {'help': 'Config file', 'default': 'config.json'}),),
         parser_opts={'help': 'Run builder'})
def build(*args, **kwargs):
    """
    Command that performs thet gets a GIT repository, compiles some files and pushes them to another repository
    If build is not OK it send an email with the changelog and the error
    :param args: 
    :param kwargs: build command arguments
    :return: 
    """
    result = 0
    with open(kwargs['config']) as f:
        config = json.load(f)

    print('This is your current config:\n{}'.format(pprint.pformat(config, indent=2, width=120)))
    if bool_input('Do you want to continue?'):

        last_execution = datetime.datetime.strptime(config["last_execution"], "%Y-%m-%d %H:%M:%S.%f") \
            if config["last_execution"] else datetime.datetime(1900, 1, 1)

        email = Email(config["email"]["smtp_server"],
                      config["email"]["smtp_port"],
                      config["email"]["username"],
                      config["email"]["password"], )

        origin_repo = GitRepository(config["git_origin"]["repo_path"], config["git_origin"]["git_repo"])
        target_repo = GitRepository(config["git_target"]["target_path"],
                                    config["git_target"]["git_target"].format(config["git_origin"]["git_user"],
                                                                          config["git_origin"]["git_pass"]))

        builder = Builder(origin=origin_repo, target=target_repo, email=email)

        build_ok = builder.build(config["git_target"]["build_file"])

        if build_ok:
            builder.push_binary(config["git_target"]["files"])
            config["last_execution"] = str(datetime.datetime.now())

            with open(kwargs['config'], "w") as f:
                json.dump(config, f)
                print("Success")
        else:
            builder.send_email_error(last_execution, config["email"]["email_from"], config["email"]["email_to"],
                                     config["email"]["subject"])

        result = 0 if build_ok else -1
    return result


if __name__ == '__main__':
    sys.exit(Main().run())
