from backend import query
from ._types import List


def create_deny(ip: str) -> List:
    return query("INSERT INTO deny (ip) VALUES (?)", (ip,))
