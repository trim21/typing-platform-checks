"""The constant under test, read as a module attribute."""

import sys
from typing import Final

IS_OTHER: Final = sys.platform == "linux"
