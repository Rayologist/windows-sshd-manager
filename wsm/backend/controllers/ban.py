from ..services import get_to_ban
from ..utils import generate_expire
from ..services import create_many_banned, get_banned_ips
from ..powershell import PowerShell
from datetime import datetime, timedelta
from typing import List


def update_firewall() -> None:
    ps: PowerShell = PowerShell()
    ips: List = get_banned_ips()
    ps.block_ips(ips)


def ban(find_time: int, ban_time: int, max_retry: int):
    end_time: datetime = generate_expire(0)
    start_time: datetime = end_time - timedelta(seconds=find_time)
    ban_from_now = generate_expire(ban_time)
    to_ban: List = get_to_ban(start_time, end_time, max_retry)
    to_ban: map = map(lambda x: (x, ban_from_now), to_ban)
    create_many_banned(to_ban)
