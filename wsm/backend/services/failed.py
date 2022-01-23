from ._types import datetime, List
from ..models.model import query


def create_failed(ip: str, username: str, time: datetime) -> List:
    return query(
        "INSERT INTO failed (ip, username, time) VALUES (?, ?, ?)", (ip, username, time)
    )


def get_failed() -> List:
    return query("SELECT * FROM failed")
