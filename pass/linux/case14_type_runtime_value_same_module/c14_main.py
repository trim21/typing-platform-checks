"""Same module: the initializer is not statically evaluable, so the name is a
plain ``bool`` and no literal value can reach a reader."""

import os
from typing import Final, assert_type

FLAG: Final[bool] = os.getenv("TYPING_PLATFORM_CHECKS") == "1"

assert_type(FLAG, bool)
