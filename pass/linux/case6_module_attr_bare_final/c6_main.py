"""Cross module, ``c6_flags.IS_OTHER``."""

import os

import c6_flags

if c6_flags.IS_OTHER:
    os.startfile("x")
