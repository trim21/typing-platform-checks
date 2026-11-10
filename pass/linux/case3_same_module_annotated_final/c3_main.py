"""Same module: the ``Final`` constant is declared and used in this file."""

import os
import sys
from typing import Final

IS_OTHER: Final[bool] = sys.platform == "win32"

if IS_OTHER:
    os.startfile("x")
