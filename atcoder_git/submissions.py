from typing import List, NamedTuple, Optional

import requests

from atcoder_git.util import limit_interval


__all__ = [
    "Submission",
    "get_submissions",
]


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


API_BASE = "https://kenkoooo.com/atcoder"


@limit_interval(1.0)
def get_submissions(user: str) -> List[Submission]:
    resp = requests.get(f"{API_BASE}/atcoder-api/results", {"user": user})
    subs = resp.json()
    return [Submission(**sub) for sub in subs]
