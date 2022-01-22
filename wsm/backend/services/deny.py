from backend import query
from ._types import Cursor


def create_deny(ip: str) -> Cursor:
    return query("INSERT INTO deny (ip) VALUES (?)", (ip,))
