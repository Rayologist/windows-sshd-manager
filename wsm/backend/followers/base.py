from abc import ABC, abstractmethod
from typing import Dict
import re

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

    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    @abstractmethod
    def status_class(self) -> BaseStatus:
        pass

    def __iter__(self):
        with open(self.file_path, "r") as f:
            f.seek(0, self.SEEK_END)
            while True:
                line = f.readline()

                if not self.status_class.validate_status(line):
                    continue

                yield self.status_class.extract_status(line)
