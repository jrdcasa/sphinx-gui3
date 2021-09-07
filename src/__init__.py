__version__ = "0.2.3"

import contextlib
from typing import Optional, List, TextIO


def main(argv: Optional[List[str]] = None, stream: Optional[TextIO] = None) -> int:

    from .sphinx_gui3 import main_app

    with contextlib.ExitStack() as ctx:
        return main_app().execute(ctx)
