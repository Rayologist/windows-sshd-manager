from ._types import datetime, List
from ..models.model import query


def create_banned(ip: str, expire: datetime) -> List:
    return query("INSERT INTO banned (ip, expire) VALUES (?, ?)", (ip, expire))
