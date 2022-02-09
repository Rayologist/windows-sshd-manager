from ..services import get_table_by_interval, get_table_group_by_col
from ..utils import check_overwritable
import pandas as pd


def report(start_time, end_time, table, group_by=None, save_path=None):
    if group_by is not None:
        result = get_table_group_by_col(
            table=table, column=group_by, start_time=start_time, end_time=end_time
        )
    else:
        result = get_table_by_interval(table, start_time=start_time, end_time=end_time)

    df: pd.DataFrame = pd.DataFrame(result)

    if save_path is not None:
        can_overwrite = check_overwritable(save_path)
        if can_overwrite:
            df.to_csv(save_path, index=False)

    return df
