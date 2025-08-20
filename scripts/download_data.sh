#!/usr/bin/env bash
# Download sample employee data into a destination directory.
set -euo pipefail

DEST_DIR="${1:-$HOME/Downloads}"
mkdir -p "$DEST_DIR"

# Sample dataset; replace URL with the actual dataset location if needed.
BASE_URL="https://raw.githubusercontent.com/plotly/datasets/master"
FILE="2014_usa_states.csv"

curl -L "$BASE_URL/$FILE" -o "$DEST_DIR/Employee Information 1.csv"

echo "Data downloaded to $DEST_DIR/Employee Information 1.csv"
