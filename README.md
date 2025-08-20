# challengedata

## Data Setup

Run the download script to populate a directory with sample data before using
any of the data-loading utilities. Pass an optional destination directory (the
default is `~/Downloads`):

```bash
./scripts/download_data.sh [DEST_DIR]
```

For example:

```bash
./scripts/download_data.sh ~/Downloads
```

`load_employee_data` expects at least one CSV file matching the pattern
`Employee Information *.csv` inside the directory provided to the function.
If the directory contains no such files, a `FileNotFoundError` is raised
indicating that the data could not be located.
