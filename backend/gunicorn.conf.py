import os
from dotenv import load_dotenv

load_dotenv()

bind = f"0.0.0.0:{os.getenv('BACKEND_PORT', '8000')}"
workers = 4
worker_class = "gevent"
timeout = 0
