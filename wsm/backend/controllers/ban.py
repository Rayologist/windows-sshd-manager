import asyncio
from ..services import get_to_ban
from ..utils import generate_expire
from ..services import create_many_banned, get_banned_ips, delete_expired, get_allow
from ..powershell import PowerShell
from datetime import datetime, timedelta
from typing import List, Set


def is_same_ips(ips, firewall_ips):
    ips = "\n".join(ips)
    return ips == firewall_ips


def update_firewall() -> None:
    ps: PowerShell = PowerShell()
    ips: List = get_banned_ips()
    firewall_ips = ps.get_firewall_content()

    if not ips:
        ips = ["0.0.0.0"]

    if not is_same_ips(ips, firewall_ips):
        print(f"[FIREWALL]: write {ips}")
        return ps.block_ips(ips)


def filter_to_ban(to_ban) -> None:
    ips: Set = set(get_banned_ips())
    whitelist = set(get_allow())
    to_ban: Set = set(to_ban)
    return list(to_ban - ips - whitelist)


async def ban(find_time: int, ban_time: int, max_retry: int) -> None:
    while True:
        end_time: datetime = generate_expire(0)
        start_time: datetime = end_time - timedelta(seconds=find_time)
        ban_from_now = generate_expire(ban_time)
        to_ban: List = get_to_ban(start_time, end_time, max_retry)
        to_ban: List = filter_to_ban(to_ban)
        if to_ban:
            print(f"[BAN] ban: {to_ban} expire: {ban_from_now}")
            to_ban: map = map(lambda x: (x, ban_from_now), to_ban)
            create_many_banned(to_ban)
        expired = delete_expired()
        if expired:
            print("[Expired] ", expired)
        update_firewall()
        await asyncio.sleep(1)
