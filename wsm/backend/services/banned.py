from ._types import datetime, Cursor
from backend import query


def create_banned(ip: str, expire: datetime) -> Cursor:
    return query("INSERT INTO banned (ip, expire) VALUES (?, ?)", (ip, expire))
