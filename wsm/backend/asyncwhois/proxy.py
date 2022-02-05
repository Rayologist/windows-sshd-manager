from ipaddress import IPv4Address
from .base import BaseAsyncWhois
from typing import Iterable, List
from ..utils import is_ipv4_address


class AsyncWhois:
    def __init__(self, async_whois: BaseAsyncWhois) -> None:
        self._whois = async_whois
        self._whois_result = None

    async def whois(self, ips: Iterable[str], cache: bool = True) -> List:
        filtered_ips = self.filter_ips(ips)
        self._whois_result = await self._whois.async_whois(
            ips=filtered_ips, cache=cache
        )
        return self._whois_result

    def filter_ips(self, ips: Iterable[str]) -> List[IPv4Address]:
        non_repeated_ipv4_addrs = map(is_ipv4_address, set(ips))
        filtered = filter(None, non_repeated_ipv4_addrs)
        return list(filtered)

    @property
    def result(self):
        return self._whois_result

    @property
    def lookup_failed(self) -> List[IPv4Address]:
        return self._whois.lookup_failed
