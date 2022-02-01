from ..services import get_stats


async def report_stats(log_path, find_time):
    (
        currently_failed,
        total_failed,
        currently_banned,
        total_banned,
        get_banned_ips,
    ) = await get_stats(find_time)

    reports = (
        f"Failed:\n"
        f"  Currently failed: {currently_failed[0]}\n"
        f"  Total failed: {total_failed[0]}\n"
        f"  Watching file: {log_path}\n"
        f"Banned:\n"
        f"  Currently banned: {currently_banned[0]}\n"
        f"  Total banned: {total_banned[0]}\n"
        f"""  Current banned ips: {", ".join(get_banned_ips)}\n"""
    )
    return reports
