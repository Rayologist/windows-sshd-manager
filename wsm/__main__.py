import sys
import pandas as pd
from pathlib import Path
import toml

path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(path))

from wsm import *

wsm_parser = WSMParser()

parser = vars(wsm_parser.parse_args())

conf = toml.load(CONFIG_PATH)["SSHD"]


if parser.get("subcmd") != "config":
    if conf["logpath"] == "":
        raise NameError(
            f'Please use "wsm config --log-path your/path" to first configure path.'
        )


if parser.get("subcmd") == "check":
    print(f"check: {parser.get('check')}")
    print(conf)

if parser.get("subcmd") == "search":
    print("search")


if parser.get("subcmd") == "whois":
    print("whois")

if parser.get("subcmd") == "ban":
    print("ban")


if parser.get("subcmd") == "config":
    subcommand = parser.get("subconfig")

    subparams = {
        "bantime": parser.get("ban_time"),
        "logpath": parser.get("log_path"),
        "findtime": parser.get("find_time"),
        "maxretry": parser.get("max_retry"),
        "all": parser.get("all"),
    }

    if not any(subparams.values()):
        wsm_parser.error("No actions requested")

    if subcommand == "set":
        updates = {
            "SSHD": {
                "logpath": subparams.get("logpath") or conf.get("logpath"),
                "bantime": subparams.get("bantime") or conf.get("bantime"),
                "findtime": subparams.get("findtime") or conf.get("findtime"),
                "maxretry": subparams.get("maxretry") or conf.get("maxretry"),
            }
        }
        update_config(updates)

    if subcommand == "get":
        if parser.get('all'):
            for item in conf:
                 print(f"{item}={conf.get(item)}")
        else:        
            show = [ k for k, v in subparams.items() if v]
            for item in show:
                print(f"{item}={conf.get(item)}")
