"""A bare ``Final`` initialized with a platform check reads as a literal."""

import sys
from typing import Final, Literal, assert_type

IS_OTHER: Final = sys.platform == "linux"

assert_type(IS_OTHER, Literal[False])
