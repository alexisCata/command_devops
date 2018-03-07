import os
import subprocess
from shutil import copyfile

__all__ = ['Builder']


class Builder:
    """
    Class to build files from one origin repo into a target repo
    """

    def __init__(self, origin, target, email):
        self.origin = origin
        self.target = target
        self._email = email
        self._stdout = None
        self._stderr = None

    def build(self, build_script):
        p = subprocess.run(build_script, cwd=self.origin.path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._stdout = p.stdout.decode("UTF-8")
        self._stderr = p.stderr.decode("UTF-8")

        return self._stderr == ""

    def push_binary(self, files):
        for bfile in files:
            copyfile(os.path.join(self.origin.path, bfile), os.path.join(self.target.path, bfile))
            self.target.repository.git.add(bfile)
        self.target.push("New binary")

    def send_email_error(self, timestamp, email_from, email_to, subject):
        log_to_send = self.origin.changelog_from(timestamp)

        self._email.send(email_from, email_to, subject,
                         self._email.body_from_builder_output(log_to_send, self._stdout, self._stderr))
