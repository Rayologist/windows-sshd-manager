from abc import ABC, abstractmethod
import asyncio
from typing import Dict
import re
from pathlib import Path


class BaseStatus(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def pattern(self) -> re.Pattern:
        pass

    def validate_status(self, line: str) -> bool:
        return bool(self.pattern.match(line))

    def extract_status(self, line: str) -> Dict:
        regex_res = self.pattern.finditer(line)
        group_dict = map(lambda m: m.groupdict(), regex_res)
        return group_dict


class BaseStatusFollower(ABC):

    __slots__ = ()

    SEEK_END: int = 2

    def __init__(self, file_path: str, await_seconds: int = None):
        self.file_path: Path = file_path
        self.await_seconds = await_seconds

    @property
    @abstractmethod
    def status_class(self) -> BaseStatus:
        pass

    async def __aiter__(self):
        with open(self.file_path, "r") as f:
            f.seek(0, self.SEEK_END)
            await_count = 0
            while True:
                line = f.readline()
                if not self.status_class.validate_status(line):
                    if await_count > 200 and self.await_seconds is not None:
                        # When no valid status is avalible in a row, await
                        # If this is None, banned ips will never be unbanned
                        # until someone else access ssh service.
                        # This is because the loop will keep "continue"
                        # until it finds another extractable status
                        await_count = 0
                        await asyncio.sleep(self.await_seconds)
                    await_count = await_count + 1  # Not found
                    continue
                await_count = 0  # Found
                yield self.status_class.extract_status(line)
