from ._types import datetime, List, Iterable, Tuple
from ..models.model import query, async_query
from ..utils import generate_expire


def create_banned(ip: str, expire: datetime) -> List:
    return query("INSERT INTO banned (ip, expire) VALUES (?, ?)", (ip, expire))


def create_many_banned(iterable: Iterable[Tuple[str, int]]) -> List:
    return query(
        "INSERT INTO banned (ip, expire) VALUES (?, ?) ON CONFLICT DO NOTHING",
        params=iterable,
        mode="many",
    )


async def get_banned_ips() -> List:
    return await async_query(
        "SELECT ip FROM banned WHERE expire > ?",
        (generate_expire(0),),
        row_factory=lambda cursor, row: row[0],
    )


async def get_banned_by_ip(ip):
    return await async_query(
        "SELECT * FROM banned as b WHERE ip = ?",
        (ip,),
        row_factory=lambda cursor, row: {"ip": row[0], "expire (UTC)": row[1]},
    )


async def update_expire_by_ips(ips, expire) -> List:
    return await async_query(
        """
        UPDATE banned
        SET expire = :expire
        WHERE expire > :now
        AND ip = :ip
        """,
        [{"now": generate_expire(0), "expire": expire, "ip": ip} for ip in ips],
        mode="many",
    )


def delete_expired() -> List:
    return query(
        "DELETE FROM banned WHERE expire < ? RETURNING ip",
        (generate_expire(0),),
        row_factory=lambda cursor, row: row[0],
    )
