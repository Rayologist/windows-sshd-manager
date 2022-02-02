import asyncio
from functools import reduce
from ..utils import generate_expire, is_ipv4_address
from ..services import (
    create_many_banned,
    get_banned_ips,
    get_to_ban,
    get_allow,
    create_whois,
    update_expire_by_ips,
    get_banned_by_ip,
    get_deny,
)
from ..powershell import PowerShell
from ..config import get_config
from datetime import datetime, timedelta
from typing import List, Set
import pandas as pd


def is_same_ips(ips, firewall_ips):
    ips = "\n".join(ips)
    return ips == firewall_ips


async def update_firewall() -> None:
    ps: PowerShell = PowerShell()
    ips: List = await get_banned_ips()
    firewall_ips = ps.get_firewall_content()

    if not ips:
        ips = ["0.0.0.0"]

    if not is_same_ips(ips, firewall_ips):
        print(f"[FIREWALL]: write {ips}")
        return ps.block_ips(ips)


async def filter_to_ban(to_ban) -> None:
    banned_ips: Set = set(await get_banned_ips())
    whitelist = set(get_allow())
    to_ban: Set = set(to_ban)
    return list(to_ban - banned_ips - whitelist)


async def ban(find_time: int, ban_time: int, max_retry: int) -> None:
    while True:
        end_time: datetime = generate_expire(0)
        start_time: datetime = end_time - timedelta(seconds=find_time)
        expire = generate_expire(ban_time)
        to_ban: List = get_to_ban(start_time, end_time, max_retry)
        to_ban: List = await filter_to_ban(to_ban)
        if to_ban:
            print(f"[BAN] ban: {to_ban} expire: {expire}")
            to_ban: map = map(lambda x: (x, expire), to_ban)
            create_many_banned(to_ban)
        await update_firewall()
        await asyncio.sleep(1)


async def manual_ban(to_ban: List, expire: datetime = None) -> None:
    invalid_ips = list(filter(lambda x: not is_ipv4_address(x), to_ban))
    if invalid_ips:
        print(f"Invalid ip address(es): {', '.join(invalid_ips)} ")
        return
    if expire is None:
        ban_time = get_config()["SSHD"].get("bantime")
        expire = generate_expire(ban_time)
    create_whois_tasks = [asyncio.create_task(create_whois(ip)) for ip in to_ban]
    await asyncio.gather(*create_whois_tasks)
    to_ban: List = await filter_to_ban(to_ban)
    if to_ban:
        to_ban: map = map(lambda x: (x, expire), to_ban)
        create_many_banned(to_ban)
        await update_firewall()


async def filter_to_unban(to_unban):
    denied = set(get_deny())
    whitelist = set(get_allow())
    to_unban: Set = set(to_unban)
    return list(to_unban - denied - whitelist)


async def manual_unban(to_unban, expire=None) -> None:
    if expire == None:
        expire = generate_expire(0)
    to_unban = filter_to_ban(to_unban)
    await update_expire_by_ips(to_unban, expire)


async def manual_get_banned_ips(ips) -> pd.DataFrame:
    tasks = [asyncio.create_task(get_banned_by_ip(ip)) for ip in ips]
    result = await asyncio.gather(*tasks)
    return pd.DataFrame(reduce(lambda x, y: x + y, result, []))
