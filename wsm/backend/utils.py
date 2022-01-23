from datetime import datetime, timezone, timedelta


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
