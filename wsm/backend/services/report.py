from datetime import timedelta
from ..models.model import query
from ._types import List, Literal, datetime, Optional
from ..utils import generate_expire


def control_columns(column: Literal["ip", "username", "country"]):
    column_mapping = {
        "ip": {"col_outer": "ip", "col_inner": "t.ip, w.country"},
        "username": {"col_outer": "username", "col_inner": "t.username"},
        "country": {"col_outer": "country", "col_inner": "w.country"},
    }
    return column_mapping.get(column)


def interval_factory(cursor, row, table):
    if table in {"failed", "success"}:
        return {
            "ip": row[0],
            "username": row[1],
            "access_time": row[2],
            "country": row[3],
        }
    elif table == "banned":
        return {"ip": row[0], "expiration_time": row[1], "country": row[2]}


def get_table_by_interval(
    table: Literal["success", "failed", "banned"],
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> List:

    if table not in {"success", "failed", "banned"}:
        raise ValueError(f"Invalid parameter: {table}")

    if (end_time is None) or (start_time is None):
        now = generate_expire(0)

    if end_time is None:
        end_time = now

    if start_time is None:
        start_time = now - timedelta(days=366)

    return query(
        f"""
        SELECT t.*, w.country 
        FROM {table} AS t
        INNER JOIN whois AS w
        ON t.ip = w.ip
        WHERE {"time" if table != "banned" else "expire"}
        BETWEEN :start_time and :end_time
        """,
        {"start_time": start_time, "end_time": end_time},
        row_factory=lambda cursor, row: interval_factory(cursor, row, table)
    )


def group_by_factory(cursor, row, column):
    if column == "ip":
        return {"ip": row[0], "country": row[1], "count": row[2]}
    elif column == "username":
        return {"username": row[0], "count": row[1]}
    elif column == "country":
        return {"country": row[0], "count": row[1]}


def get_table_group_by_col(
    table: Literal["success", "failed", "banned"],
    column: Literal["ip", "username", "country"],
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    if table not in {"success", "failed", "banned"}:
        raise ValueError(f"Invalid table: {table}")

    if column not in {"ip", "username", "country"}:
        raise ValueError(f"Invalid column: {column}")

    if table == "banned" and column == "username":
        raise ValueError(f"Invalid column: {column}")

    if (end_time is None) or (start_time is None):
        now = generate_expire(0)

    if end_time is None:
        end_time = now

    if start_time is None:
        start_time = now - timedelta(days=365)

    col = control_columns(column)

    return query(
        f"""
        SELECT *, count({col['col_outer']}) AS count 
        FROM (
          SELECT 
          {col['col_inner']} 
          FROM {table} as t
          INNER JOIN whois AS w
          ON t.ip = w.ip
          WHERE {"t.time" if table != "banned" else "t.expire"} 
          BETWEEN :start_time and :end_time
        ) AS tc
        GROUP BY {col['col_outer']}
        ORDER BY count DESC
        """,
        {"start_time": start_time, "end_time": end_time},
        row_factory=lambda cursor, row: group_by_factory(cursor, row, column),
    )
