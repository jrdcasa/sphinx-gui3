__version__ = "0.2.3"

import contextlib
from typing import Optional, List, TextIO


def main(argv: Optional[List[str]] = None, stream: Optional[TextIO] = None) -> int:

    from .sphinx_gui3 import Main

    with contextlib.ExitStack() as ctx:
        return Main().execute(ctx)
