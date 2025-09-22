bind = "0.0.0.0:8000"
workers = 3
timeout = 60
worker_class = "sync"   # default
accesslog = "-"         # logs sur stdout
errorlog = "-"          # logs sur stdout
graceful_timeout = 30
