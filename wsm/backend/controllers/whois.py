import asyncio
from ..asyncwhois import IPWhois, AsyncWhois
from ..services import get_ip_without_whois


async def whois() -> None:

    async_whois = IPWhois()
    whois = AsyncWhois(async_whois)

    while True:
        ips = await get_ip_without_whois()
        await whois.whois(ips)
        await asyncio.sleep(60)
