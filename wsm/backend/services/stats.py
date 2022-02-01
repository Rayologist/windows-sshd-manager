from ._types import List, datetime
from datetime import timedelta
import asyncio
from ..utils import generate_expire
from ..models.model import async_query
from .banned import get_banned_ips


async def get_stats(find_time: int) -> List:
    tasks = map(
        lambda coro: asyncio.create_task(coro),
        [
            get_currently_failed(find_time),
            get_total_failed(),
            get_currently_banned(),
            get_total_banned(),
            get_banned_ips()
        ],
    )
    return await asyncio.gather(*tasks)


async def get_currently_failed(find_time) -> List:
    end_time: datetime = generate_expire(0)
    start_time: datetime = end_time - timedelta(seconds=find_time)
    return await async_query(
        """
        SELECT COUNT(*) 
        FROM failed 
        WHERE time
        BETWEEN :start_time AND :end_time
        """,
        {"start_time": start_time, "end_time": end_time},
        row_factory=lambda cursor, row: row[0],
    )


async def get_total_failed() -> List:
    return await async_query(
        """
        SELECT COUNT(*) 
        FROM failed
        """,
        row_factory=lambda cursor, row: row[0],
    )


async def get_currently_banned() -> List:
    now: datetime = generate_expire(0)
    return await async_query(
        """
        SELECT COUNT(*)
        FROM banned
        WHERE expire > ?
        """,
        (now,),
        row_factory=lambda cursor, row: row[0],
    )


async def get_total_banned() -> List:
    return await async_query(
        """
        SELECT COUNT(*)
        FROM banned
        """,
        row_factory=lambda cursor, row: row[0],
    )
