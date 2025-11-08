#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
source .venv/bin/activate
pip install -r requirements.txt >/dev/null
(streamlit run ui/app.py --server.headless true --server.port 8501 &)
sleep 2
open -a "Google Chrome" http://localhost:8501
