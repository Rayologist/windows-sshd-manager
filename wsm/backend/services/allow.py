from ._types import List
from ..models.model import query


def create_allow(ip: str) -> List:
    return query("INSERT INTO allow (ip) VALUES (?)", (ip,))


def get_allow() -> List:
    return query("SELECT ip FROM allow", row_factory=lambda cursor, row: row[0])
