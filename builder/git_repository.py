import datetime
import os

from git import Repo, Git, GitCommandError

__all__ = ['GitRepository']


class GitRepository:
    def __init__(self, path, url):
        self.path = path
        self._url = url
        self._prepare_folder()
        if not os.listdir(self.path):
            self.repository = Repo.clone_from(url=self._url, to_path=self.path)
        else:
            self.repository = Repo(self.path)
            self.pull()

    def _prepare_folder(self):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def pull(self):
        remote = self.repository.remote("origin")
        remote.pull()

    def add(self, file):
        self.repository.git.add(file)

    def commit(self, message):
        self.repository.git.commit("-m", message)

    def push(self, message):
        try:
            self.commit(message)
            remote = self.repository.remote("origin")
            remote.push(refspec="master:master")
        except GitCommandError as e:
            print(e)

    def changelog_from(self, from_last_execution):
        log_to_send = ""
        try:
            log = self.repository.git.log()

            lines = log.split("\n\n")
            log_lines = []
            for i, l in enumerate(lines):
                if i % 2 == 0:
                    log_lines.append(l + "\n" + lines[i + 1] + "\n")

            for line in log_lines:
                start_index = line.index("Date:   ") + 8
                end_index = line.index("\n", start_index)
                date = datetime.datetime.strptime(line[start_index:end_index], "%a %b %d %H:%M:%S %Y +%f")
                if date > from_last_execution:
                    log_to_send += "commit " + line + "\n"
        except Exception as e:
            print(e.message)

        return log_to_send
