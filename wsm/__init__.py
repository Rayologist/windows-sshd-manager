from .backend import *
from .commands import *

check_config()

if not DB_PATH.is_file():
    init_db()
    init_firewall()
