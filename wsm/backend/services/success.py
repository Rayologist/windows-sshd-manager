from ._types import datetime, List
from ..models.model import query


def create_success(ip: str, username: str, time: datetime) -> List:
    return query(
        "INSERT INTO success (ip, username, time) VALUES (?, ?, ?)",
        (ip, username, time),
    )
