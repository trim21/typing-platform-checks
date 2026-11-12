"""Cross module, ``from c15_flags import FLAG``.

The initializer is not statically evaluable, so the imported name is a plain
``bool`` as well.
"""

from typing import assert_type

from c15_flags import FLAG

assert_type(FLAG, bool)
