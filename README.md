# challengedata

## Data Setup

Run the download script to populate the `data/` directory before using any
of the data-loading utilities:

```bash
./scripts/download_data.sh
```

`load_employee_data` expects at least one CSV file matching the pattern
`Employee Information *.csv` inside the directory provided to the function.
If the directory contains no such files, a `FileNotFoundError` is raised
indicating that the data could not be located.
