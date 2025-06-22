# pipeline/logger.py
from rich.console import Console
from datetime import datetime

console = Console()

class Logger:
    def info(self, msg): console.log(f"[INFO {datetime.now()}] {msg}")
    def error(self, msg): console.log(f"[ERROR {datetime.now()}] {msg}", style="bold red")
    def success(self, msg): console.log(f"[SUCCESS {datetime.now()}] {msg}", style="bold green")

log = Logger()
