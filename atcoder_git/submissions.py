import json
from typing import List, NamedTuple, Optional
import urllib.parse
import urllib.request


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


def get_submissions(user: str) -> List[Submission]:
    params = urllib.parse.urlencode({
        "user": user,
    })
    url = f"{API_BASE}/atcoder-api/results?{params}"
    resp = urllib.request.urlopen(url)
    return [Submission(*sub) for sub in json.load(resp)]
