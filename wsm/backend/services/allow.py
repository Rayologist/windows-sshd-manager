from backend import query
from ._types import List


def create_allow(ip: str) -> List:
    return query("INSERT INTO allow (ip) VALUES (?)", (ip,))
