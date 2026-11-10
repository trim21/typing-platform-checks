"""The constant under test, imported by c5_main.py."""

import sys
from typing import Final

IS_OTHER: Final[bool] = sys.platform == "linux"
