#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
  echo "Installing dependencies..."
  .venv/bin/pip install -q -r requirements.txt
fi
echo "Activating virtual environment and starting Streamlit on port 9999..."
source .venv/bin/activate
exec streamlit run streamlit_app.py --server.port 9999
