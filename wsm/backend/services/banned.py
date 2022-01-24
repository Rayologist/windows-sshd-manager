from ._types import datetime, List, Iterable, Tuple
from ..models.model import query
from ..utils import generate_expire


def create_banned(ip: str, expire: datetime) -> List:
    return query("INSERT INTO banned (ip, expire) VALUES (?, ?)", (ip, expire))


def create_many_banned(iterable: Iterable[Tuple[str, int]]) -> List:
    return query(
        "INSERT INTO banned (ip, expire) VALUES (?, ?)", params=iterable, mode="many"
    )


def get_banned_ips() -> List:
    return query("SELECT ip FROM banned", row_factory=lambda cursor, row: row[0])


def delete_expired() -> List:
    return query("DELETE FROM banned WHERE expire < ?", (generate_expire(0),))
