"""Cross module, ``c7_flags.IS_OTHER``."""

import os

import c7_flags

if c7_flags.IS_OTHER:
    os.startfile("x")
