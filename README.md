
AES Again

Install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

CLI
python runner.py --mode cbc --op enc --key 603deb1015ca71be2b73aef0857d7781 --in demo/sample.txt --out sample.cbc
python runner.py --mode ctr --op enc --key 2b7e151628aed2a6abf7158809cf4f3c --ctr f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff --in demo/sample.txt --out sample.ctr

Tests
pytest -q

Web UI
streamlit run ui/app.py
link for Dr. Ali: https://relaxed-kataifi-de071e.netlify.app/
