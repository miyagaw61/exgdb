

#add by me
import __main__, os, sys, struct, socket, telnetlib, subprocess, time
import sys, re, binascii

home = os.environ['HOME']
mgtoolslib = home + "/mgtools/lib/python"
pedalib = home + "/peda/lib"
if not(os.path.exists(pedalib)):
    print("[+]Error\nTry: mpinstall")
sys.path.append(mgtoolslib)
sys.path.append(pedalib)

import shlex
import string
import signal
import traceback
import codecs
import six
from six.moves import range
from six.moves import input
import six.moves.cPickle as pickle
import pickle
from skeleton import *
from shellcode import *
from utils import *
import config
from nasm import *

sys.path.append("/home/miyagaw61/Pwngdb/")
import pwngdb
#added by me


