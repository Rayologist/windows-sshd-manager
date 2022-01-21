from .base import BaseStatus
import re


class FailedPassword(BaseStatus):
    @property
    def pattern(self) -> re.Pattern:
        return re.compile(
            r"(?P<pid>\d+) (?P<date>\d+-\d+-\d+) (?P<time>\d+:\d+:\d+\.\d+) (?P<status>Failed) password for (invalid user)? (?P<username>.*?) from (?P<ip_address>.*?) port (?P<port>\d+) (?P<ssh_version>.*)"
        )


class AcceptedPassword(BaseStatus):
    @property
    def pattern(self) -> re.Pattern:
        return re.compile(
            r"(?P<pid>\d+) (?P<date>\d+-\d+-\d+) (?P<time>\d+:\d+:\d+\.\d+) (?P<status>Accepted) password for (?P<username>.+?) from (?P<ip_address>.*?) port (?P<port>\d+) (?P<ssh_version>.*)"
        )


class AcceptedOrFailedPassword(BaseStatus):
    @property
    def pattern(self) -> re.Pattern:
        return re.compile(
            r"(?P<pid>\d+) (?P<date>\d+-\d+-\d+) (?P<time>\d+:\d+:\d+\.\d+) (?P<status>(Accepted|Failed)) password for (invalid user )?(?P<username>.+?) from (?P<ip_address>.*?) port (?P<port>\d+) (?P<ssh_version>.*)"
        )
