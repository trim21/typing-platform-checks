"""A plain ``bool`` can be rebound at runtime, so the branch stays live and
the platform-specific call must be reported."""

import os
import sys

is_other: bool = sys.platform == "win32"
is_other = bool(int(os.environ.get("TARGET_PLATFORM", "0")))

if is_other:
    os.startfile("x")
