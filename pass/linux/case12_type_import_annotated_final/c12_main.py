"""Read type across a module boundary, annotated ``Final[bool]``.

The declared type is ``bool``; ``Final`` means the name cannot be rebound, so
the literal value of the initializer is what a reader observes.
"""

from typing import Literal, assert_type

from c12_flags import IS_OTHER

assert_type(IS_OTHER, Literal[False])
