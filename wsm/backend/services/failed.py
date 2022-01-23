from ._types import datetime, List
from ..models.model import query


def create_failed(ip: str, username: str, time: datetime) -> List:
    return query(
        "INSERT INTO failed (ip, username, time) VALUES (?, ?, ?)", (ip, username, time)
    )


def get_failed() -> List:
    return query("SELECT * FROM failed")


def get_to_ban(start_time: datetime, end_time: datetime, max_retry: int) -> List:
    to_ban: str = """
    SELECT ip
    FROM (
        SELECT ip, count(ip) AS count
        FROM failed
        WHERE time BETWEEN :start_time AND :end_time
        GROUP BY ip
    ) 
    WHERE count > :max_retry
    """
    result: List = query(
        to_ban, {"start_time": start_time, "end_time": end_time, "max_retry": max_retry}
    )
    return list(map(lambda x: x[0], result))
