from pathlib import Path
from typing import Dict, Union
import toml

pkg_path: Path = Path(__file__).resolve().parent.parent
CONFIG_PATH: Path = pkg_path / ".config" / "config.toml"


def check_config() -> None:
    if not CONFIG_PATH.parent.is_dir():
        CONFIG_PATH.parent.mkdir()

    if not CONFIG_PATH.is_file():
        content = toml.dumps(
            {
                "SSHD": {
                    "logpath": "",
                    "bantime": 10800,
                    "findtime": 600,
                    "maxretry": 10,
                }
            }
        )
        CONFIG_PATH.write_text(content)


def update_config(updates: Dict[str, Dict[str, Union[int, str]]]) -> None:
    updates["SSHD"]["logpath"] = str(updates["SSHD"]["logpath"])
    CONFIG_PATH.write_text(toml.dumps(updates))
