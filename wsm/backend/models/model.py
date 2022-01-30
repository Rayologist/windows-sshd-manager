import sqlite3
from typing import Any, Dict, List, Optional, Tuple, Union
from ..config import DB_PATH


def WSM_CONN() -> sqlite3.Connection:
    return sqlite3.connect(
        DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )


def query(
    command: str,
    params: Optional[Union[Tuple[Any], Dict[str, Any]]] = None,
    mode: Optional[str] = None,
    row_factory=None,
) -> List:

    WSM = WSM_CONN()

    if row_factory is not None:
        WSM.row_factory = row_factory

    with WSM:
        if mode == "script":
            return WSM.executescript(command).fetchall()
        elif mode == "many":
            if params is None:
                raise TypeError("parames must be specified")
            return WSM.executemany(command, params).fetchall()

        if params is not None:
            return WSM.execute(command, params).fetchall()

        return WSM.execute(command).fetchall()


async def async_query(
    command: str,
    params: Optional[Union[Tuple[Any], Dict[str, Any]]] = None,
    mode: Optional[str] = None,
    row_factory=None,
) -> List:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, query, command, params, mode, row_factory)


def init_db() -> None:
    if DB_PATH.is_file():
        return

    table = """
        BEGIN TRANSACTION;
        CREATE TABLE whois (
            ip TEXT UNIQUE,
            country TEXT,
            whois TEXT
        );

        CREATE TABLE failed (
            ip TEXT,
            username TEXT,
            time TIMESTAMP
        );

        CREATE TABLE success (
            ip TEXT,
            username TEXT,
            time TIMESTAMP
        );

        CREATE TABLE banned (
            ip TEXT UNIQUE,
            expire TIMESTAMP
        );

        CREATE TABLE allow (
            ip TEXT UNIQUE
        );

        CREATE TABLE deny (
            ip TEXT UNIQUE
        );

        COMMIT;
    """
    query(table, mode="script")
