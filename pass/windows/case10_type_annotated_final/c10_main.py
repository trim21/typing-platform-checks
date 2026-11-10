"""An annotated ``Final[bool]`` reads as a literal, like the bare form."""

import sys
from typing import Final, Literal, assert_type

IS_OTHER: Final[bool] = sys.platform == "linux"

assert_type(IS_OTHER, Literal[False])
