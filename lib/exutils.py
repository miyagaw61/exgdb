import os
import sys

EXGDBFILE = os.path.abspath(os.path.expanduser(__file__))
sys.path.insert(0, os.path.dirname(EXGDBFILE) + "/lib/")

import utils
from enert import *

def concat_quote(args):
    tmp_args = []
    flg = False
    n = -1
    for x in args:
        if type(x) != str:
            tmp_args.append(x)
            continue
        if x[0] in ("\"", "'"):
            flg = True
            if x[-1] in ("\"", "'"):
                flg = False
                tmp_args.append(x[1:-1])
                n += 1
            else:
                tmp_args.append(x[1:])
                n += 1
            continue
        if x[-1] in ("\"", "'"):
            flg = False
            tmp_args[n] = "%s %s" % (tmp_args[n], x[:-1])
            continue
        if flg:
            tmp_args[n] = "%s %s" % (tmp_args[n], x)
        else:
            tmp_args.append(x)
            n += 1
    return tmp_args

utils.concat_quote = concat_quote

def normalize_argv(args, size=0):
    """
    Customized normalize_argv from https://github.com/longld/peda
    """
    args = list(args)
    args = utils.concat_quote(args)
    for (idx, val) in enumerate(args):
        if utils.to_int(val) is not None:
            args[idx] = utils.to_int(val)
        if size and idx == size:
            return args[:idx]

    if size == 0:
        return args
    for i in range(len(args), size):
        args += [None]
    return args

utils.normalize_argv = normalize_argv

def clearscreen():
    """
    Customized clearscreen from https://github.com/longld/peda
    """
    print("\x1b[2J\x1b[H")

utils.clearscreen = clearscreen
