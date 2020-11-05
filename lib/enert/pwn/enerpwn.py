from enert.init import *
from .toplevel import *

def p(n, bit):
    """
    Make a packet from the given bit.

    Args:
        n: (int): write your description
        bit: (int): write your description
    """
    return make_packer(bit)(n)

def u(x, bit):
    """
    Return the value of x.

    Args:
        x: (int): write your description
        bit: (int): write your description
    """
    return make_unpacker(bit)(x)

def s(x, bit):
    """
    Return a binary string from x

    Args:
        x: (int): write your description
        bit: (int): write your description
    """
    return make_unpacker(bit, sign='signed')(x)

def s4(x):
    """
    Unpack x. s4.

    Args:
        x: (int): write your description
    """
    return make_unpacker(4, sign='signed')(x)

def s8(x):
    """
    S8 - > bytes

    Args:
        x: (int): write your description
    """
    return make_unpacker(8, sign='signed')(x)

def s16(x):
    """
    Return a signed 64 - encoded bytestring.

    Args:
        x: (int): write your description
    """
    return make_unpacker(16, sign='signed')(x)

def s32(x):
    """
    Make a signed 32 - bit integer.

    Args:
        x: (int): write your description
    """
    return make_unpacker(32, sign='signed')(x)

def s64(x):
    """
    Make a 64 - encoded 64 - bit integer.

    Args:
        x: (int): write your description
    """
    return make_unpacker(64, sign='signed')(x)

def allp(n):
    """
    Allocates a packet

    Args:
        n: (todo): write your description
    """
    return make_packer('all')(n)

def allu(x):
    """
    Returns a list of integers.

    Args:
        x: (todo): write your description
    """
    if arch == 64:
        return make_unpacker(len(x)*8)(x)
    else:
        return make_unpacker(len(x)*4)(x)

def complement(x, bit):
    """
    Complement the complement of the given bit.

    Args:
        x: (todo): write your description
        bit: (int): write your description
    """
    tmp = p(x, bit)
    return s(tmp, bit)
