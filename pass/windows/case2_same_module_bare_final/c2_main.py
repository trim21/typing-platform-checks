"""Same module: the ``Final`` constant is declared and used in this file."""

import os
import sys
from typing import Final

IS_OTHER: Final = sys.platform == "linux"

if IS_OTHER:
    os.getuid()
