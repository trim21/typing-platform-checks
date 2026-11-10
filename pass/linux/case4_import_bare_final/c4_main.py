"""Cross module, ``from c4_flags import IS_OTHER``."""

import os

from c4_flags import IS_OTHER

if IS_OTHER:
    os.startfile("x")
