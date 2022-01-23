from backend import query
from ._types import datetime, List


def create_failed(ip: str, username: str, time: datetime) -> List:
    return query(
        "INSERT INTO failed (ip, username, time) VALUES (?, ?, ?)", (ip, username, time)
    )


def read_failed() -> List:
    return query("SELECT * FROM failed")
