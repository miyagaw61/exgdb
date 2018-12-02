from __future__ import division, print_function, absolute_import, unicode_literals
import os
import sys
import re
import subprocess
import platform

argv = sys.argv
argc = len(argv)
regex_n = re.compile(r'\n')
regex_before_n = re.compile(r'(.*?)\n')
regex_s = re.compile(r' ')
regex_blankline = re.compile(r'^$')

ENTER = 13
SPACE = 32
UP = 65
DOWN = 66
LEFT = 68
RIGHT = 67
CTRL_C = 3
CTRL_D = 4
CTRL_J = 10
CTRL_K = 11
CTRL_H = 8
CTRL_L = 12
CTRL_S = 19

if platform.python_version()[0] == '2':
    python3 = False
    python2 = True
    PYTHON3 = False
    PYTHON2 = True
else:
    python3 = True
    python2 = False
    PYTHON3 = True
    PYTHON2 = False

if PYTHON2:
    input = raw_input

OS = platform.system()
if OS == 'Windows':
    os.system('')

if platform.machine() == 'i386':
    arch = 32
    arch_str = 'i386'
    ARCH = 32
    ARCH_STR = 'i386'
else:
    arch = 64
    arch_str = 'amd64'
    ARCH = 64
    ARCH_STR = 'amd64'
