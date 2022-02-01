import asyncio
import aiohttp
from ipwhois import IPWhois as _IPWhois
from typing import List, Iterable
from .base import BaseAsyncWhois, Action, Kind
from .cache import IPWhoisCacheHandler
from .extractor import IPWhoisExtractor
from ipaddress import IPv4Address
import time


class IPWhois(BaseAsyncWhois):

    lookup_failed: List[IPv4Address] = []
    extractor = IPWhoisExtractor()
    cache = IPWhoisCacheHandler()

    def __init__(self, rate: int = 5) -> None:
        self.rate = rate
        self.rate_limit = True

    async def _whois(self, ip: IPv4Address):
        """A wrapper function for ipwhois.IPWhois"""
        loop = asyncio.get_running_loop()
        whois_obj = _IPWhois(ip)
        return await loop.run_in_executor(None, whois_obj.lookup_rdap)

    async def _async_whois(self, ip: IPv4Address):
        try:
            await self._limit_rate()
            response = await self._whois(ip)
            extracted = self.extractor.extract(response)
            await self.cache.update(
                Action(
                    Kind.UPDATE_WHOIS_BY_IP,
                    {
                        "ip": ip,
                        "country": extracted["country"],
                        "whois": response,
                    },
                )
            )

            return {"ip": ip, "whois": response}
        except Exception as e:
            print("[IPWHOIS]", e)
            self.lookup_failed.append(ip)
            return {"ip": ip, "whois": {"error": e}}

    async def _limit_rate(self):
        if self.rate_limit:
            sleep_time = 1 / self.rate
            time.sleep(sleep_time)

    async def _cached_async_whois(self, ip: IPv4Address):
        response = await self.cache.read(Action(Kind.GET_CACHE_BY_IP, {"ip": ip}))

        if response == []:
            return await self._async_whois(ip)

        return {"ip": ip, "whois": response}

    async def async_whois(self, ips: Iterable[IPv4Address], cache: bool = True):
        if len(ips) <= 5:
            self.rate_limit = False
        else:
            self.rate_limit = True

        if not cache:
            tasks = [asyncio.create_task(self._async_whois(ip)) for ip in ips]
            return await asyncio.gather(*tasks)

        cached_tasks = [asyncio.create_task(self._cached_async_whois(ip)) for ip in ips]
        return await asyncio.gather(*cached_tasks)


class IPWhoisIO(BaseAsyncWhois):
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def _whois(self, ip):
        async with self.session.get(f"https://ipwhois.app/json/{ip}") as response:
            return await response.json()

    async def async_whois(self, ips):
        tasks = [asyncio.create_task(self._whois(ip)) for ip in ips]
        async with self.session:
            return await asyncio.gather(*tasks)
