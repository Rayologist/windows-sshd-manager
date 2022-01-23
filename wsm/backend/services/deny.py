from ._types import List
from ..models.model import query


def create_deny(ip: str) -> List:
    return query("INSERT INTO deny (ip) VALUES (?)", (ip,))
