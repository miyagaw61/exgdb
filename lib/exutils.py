import os
import sys

EXGDBFILE = os.path.abspath(os.path.expanduser(__file__))
sys.path.insert(0, os.path.dirname(EXGDBFILE) + "/lib/")

import utils
from enert import *

def clearscreen():
    """
    Customized clearscreen from https://github.com/longld/peda
    """
    print("\x1b[2J\x1b[H")

utils.clearscreen = clearscreen
