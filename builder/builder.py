import os
import subprocess
from shutil import copyfile

__all__ = ['Builder']


class Builder:
    def __init__(self, repo_path, target_path):
        self.repo_path = repo_path
        self.target_path = target_path
        self.stdout = None
        self.stderr = None

    def build(self, build_script):

        p = subprocess.run(build_script,
                           cwd=self.repo_path,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        self.stdout = p.stdout.decode("UTF-8")
        self.stderr = p.stderr.decode("UTF-8")

        return self.stderr == ""

    @staticmethod
    def handle_built(files, origin_repo, target_repo):
        for bfile in files:
            copyfile(os.path.join(origin_repo.path, bfile), os.path.join(target_repo.path, bfile))
            target_repo.repository.git.add(bfile)
        target_repo.push("New binary")

