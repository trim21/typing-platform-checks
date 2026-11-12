"""Cross module, ``c16_flags.FLAG``: still a plain ``bool``."""

from typing import assert_type

import c16_flags

assert_type(c16_flags.FLAG, bool)
