# py-memory-graph
py-memory-graph

# create venv
python3 -m venv .venv

# activate
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# run
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8001