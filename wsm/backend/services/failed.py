from backend import query
from ._types import datetime, Cursor


def create_failed(ip: str, username: str, time: datetime) -> Cursor:
    return query(
        "INSERT INTO failed (ip, username, time) VALUES (?, ?, ?)", (ip, username, time)
    )


def read_failed() -> Cursor:
    return query("SELECT * FROM failed")
