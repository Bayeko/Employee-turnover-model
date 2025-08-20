from pathlib import Path
from typing import List

import pandas as pd


def load_employee_data(data_dir: str | None = None) -> pd.DataFrame:
    """Load and combine employee information files from a directory.

    The function searches for CSV files matching the pattern
    ``Employee Information *.csv`` within ``data_dir`` and concatenates them
    into a single :class:`~pandas.DataFrame`. When ``data_dir`` is omitted, the
    function looks for these files in the user's Downloads directory.

    Parameters
    ----------
    data_dir:
        Directory path containing the employee CSV files. Defaults to the
        user's Downloads directory.

    Returns
    -------
    pandas.DataFrame
        Combined data from all matched CSV files.

    Raises
    ------
    FileNotFoundError
        If no matching files are found in ``data_dir``.
    """

    data_path = Path(data_dir) if data_dir else Path.home() / "Downloads"
    frames: List[pd.DataFrame] = [pd.read_csv(csv_file) for csv_file in data_path.glob("Employee Information *.csv")]

    if not frames:
        raise FileNotFoundError(
            f"No 'Employee Information *.csv' files found in {data_path}."
        )

    return pd.concat(frames, ignore_index=True)
