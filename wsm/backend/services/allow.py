from ._types import List
from ..models.model import query
from ..utils import generate_expire


def create_allow(ips: List) -> List:
    query(
        """
        UPDATE banned
        SET expire = :now
        WHERE expire > :now
        AND ip = :ip
        """,
        [{"now": generate_expire(0), "ip": ip} for ip in ips],
        mode="many",
    )

    return query("INSERT INTO allow (ip) VALUES (?)", (list(ips),), mode="many")


def get_allow() -> List:
    return query("SELECT ip FROM allow", row_factory=lambda cursor, row: row[0])


def delete_allow(ips: List) -> List:
    return query("DELETE FROM allow WHERE ip = ?", (ips,), mode="many")
