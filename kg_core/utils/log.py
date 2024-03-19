import datetime
import sys

class Logger:
    def __init__(self, name):
        self.name = name

    def debug(self, msg):
        print(f"[DEB] [{datetime.datetime.now()}] [{self.name}] {msg}", file=sys.stdout)

    def info(self, msg):
        print(f"[INF] [{datetime.datetime.now()}] [{self.name}] {msg}", file=sys.stdout)

    def error(self, msg):
        print(f"[ERR] [{datetime.datetime.now()}] [{self.name}] {msg}", file=sys.stderr)

    def warning(self, msg):
        print(f"[WRN] [{datetime.datetime.now()}] [{self.name}] {msg}", file=sys.stderr)

