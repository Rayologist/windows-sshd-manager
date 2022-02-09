from datetime import datetime, timezone, timedelta
from ipaddress import IPv4Address
from typing import Dict, Literal, Union
from functools import reduce
import re


def parse_datetime(date: str, time: str) -> datetime:
    """Infer local time zone from ssh log and transform date and time to UTC"""
    local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
    date_time: datetime = (
        datetime.fromisoformat(f"{date} {time}")
        .replace(tzinfo=local_timezone)
        .astimezone(timezone.utc)
    )

    # SQLite converter will raise an error
    # if a timestamp does not have microseconds,
    # but comes with timezone information
    has_microseconds: bool = bool(date_time.time().microsecond)

    if not has_microseconds:
        date_time = date_time + timedelta(microseconds=1)

    return date_time


def generate_expire(seconds: int) -> datetime:
    expire = datetime.now() + timedelta(seconds=seconds)
    return expire.astimezone(timezone.utc)


def is_ipv4_address(ip) -> Union[Literal[False], IPv4Address]:
    try:
        return IPv4Address(ip)
    except ValueError:
        return False


def _parse_hms(amount: int, unit: Literal["d", "h", "m", "s"]) -> timedelta:
    unit_mapping: Dict = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds"}
    return timedelta(**{unit_mapping[unit]: amount})


def parse_hms(string: str) -> timedelta:
    duplicated = re.findall(r"([dhms]).*\1", string)
    if duplicated:
        raise ValueError(
            f"Duplicate: '{', '.join(duplicated)}' in the string '{string}'"
        )

    extracted_hms = re.findall(r"(\d+)([dhms])", string)

    return reduce(
        lambda x, y: x + y,
        [_parse_hms(int(amount), unit) for amount, unit in extracted_hms],
        timedelta(),
    )


def check_overwritable(save_path: Union[str, Path]) -> bool:
    if not isinstance(save_path, Path):
        save_path = Path(save_path)

    if not save_path.is_file():
        return True

    inp = input(f"Are you sure to overwrite '{save_path}'? (y/n): ")

    if inp in {"y", "Y"}:
        return True

    return False
