from ._types import List
from ..models.model import query
from datetime import datetime
from ..utils import generate_expire


def get_deny() -> List:
    return query("SELECT ip FROM DENY", row_factory=lambda cursor, row: row[0])


def create_deny(ips: List) -> List:
    query(
        "INSERT INTO banned (ip, expire) VALUES (?, ?)",
        [(ip, datetime(year=9999, month=12, day=31)) for ip in ips],
        mode="many",
    )
    query("INSERT INTO deny (ip) VALUES (?)", (ips,), mode="many")
    return []


def delete_deny(ips: List) -> List:
    query(
        """
        UPDATE banned 
        SET expire = :now 
        WHERE ip=:ip 
        AND expire > :now
        """,
        [{"ip": ip, "now": generate_expire(0)} for ip in ips],
        mode="many",
    )
    query("delete from deny where ip=?", (ips,), mode="many")
    return []
