from ._types import datetime, List
from ..models.model import query


def create_country(ip: str) -> List:
    return query("INSERT INTO country (ip) VALUES (?) ON CONFLICT DO NOTHING", (ip,))


def get_country() -> List:
    return query("SELECT * FROM country")
