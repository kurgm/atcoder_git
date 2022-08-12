from __future__ import annotations

from enum import Enum
from html.parser import HTMLParser
from typing import NamedTuple

import requests

import atcoder_git.submissions
from atcoder_git.util import limit_interval


class SubmissionPageHTMLParserState(Enum):
    BEFORE = 0
    INSIDE = 1
    AFTER = 2


_State = SubmissionPageHTMLParserState


class SubmissionPageHTMLParser(HTMLParser):

    _state: SubmissionPageHTMLParserState
    _submitted_code: str

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._state = _State.BEFORE
        self._submitted_code = ""

    def handle_starttag(self, tag, attrs) -> None:
        assert self._state != _State.INSIDE
        if tag == "pre" and dict(attrs).get("id") == "submission-code":
            assert self._state == _State.BEFORE
            self._state = _State.INSIDE

    def handle_endtag(self, tag) -> None:
        if self._state == _State.INSIDE:
            assert tag == "pre"
            self._state = _State.AFTER

    def handle_data(self, data: str) -> None:
        if self._state == _State.INSIDE:
            self._submitted_code += data

    def get_submitted_code(self) -> str:
        assert self._state == _State.AFTER
        return self._submitted_code


def get_submission_url(contest_id: str, submission_id: int) -> str:
    return (
        "https://atcoder.jp"
        f"/contests/{contest_id}/submissions/{submission_id}"
    )


class SubmissionDetail(NamedTuple):
    url: str
    source_code: bytes


atcoder_api_limit = limit_interval(3.0)


@atcoder_api_limit
def get_submission_detail(
    submission: atcoder_git.submissions.Submission
) -> SubmissionDetail:
    url = get_submission_url(
        contest_id=submission.contest_id,
        submission_id=submission.id)

    resp = requests.get(url)
    resp.encoding = "utf-8"
    text = resp.text

    parser = SubmissionPageHTMLParser()
    parser.feed(text)
    source_code = parser.get_submitted_code().encode("utf-8")

    return SubmissionDetail(url=url, source_code=source_code)
