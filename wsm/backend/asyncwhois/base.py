from abc import ABC, abstractmethod
from typing import List, Any
from ipaddress import IPv4Address
from dataclasses import dataclass, FrozenInstanceError
from types import SimpleNamespace


class FrozenSimpleNamespace(SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        raise FrozenInstanceError(f"cannot assign to field '{name}'")


@dataclass(frozen=True)
class Action:
    kind: str
    payload: dict

    def __post_init__(self):
        super().__setattr__("payload", FrozenSimpleNamespace(**self.payload))


class BaseWhoisExtractor(ABC):

    __slots__ = ()

    @abstractmethod
    def extract(self, whois_result):
        pass


class BaseCacheHandler(ABC):
    __slots__ = ()

    @abstractmethod
    async def create(self, action: Action):
        raise NotImplementedError

    @abstractmethod
    async def read(self, action: Action):
        raise NotImplementedError

    @abstractmethod
    async def update(self, action: Action):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, action: Action):
        raise NotImplementedError


class BaseAsyncWhois(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def lookup_failed(self) -> List[IPv4Address]:
        pass

    @abstractmethod
    async def async_whois(self, ips: List[IPv4Address], cache: bool = True):
        pass

    @property
    @abstractmethod
    def extractor(self) -> BaseWhoisExtractor:
        raise NotImplementedError

    @property
    @abstractmethod
    def cache(self) -> BaseCacheHandler:
        raise NotImplementedError
