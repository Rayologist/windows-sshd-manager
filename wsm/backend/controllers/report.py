from datetime import datetime
from typing import Literal, Optional, Union, List
from pathlib import Path
from ..services import get_table_by_interval, get_table_group_by_col
from ..utils import check_overwritable
import pandas as pd


def report(
    start_time: datetime,
    end_time: datetime,
    table: Literal["success", "failed", "banned"],
    group_by: Optional[Literal["ip", "username", "country"]] = None,
    save_path: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    if group_by is not None:
        result: List = get_table_group_by_col(
            table=table, column=group_by, start_time=start_time, end_time=end_time
        )
    else:
        result: List = get_table_by_interval(
            table, start_time=start_time, end_time=end_time
        )

    df: pd.DataFrame = pd.DataFrame(result)

    if save_path is not None:
        can_overwrite: bool = check_overwritable(save_path)
        if can_overwrite:
            df.to_csv(save_path, index=False)

    return df
