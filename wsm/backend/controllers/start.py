from datetime import datetime
from typing import Callable, Dict, List
from ..utils import parse_datetime
from ..services import create_failed, create_success, create_whois
from ..followers import AcceptedOrFailedStatusFollower, BaseStatusFollower
import asyncio

status_factory: Dict[str, Callable[[str, str, datetime], List]] = {
    "Failed": create_failed,
    "Accepted": create_success,
}


async def start(file_path) -> None:
    follower: BaseStatusFollower = AcceptedOrFailedStatusFollower(file_path)
    for line in follower:
        line: str = list(line)[0]
        if line["ip_address"] == "::1":
            continue
        create: Callable[[str, str, datetime], List] = status_factory[line["status"]]
        utc: datetime = parse_datetime(line["date"], line["time"])
        create(line["ip_address"], line["username"], utc)
        await create_whois(line["ip_address"])
        await asyncio.sleep(1)
