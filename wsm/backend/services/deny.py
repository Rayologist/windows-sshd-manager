from ._types import List
from ..models.model import query
from datetime import datetime


def create_deny(ip: str) -> List:
    query(
        "INSERT INTO banned (ip, expire) VALUES (?, ?)",
        (ip, datetime(year=9999, month=12, day=31)),
    )
    query("INSERT INTO deny (ip) VALUES (?)", (ip,))
    return []


def delete_deny(ip: str) -> List:
    query("delete from banned where ip=?", (ip,))
    query("delete from deny where ip=?", (ip,))
    return []
