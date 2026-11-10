"""Anchor: the inline platform check that the typing spec expects a checker
to understand ("Version and platform checking"). The platform-specific call in
the dead branch must not be reported."""

import os
import sys

if sys.platform == "linux":
    os.getuid()
