"""Cross module, ``from c5_flags import IS_OTHER``."""

import os

from c5_flags import IS_OTHER

if IS_OTHER:
    os.getuid()
