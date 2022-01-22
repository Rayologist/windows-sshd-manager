from backend import query
from ._types import datetime, Cursor


def create_success(ip: str, username: str, time: datetime) -> Cursor:
    return query(
        "INSERT INTO success (ip, username, time) VALUES (?, ?, ?)",
        (ip, username, time),
    )
