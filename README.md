# challengedata

## Data Setup

Run the download script to populate the `data/` directory before using any
of the data-loading utilities:

```bash
./scripts/download_data.sh
```

`load_employee_data` searches for files named `Employee Information *.csv`.
If no directory is provided, it looks in the user's `Downloads` folder:

```python
from employee_data import load_employee_data

df = load_employee_data()  # uses ~/Downloads
```

Pass a path to override the default, such as the directory populated by the
download script:

```python
df = load_employee_data("data")
```

If the chosen directory contains no matching files, a `FileNotFoundError` is
raised indicating that the data could not be located.
