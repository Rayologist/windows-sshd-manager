from backend import query
from ._types import Cursor


def create_allow(ip: str) -> Cursor:
    return query("INSERT INTO allow (ip) VALUES (?)", (ip,))
