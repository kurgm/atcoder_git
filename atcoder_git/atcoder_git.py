#!/usr/bin/env python3

import argparse
import os
from typing import Dict, List, Optional, Tuple

import onlinejudge.service.atcoder as atcoder

import atcoder_git.repository
import atcoder_git.submissions
from atcoder_git.util import cache_result, limit_interval


@limit_interval(3.0)
def get_submission_detail(
        submission: atcoder_git.submissions.Submission
) -> atcoder.AtCoderSubmissionDetailedData:

    sub = atcoder.AtCoderSubmission(
        contest_id=submission.contest_id,
        submission_id=submission.id)

    return sub.download_data()


@cache_result
def contest_alphabet_dict() -> Dict[str, Tuple[str, str]]:
    result = {}

    for problem in atcoder_git.submissions.get_problems():
        alphabet, _title = problem.title.split(". ", 1)
        result[problem.id] = (problem.contest_id, alphabet)

    return result


def lookup_contest_alphabet(problem_id: str) -> Tuple[str, str]:
    return contest_alphabet_dict()[problem_id]


LANGUAGE_EXTENSION: Dict[str, str] = {
    "Ada": ".adb",
    "Awk": ".awk",
    "Bash": ".sh",
    "Brainfuck": ".bf",
    "C": ".c",
    "C#": ".cs",
    "C++": ".cpp",
    "COBOL - Fixed": ".cob",
    "COBOL - Free": ".cob",
    "Ceylon": ".ceylon",
    "Clojure": ".clj",
    "Common Lisp": ".lisp",
    "Crystal": ".cr",
    "Cython": ".pyx",
    "D": ".d",
    "Dart": ".dart",
    "Dash": ".sh",
    "Elixir": ".ex",
    "Erlang": ".erl",
    "F#": ".fs",
    "Forth": ".fs",
    "Fortran": ".f08",
    "Go": ".go",
    "Haskell": ".hs",
    "Haxe": ".hx",
    "IOI-Style C++": ".cpp",
    "Java": ".java",
    "JavaScript": ".js",
    "Julia": ".jl",
    "Kotlin": ".kt",
    "Lua": ".lua",
    "LuaJIT": ".lua",
    "MoonScript": ".moon",
    "Nim": ".nim",
    "OCaml": ".ml",
    "Objective-C": ".m",
    "Octave": ".m",
    "PHP": ".php",
    "Pascal": ".pas",
    "Perl": ".pl",
    "Perl6": ".p6",
    "Prolog": ".pl",
    "PyPy": ".py",
    "Python": ".py",
    "Racket": ".rkt",
    "Raku": ".p6",
    "Ruby": ".rb",
    "Rust": ".rs",
    "Scala": ".scala",
    "Scheme": ".scm",
    "Sed": ".sed",
    "Standard ML": ".sml",
    "Swift": ".swift",
    "Text": ".txt",
    "TypeScript": ".ts",
    "Unlambda": ".unl",
    "Vim": ".vim",
    "Visual Basic": ".vb",
    "Zsh": ".sh",
    "bc": ".bc",
    "dc": ".dc",
}


def get_extension_from_language(language: str) -> str:
    short_language_name = language.split("(", 1)[0].strip()
    if short_language_name != "Perl6":
        short_language_name = short_language_name.rstrip("0123456789")

    return LANGUAGE_EXTENSION[short_language_name]


def get_file_path(submission: atcoder_git.submissions.Submission) -> str:
    contest, alphabet = lookup_contest_alphabet(submission.problem_id)

    ext = get_extension_from_language(submission.language)
    return os.path.join(
        contest,
        alphabet,
        f"Main{ext}"
    )


def in_repository(
        submission: atcoder_git.submissions.Submission,
        repository: atcoder_git.repository.Repository
) -> bool:

    filepath = get_file_path(submission)
    datetime = submission.epoch_second
    return repository.has_update(filepath, datetime)


def add_to_repository(
        submission: atcoder_git.submissions.Submission,
        repository: atcoder_git.repository.Repository
) -> None:

    filepath = get_file_path(submission)
    datetime = submission.epoch_second
    detail = get_submission_detail(submission)
    content = detail.source_code

    message = f"Update {filepath}" + "\n\n" + detail.submission.get_url()

    repository.update_file(filepath, datetime, content, message)


def build_repository(
        repository: atcoder_git.repository.Repository,
        username: str
) -> None:
    submissions = atcoder_git.submissions.get_submissions(username)
    submissions.sort(key=lambda submission: submission.epoch_second)
    for submission in submissions:
        if submission.result != "AC":
            continue
        if not in_repository(submission, repository):
            add_to_repository(submission, repository)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--git-user", nargs=2, metavar=("NAME", "EMAIL"))
    parser.add_argument("--git-timezone", default="+0900")
    parser.add_argument("git_directory")
    parser.add_argument("atcoder_user_name")

    args = parser.parse_args(argv)

    user: Optional[atcoder_git.repository.GitUser] = None
    if args.git_user is not None:
        user = atcoder_git.repository.GitUser(
            name=args.git_user[0],
            email=args.git_user[1],
        )

    repository = atcoder_git.repository.GitRepository(
        path=args.git_directory,
        user=user,
        timezone=args.git_timezone,
    )
    build_repository(repository, args.atcoder_user_name)


if __name__ == "__main__":
    main()
