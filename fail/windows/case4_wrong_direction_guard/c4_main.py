"""Negated guard: the branch is live on this platform, so the call must be
reported. Proves that pruning respects the direction of the condition."""

import os
import sys
from typing import Final

IS_OTHER: Final[bool] = sys.platform == "linux"

if not IS_OTHER:
    os.getuid()
