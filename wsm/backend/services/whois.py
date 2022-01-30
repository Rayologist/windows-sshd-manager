from ipaddress import IPv4Address
from ._types import List
from ..models.model import async_query
import json


async def create_whois(ip: IPv4Address) -> List:
    return await async_query(
        """
        INSERT INTO whois (ip) 
        VALUES (?) 
        ON CONFLICT DO NOTHING
        """,
        (str(ip),),
    )


async def get_whois() -> List:
    return await async_query("SELECT * FROM whois")


async def get_whois_by_ip(ip: IPv4Address) -> List:
    return await async_query("SELECT * FROM whois WHERE ip=?", (str(ip),))


async def get_cache_by_ip(ip: IPv4Address) -> List:
    return await async_query(
        """
        SELECT cache 
        FROM whois 
        WHERE ip=? 
        AND cache IS NOT NULL
        """,
        (str(ip),),
        row_factory=lambda cursor, row: json.loads(row[0]) if row != [] else row,
    )


async def get_ip_without_whois() -> List:
    return await async_query(
        "SELECT ip FROM whois WHERE cache IS NULL",
        row_factory=lambda cursor, row: IPv4Address(row[0])
        if row[0] != "::1"
        else None,
    )


async def get_ip_with_whois() -> List:
    return await async_query(
        "SELECT * FROM whois WHERE cache IS NOT NULL",
        row_factory=lambda cursor, row: IPv4Address(row[0]),
    )


async def update_whois_by_ip(ip, country, cache):
    return await async_query(
        """
        INSERT INTO whois (ip, country, cache) 
        VALUES (:ip, :country, :cache) 
        ON CONFLICT DO 
        UPDATE 
        SET country=:country, cache=:cache
        """,
        {"country": country, "cache": cache, "ip": str(ip)},
    )
