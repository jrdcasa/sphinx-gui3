import os
import sys
try:
    import src
except ImportError:
    _this_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.split(_this_dir)[0])