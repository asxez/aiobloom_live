"""

origin author: https://github.com/joseph-fox
author: ASXE  https://github.com/asxez

"""

from io import BytesIO
from typing import Optional

__all__ = [
    "range_fn",
    "is_string_io",
]


def range_fn(start: int = 0, stop: Optional[int] = None):
    return range(start, stop) if stop is not None else range(start)


def is_string_io(instance) -> bool:
    return isinstance(instance, BytesIO)
