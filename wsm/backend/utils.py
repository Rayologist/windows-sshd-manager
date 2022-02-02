from datetime import datetime, timezone, timedelta
from ipaddress import IPv4Address


def parse_datetime(date: str, time: str) -> datetime:
    local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
    return (
        datetime.fromisoformat(f"{date} {time}")
        .replace(tzinfo=local_timezone)
        .astimezone(timezone.utc)
    )


def generate_expire(seconds: int) -> datetime:
    expire = datetime.now() + timedelta(seconds=seconds)
    return expire.astimezone(timezone.utc)


def is_ipv4_address(ip) -> Union[Literal[False], IPv4Address]:
    try:
        return IPv4Address(ip)
    except ValueError:
        return False
