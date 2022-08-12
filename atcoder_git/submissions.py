from typing import List, NamedTuple, Optional

import requests

from atcoder_git.util import limit_interval


__all__ = [
    "Submission",
    "get_submissions",
]

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


# https://github.com/kenkoooo/AtCoderProblems/blob/master/doc/api.md
API_BASE = "https://kenkoooo.com/atcoder"

atcoder_problems_api_limit = limit_interval(1.0)


@atcoder_problems_api_limit
def get_submissions(user: str) -> List[Submission]:
    resp = requests.get(f"{API_BASE}/atcoder-api/results", {"user": user})
    subs = resp.json()
    return [Submission(**sub) for sub in subs]


@atcoder_problems_api_limit
def get_problems() -> List[Problem]:
    resp = requests.get(f"{API_BASE}/resources/problems.json")
    probs = resp.json()
    return [Problem(**prob) for prob in probs]


@atcoder_problems_api_limit
def get_contest_problems() -> List[ContestProblem]:
    resp = requests.get(f"{API_BASE}/resources/contest-problems.json")
    cprobs = resp.json()
    return [ContestProblem(**cprob) for cprob in cprobs]
