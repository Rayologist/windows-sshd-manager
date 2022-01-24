from datetime import datetime
from typing import Callable, Dict, List
from ..utils import parse_datetime
from ..services import create_failed, create_success, create_country
from ..followers import AcceptedOrFailedStatusFollower, BaseStatusFollower

status_factory: Dict[str, Callable[[str, str, datetime], List]] = {
    "Failed": create_failed,
    "Accepted": create_success,
}


def start(file_path) -> None:
    follower: BaseStatusFollower = AcceptedOrFailedStatusFollower(file_path)
    for line in follower:
        line: str = list(line)[0]
        create: Callable[[str, str, datetime], List] = status_factory[line["status"]]
        utc: datetime = parse_datetime(line["date"], line["time"])
        create(line["ip_address"], line["username"], utc)
        create_country(line["ip_address"])
