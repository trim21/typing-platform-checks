"""The constant under test, read as a module attribute."""

import os
from typing import Final

FLAG: Final[bool] = os.getenv("TYPING_PLATFORM_CHECKS") == "1"
