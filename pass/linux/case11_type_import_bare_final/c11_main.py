"""Read type across a module boundary, bare ``Final``."""

from typing import Literal, assert_type

from c11_flags import IS_OTHER

assert_type(IS_OTHER, Literal[False])
