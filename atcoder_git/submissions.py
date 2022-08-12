from __future__ import annotations

__all__ = [
    "Submission",
    "get_all_submissions",
]

from typing import NamedTuple, Optional

import requests

from atcoder_git.util import limit_interval

# https://github.com/kenkoooo/AtCoderProblems/blob/master/atcoder-problems-backend/sql-client/src/models.rs


class Submission(NamedTuple):
    id: int
    epoch_second: int
    problem_id: str
    contest_id: str
    user_id: str
    language: str
    point: float
    length: int
    result: str
    execution_time: Optional[int]


class Problem(NamedTuple):
    id: str
    contest_id: str
    problem_index: str
    name: str
    title: str


class ContestProblem(NamedTuple):
    contest_id: str
    problem_id: str
    problem_index: str


class Contest(NamedTuple):
    id: str
    start_epoch_second: int
    duration_second: int
    title: str
    rate_change: str


# https://github.com/kenkoooo/AtCoderProblems/blob/master/doc/api.md
API_BASE = "https://kenkoooo.com/atcoder"

atcoder_problems_api_limit = limit_interval(1.0)


@atcoder_problems_api_limit
def get_submissions_from(user: str, from_second: int) -> list[Submission]:
    resp = requests.get(f"{API_BASE}/atcoder-api/v3/user/submissions", {
        "user": user,
        "from_second": from_second,
    })
    subs = resp.json()
    return [Submission(**sub) for sub in subs]


@atcoder_problems_api_limit
def get_problems() -> list[Problem]:
    resp = requests.get(f"{API_BASE}/resources/problems.json")
    probs = resp.json()
    return [Problem(**prob) for prob in probs]


@atcoder_problems_api_limit
def get_contest_problems() -> list[ContestProblem]:
    resp = requests.get(f"{API_BASE}/resources/contest-problem.json")
    cprobs = resp.json()
    return [ContestProblem(**cprob) for cprob in cprobs]


@atcoder_problems_api_limit
def get_contests() -> list[Contest]:
    resp = requests.get(f"{API_BASE}/resources/contests.json")
    conts = resp.json()
    return [Contest(**cont) for cont in conts]


def get_all_submissions(user: str) -> list[Submission]:
    result: list[Submission] = []
    from_second = 0
    while True:
        new_submissions = get_submissions_from(user, from_second)
        if not new_submissions:
            return result
        from_second = new_submissions[-1].epoch_second + 1
        result += new_submissions
