import sys
import asyncio
from typing import Dict, List
import pandas as pd
from pathlib import Path
import json
import toml

path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(path))

from wsm import *

wsm_parser = WSMParser()

parser = vars(wsm_parser.parse_args())

conf: Dict = get_config()["SSHD"]


if parser.get("subcmd") != "config":
    if conf["logpath"] == "":
        raise NameError(
            f'Please use "wsm config --log-path your/path" to first configure path.'
        )

if parser.get("subcmd") == "start":

    async def main():
        task = asyncio.create_task(
            ban(
                find_time=conf.get("findtime"),
                ban_time=conf.get("bantime"),
                max_retry=conf.get("maxretry"),
            )
        )
        await asyncio.gather(follow(conf["logpath"]), task, whois())

    asyncio.run(main())

if parser.get("subcmd") == "check":
    print(f"check: {parser.get('check')}")
    print(conf)

if parser.get("subcmd") == "status":

    async def main():
        print(
            await report_stats(
                log_path=conf.get("logpath"),
                find_time=conf.get("findtime"),
            )
        )

    asyncio.run(main())


if parser.get("subcmd") == "search":
    print("search")


if parser.get("subcmd") == "whois":
    ips = parser.get("whois")
    cache = not parser.get("no_cache")
    save_path: Path = parser.get("save_path")
    form = parser.get("format") or "toml"

    def format_output(form, data):
        if form == "json":
            return json.dumps(data, indent=4, default=lambda x: str(x))

        elif form == "toml":
            return toml.dumps(data)

    async def main() -> None:
        async_whois = IPWhois()
        whois = AsyncWhois(async_whois)
        result = await whois.whois(ips, cache=cache)
        result = dict(map(lambda x: (str(x["ip"]), x["whois"]), result))
        if save_path is not None:
            if save_path.is_file():
                inp = input(f"Are you sure to overwrite '{save_path}'? (y/n): ")
                if inp in {"y", "Y"}:
                    save_path.write_text(format_output(form=form, data=result))

            else:
                save_path.write_text(format_output(form=form, data=result))

        print(format_output(form=form, data=result))

    asyncio.run(main())

if parser.get("subcmd") == "ban":
    to_ban: List = parser.get("ban")
    expire: str = parser.get("expire") and generate_expire(0) + parse_hms(
        parser.get("expire")
    )
    get: bool = parser.get("get")
    lift: bool = parser.get("lift")

    if get and lift:
        raise wsm_parser.error("--get and --lift can not co-exist")

    elif get:
        result = asyncio.run(manual_get_banned_ips(to_ban))
        if not result.empty:
            print(result)

    elif lift:
        asyncio.run(manual_unban(to_ban, expire))

    else:
        asyncio.run(manual_ban(to_ban, expire))



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
        if parser.get("all"):
            for item in conf:
                print(f"{item}={conf.get(item)}")
        else:
            show = [k for k, v in subparams.items() if v]
            for item in show:
                print(f"{item}={conf.get(item)}")
