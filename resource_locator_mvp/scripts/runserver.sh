#!/usr/bin/env bash
# Handy wrapper to start the Django development server using the project's py310 conda env.
set -euo pipefail

CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"
if [ ! -f "$CONDA_SH" ]; then
  echo "Cannot find conda.sh at $CONDA_SH. Adjust CONDA_SH in this script." >&2
  exit 1
fi

source "$CONDA_SH"
conda activate py310

cd "$(dirname "$0")/.."
echo "Running Django dev server in $(pwd) using $(which python)"
python manage.py runserver 0.0.0.0:8082
