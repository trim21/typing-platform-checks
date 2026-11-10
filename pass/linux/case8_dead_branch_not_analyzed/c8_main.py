"""A dead branch must not be analyzed, so the type error inside it is not
reported."""

import sys
from typing import Final

IS_OTHER: Final[bool] = sys.platform == "win32"

if IS_OTHER:
    bad: int = "not an int"
