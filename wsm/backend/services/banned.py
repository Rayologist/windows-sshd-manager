from ._types import datetime, List
from backend import query


def create_banned(ip: str, expire: datetime) -> List:
    return query("INSERT INTO banned (ip, expire) VALUES (?, ?)", (ip, expire))
