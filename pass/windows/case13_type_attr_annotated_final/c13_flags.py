"""The constant under test."""

import sys
from typing import Final

IS_OTHER: Final[bool] = sys.platform == "linux"
