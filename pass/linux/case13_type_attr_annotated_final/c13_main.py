"""Read type through a module attribute, annotated ``Final[bool]``."""

from typing import Literal, assert_type

import c13_flags

assert_type(c13_flags.IS_OTHER, Literal[False])
