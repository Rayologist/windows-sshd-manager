from backend import query
from ._types import datetime, List


def create_success(ip: str, username: str, time: datetime) -> List:
    return query(
        "INSERT INTO success (ip, username, time) VALUES (?, ?, ?)",
        (ip, username, time),
    )
