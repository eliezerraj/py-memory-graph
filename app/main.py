
from app.controllers import app

# ----------------------------------------------
# gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8001
# ----------------------------------------------