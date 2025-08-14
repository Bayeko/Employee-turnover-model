#!/usr/bin/env bash
# Download sample employee data into the data/ directory.
set -euo pipefail

DATA_DIR="data"
mkdir -p "$DATA_DIR"

# Sample dataset; replace URL with the actual dataset location if needed.
BASE_URL="https://raw.githubusercontent.com/plotly/datasets/master"
FILE="2014_usa_states.csv"

curl -L "$BASE_URL/$FILE" -o "$DATA_DIR/Employee Information 1.csv"

echo "Data downloaded to $DATA_DIR/Employee Information 1.csv"
