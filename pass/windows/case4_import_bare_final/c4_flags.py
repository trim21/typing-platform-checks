"""The constant under test, imported by c4_main.py."""

import sys
from typing import Final

IS_OTHER: Final = sys.platform == "linux"
