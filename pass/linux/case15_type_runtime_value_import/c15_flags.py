"""The constant under test, imported by c15_main.py."""

import os
from typing import Final

FLAG: Final[bool] = os.getenv("TYPING_PLATFORM_CHECKS") == "1"
