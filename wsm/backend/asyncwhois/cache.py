from .base import BaseCacheHandler, Action, Kind
import json
from ..services import (
    get_whois,
    create_whois,
    get_whois_by_ip,
    update_whois_by_ip,
    get_cache_by_ip,
)


class IPWhoisCacheHandler(BaseCacheHandler):
    async def create(self, action: Action):
        if action.kind == Kind.CREATE_WHOIS:
            return await create_whois(action.payload.ip)

    async def read(self, action: Action):
        if action.kind == Kind.GET_WHOIS_BY_IP:
            return await get_whois_by_ip(action.payload.ip)
        elif action.kind == Kind.GET_WHOIS:
            return await get_whois()
        elif action.kind == Kind.GET_CACHE_BY_IP:
            return await get_cache_by_ip(action.payload.ip)

    async def update(self, action: Action):
        if action.kind == Kind.UPDATE_WHOIS_BY_IP:
            return await update_whois_by_ip(
                action.payload.ip,
                action.payload.country,
                json.dumps(action.payload.whois),
            )

    async def delete(self, action: Action):
        return super().delete(action)
