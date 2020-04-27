import os
import subprocess
from typing import NamedTuple


__all__ = [
    "Repository",
    "GitUser",
    "GitRepositoryError",
    "GitRepository",
]


class Repository:
    def update_file(
            self, filepath: str, datetime: int, content: bytes,
            message: str) -> None:
        raise NotImplementedError()


class GitUser(NamedTuple):
    name: str
    email: str


class GitRepositoryError(OSError):
    pass


class GitRepository(Repository):
    path: str
    user: GitUser
    timezone: str

    def __init__(self, path: str, user: GitUser, timezone: str) -> None:
        self.path = path
        self.user = user
        self.timezone = timezone

        self._check_inside_git()

    def _check_inside_git(self):
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=self.path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        if result.returncode != 0:
            raise GitRepositoryError("not a git repository: %s" % self.path)

    def update_file(
            self, filepath: str, datetime: int, content: bytes,
            message: str) -> None:
        actual_path = os.path.join(self.path, filepath)
        with open(actual_path, "wb") as file:
            file.write(content)

        self._add(filepath)
        self._commit(message, datetime)

    def _add(self, *pathspecs: str) -> None:
        subprocess.run(
            ["git", "add", "--", *pathspecs],
            cwd=self.path,
            check=True
        )

    def _commit(self, message: str, datetime: int) -> None:
        datetime_str = "%d %s" % (datetime, self.timezone)

        env = dict(os.environ)
        env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = self.user.name
        env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = self.user.email
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = datetime_str

        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", message],
            cwd=self.path,
            env=env,
            check=True
        )
