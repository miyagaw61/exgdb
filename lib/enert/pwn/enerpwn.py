from enert.init import *
from .toplevel import *

def p(n, bit):
    return make_packer(bit)(n)

def u(x, bit):
    return make_unpacker(bit)(x)

def s(x, bit):
    return make_unpacker(bit, sign='signed')(x)

def s4(x):
    return make_unpacker(4, sign='signed')(x)

def s8(x):
    return make_unpacker(8, sign='signed')(x)

def s16(x):
    return make_unpacker(16, sign='signed')(x)

def s32(x):
    return make_unpacker(32, sign='signed')(x)

def s64(x):
    return make_unpacker(64, sign='signed')(x)

def allp(n):
    return make_packer('all')(n)

def allu(x):
    if arch == 64:
        return make_unpacker(len(x)*8)(x)
    else:
        return make_unpacker(len(x)*4)(x)

def complement(x, bit):
    tmp = p(x, bit)
    return s(tmp, bit)
