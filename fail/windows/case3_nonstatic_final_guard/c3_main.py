"""A ``Final`` whose initializer is not statically evaluable is not a static
condition, so the branch stays live and the call must be reported."""

import os
import sys
from typing import Final


def probe() -> bool:
    return sys.platform == "linux"


IS_OTHER: Final[bool] = probe()

if IS_OTHER:
    os.getuid()
