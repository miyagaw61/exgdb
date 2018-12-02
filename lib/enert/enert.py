#       enert - miyagaw61's python library
#
#       Copyright (C) 2017 Taisei Miyagawa <Twitter: @miyagaw61, WebPage: miyagaw61.github.io>
#
#       License: MIT

from __future__ import division, print_function, absolute_import, unicode_literals
import os, sys, subprocess, re, binascii, shutil
from .init import *
from .toplevel import *
from collections import OrderedDict
import datetime
import ssl
import socket
import better_exceptions
import platform
from backports import shutil_get_terminal_size
from argparse import *
from distutils.dir_util import copy_tree

class File:
    def __init__(self, file_name):
        if file_name[-1] == '/':
            file_name = file_name[:-1]
        self.name = file_name
        self.basename = os.path.basename(self.name)
        self.abspath = os.path.abspath(self.name)

    def name(self):
        return self.name

    def read(self):
        if os.path.exists(self.name):
            try:
                data = open(self.name).read()
            except:
                data = open(self.name, 'rb').read()
            return data
        else:
            return ''
    
    def binary(self):
        if os.path.exists(self.name):
            data = open(self.name, 'rb').read()
            return data

    def readlines(self):
        if os.path.exists(self.name):
            linedata = open(self.name).readlines()
            for i in range(len(linedata)):
                linedata[i] = regex_n.sub('', linedata[i])
            return linedata
        else:
            return ''

    def white_read(self):
        regex_color = re.compile(r'\x1b.*?m')
        if os.path.exists(self.name):
            data = open(self.name).read()
            return regex_color.sub('', data)
        else:
            return ''

    def white_readlines(self):
        regex_color = re.compile(r'\x1b.*?m')
        if os.path.exists(self.name):
            linedata = open(self.name).readlines()
            for i in range(len(linedata)):
                linedata[i] = regex_n.sub('', linedata[i])
                linedata[i] = regex_color.sub('', linedata[i])
            return linedata
        else:
            return ''

    def lines(self):
        if os.path.exists(self.name):
            return len(self.linedata())
        else:
            return ''

    def write(self, data):
        try:
            fd = open(self.name, 'w')
            fd.write(data)
            fd.close()
        except:
            fd = open(self.name, 'wb')
            fd.write(data)
            fd.close()

    def add(self, data):
        try:
            fd = open(self.name, 'a')
            fd.write(data)
            fd.close()
        except:
            fd = open(self.name, 'ab')
            fd.write(data)
            fd.close()

    def exist(self):
        return os.path.exists(self.name)

    def isdir(self):
        return os.path.isdir(self.name)

    def isfile(self):
        return os.path.isfile(self.name)

    def rm(self):
        if not os.path.exists(self.name):
            return None
        if os.path.isdir(self.name):
            shutil.rmtree(self.name)
        else:
            os.unlink(self.name)

    def edit(self):
        editor = 'vi'
        #TODO: add check os.environ
        if os.environ['EDITOR']:
            editor = os.environ['EDITOR']
        cmd = [editor, 
                self.name]
        subprocess.call(cmd)

    def mkdir(self):
        if not self.exist():
            os.makedirs(self.name)

    def cp(self, dst):
        if type(dst) == type(self):
            dst = dst.name
        if not os.path.exists(self.name):
            return None
        if os.path.isdir(self.name):
            copy_tree(self.name, dst)
        else:
            shutil.copy2(self.name, dst)

    def mv(self, dst):
        if type(dst) == type(self):
            dst = dst.name
        if not os.path.exists(self.name):
            return None
        if os.path.isdir(self.name):
            copy_tree(self.name, dst)
        else:
            shutil.copy2(self.name, dst)
        self.rm()

    def create(self):
        lst = self.name.split('/')
        if len(lst) > 1:
            dirs = '/'.join(lst[:-1])
            if not File(dirs).exist():
                File(dirs).mkdir()
        File(self.name).write('')

File.data = File.read
File.linedata = File.readlines
File.white_data = File.white_read
File.white_linedata = File.white_readlines

class Shell:
    def __init__(self, cmd):
        self.cmd = cmd

    def call(self):
        #os.system(self.cmd)
        proc = subprocess.Popen(
                self.cmd,
                shell  = True)
        proc.communicate()

    def read(self):
        proc = subprocess.Popen(
                self.cmd,
                shell  = True,
                stdin  = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        stdout_str, stderr_str = proc.communicate()
        if type(stdout_str) == bytes:
            stdout_str = stdout_str.decode()
        if type(stderr_str) == bytes:
            stderr_str = stderr_str.decode()
        return [stdout_str, stderr_str]

    def readlines(self):
        stdout_str, stderr_str = self.read()
        f = fl('/tmp/enert.tmp')
        f.write(stdout_str)
        linedata = []
        linedata.append(f.linedata())
        f.write(stderr_str)
        linedata.append(f.linedata())
        f.rm()
        return linedata

Shell.data = Shell.read
Shell.linedata = Shell.readlines

esc = '\033'
csi = esc + '['
def to(n=1):
    sys.stdout.write(csi + str(n) + 'G')
    sys.stdout.flush()

def all_delete():
    sys.stdout.write(csi + '2K')
    sys.stdout.write(csi + '1G')
    sys.stdout.flush()

def n2tail_delete(n):
    to(str(n))
    sys.stdout.write(csi + '0K')
    sys.stdout.write(csi + '1G')
    sys.stdout.flush()

def head2n_delete(n):
    to(str(n))
    sys.stdout.write(csi + '1K')
    sys.stdout.write(csi + '1G')
    sys.stdout.flush()

def down(n=1):
    sys.stdout.write(csi + str(n) + 'B')
    sys.stdout.flush()

def up(n=1):
    sys.stdout.write(csi + str(n) + 'A')
    sys.stdout.flush()

def overwrite(strings):
    sys.stdout.write('\r')
    sys.stdout.write(strings)

def save():
    sys.stdout.write(csi + 's')
    sys.stdout.flush()

def restore():
    sys.stdout.write(csi + 'u')
    sys.stdout.flush()

def lines_delete(n):
    sys.stdout.write(csi + str(n) + 'M')

def get_term_size():
    lst = []
    lst.append(shutil_get_terminal_size.get_terminal_size()[1])
    lst.append(shutil_get_terminal_size.get_terminal_size()[0])
    return lst

def clear():
    shell('clear').call()

def writefile(buf_arg,file_name):
    if type(buf_arg) == str:
        with open(file_name, 'w') as f:
            f.write(buf_arg)
    else:
        with open(file_name, 'wb') as f:
            f.write(buf_arg)

def addr2index(x):
    return x*2

def index2addr(x):
    return x/2

def ascii2addr(x):
    addr1 = str(x)[0:2]
    addr2 = str(x)[2:4]
    addr3 = str(x)[4:6]
    addr4 = str(x)[6:8]
    return int(addr4 + addr3 + addr2 + addr1, 16)

def splitn(data, n):
    """
        Usage: splitn(str data, int n)
    """
    length = len(data)
    return [data[i:i+n] for i in range(0, length, n)]

def diff(a, b):
    if a > b:
        return a - b
    else:
        return b - a

def dmp(binary, fmt=None):
    """
        Usage: dmp(bin binary, split=''/'x'/'d')
    """
    res = binascii.hexlify(binary)
    if type(res) == bytes:
        res = str(res)[2:-1]
    if(fmt != None):
        arr = splitn(res, fmt)
        res = []
        for var in arr:
            res.append(ascii2addr(var.decode()))
    return res

def complement(value, s):
    """
        Usage: complement(int value, int s)
    """
    value_str = bin(value)[2:].zfill(s)
    if(value_str[0] == '0'):
        return value
    else:
        value = value - 1
        value = value ^ 2**s-1
        return 0-value

def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Screen():
    def __init__(self):
        save()

    def addstr(self, x, y, strings):
        restore()
        down(y)
        to(x)
        sys.stdout.write(strings)
        restore()

    def overwrite(self, x, y, strings):
        restore()
        down(y)
        to(x)
        all_delete()
        sys.stdout.write(strings)
        restore()

class Menu():
    def __init__(self, lst, function):
        self.i = 0
        self.lst = lst
        self.num = len(lst)
        self.function = function
        self.top = blue('>', 'bold') + '  '
        self.to = 3

    def menu_exit(self):
        restore()
        to(1)
        lines_delete(100)

    def menu_start(self):
        sys.stdout.write(self.top)
        print('')
        for self.i in range(self.num):
            if self.i == 0:
                print(black_red('> ', 'bold') + black_white(self.lst[self.i], 'bold'))
            else:
                print(black_white(' ') +  ' ' + self.lst[self.i])
        self.i = 0
        up(self.num+1)
        save()
        to(self.to)
        while 1:
            key = getch()
            restore()
            sys.stdout.write(self.top)
            to(self.to)
            if (key == 'j' or ord(key) == DOWN) and self.i < self.num-1:
                down(self.i+1)
                all_delete()
                overwrite(black_white(' ') + ' ' + self.lst[self.i])
                restore()
                down(self.i+2)
                overwrite(black_red('> ', 'bold') + black_white(self.lst[self.i+1], 'bold'))
                restore()
                to(3)
                self.i = self.i + 1
            if (key == 'k' or ord(key) == UP) and self.i >= 1:
                down(self.i+1)
                all_delete()
                overwrite(black_white(' ') + ' ' + self.lst[self.i])
                restore()
                down(self.i)
                overwrite(black_red('> ', 'bold') + black_white(self.lst[self.i-1], 'bold'))
                restore()
                to(3)
                self.i = self.i -1
            elif key == 'q' or ord(key) == CTRL_C or ord(key) == CTRL_D:
                self.menu_exit()
                exit()
            elif ord(key) == ENTER:
                self.function(self.i)

def parse_usage(usage, args):
    """
    Usage: parse_usage(usage, args)
    Example usage: 'git [commit <-m>] [push <branch>]'
    Example args: ['commit [-m <comment>]:commit to local repository', 'push [branch]:push to remote repository']
    """
    argparser = ArgumentParser(usage=usage)
    for x in args:
        argparser.add_argument(x.split(':')[0], type=str, help=x.split(':')[1])
    tmp_args = argv
    tmp_args.append('-h')
    args = argparser.parse_args(tmp_args)

def list_check(listA, listB):
    """
    a = [1, 2, 3]
    b = [4, 5, 6]
    list_check(a, b) == 0
    b = [3, 4, 5]
    list_check(a, b) == 1
    """
    ans = 0
    for A in listA:
        for B in listB:
            if A == B:
                ans = 1
    return ans

def help_check(lst, idx=None):
    """
    Usage: help_check()
    Usage: help_check(lst, idx)
    Example: help_check(argv[2:]) #check argv[2:] in '-h' or '--help'
    Example: help_check(argv[2:], 3) # check argc < 3
    """
    if '-h' in argv or '--help' in argv:
        return 1
    else:
        if idx:
            if argc < idx:
                return 1
            else:
                return 0
        else:
            return 0

def select_input(strings, lst):
    while 1:
        ans = input(strings)
        if ans in lst:
            break
    return ans

def list_print(lst):
    for x in lst:
        print(x)

def b():
    import pdb
    pdb.set_trace()

def inf(data, prefix=None, c='green'):
    if prefix == None:
        prefix = '['+red('+','bold')+']'
    else:
        prefix = red(prefix, 'bold')
    term_y, term_x = get_term_size()
    if c == 'green':
        print(green('\n' + '='*term_x, 'bold'))
        sys.stdout.write(prefix)
        print(data)
        print(green('='*term_x + '\n', 'bold'))
    if c == 'red':
        print(red('\n' + '='*term_x, 'bold'))
        sys.stdout.write(prefix)
        print(data)
        print(red('='*term_x + '\n', 'bold'))
    if c == 'blue':
        print(blue('\n' + '='*term_x, 'bold'))
        sys.stdout.write(prefix)
        print(data)
        print(blue('='*term_x + '\n', 'bold'))

def calc(args=None, cmd=False):
    """
    Usage:
    calc('0xa') -> 10
    calc('10 x') -> 0xa
    calc('10 b') -> 0b1010
    calc('5/3') -> 1.5
    """
    if args:
        tmp = args.split(' ')
        args = ['calc']
        for x in tmp:
            args.append(x)
    else:
        args = sys.argv
    argc = len(args)

    if(args[1] == '-h'):
        print('Usage: calc [x/b/i] [expr]')
        exit()

    regex_ipt = re.compile(r'(.*) (.*)')

    if('i' in args):
        while(True):
            sys.stdout.write(green('(calc)$ ', 'bold'))
            ipt_data = input()
            ipt = regex_ipt.findall(ipt_data)
            if not(ipt):
                ipt = ipt_data
                ln = 1
                exp = ipt
            else:
                ipt = ipt[0]
                ln = len(ipt)
                if(ln == 1):
                    exp = ipt[0]
                else:
                    if(len(ipt[0]) == 1): 
                        fmt = ipt[0]
                        exp = ipt[1]
                    else:
                        exp = ipt[0]
                        fmt = ipt[1]
            if(ln == 1):
                if(exp == 'q' or exp == 'exit'):
                    exit()
                else:
                    if cmd:
                        exec('print(' + exp + ')')
                    else:
                        return str(eval(exp))
            else:
                if(fmt.count('x') > 0):
                    if cmd:
                        exec('print(hex(' + exp + '))')
                    else:
                        var = eval(exp)
                        return hex(var)
                elif(fmt.count('b') > 0):
                    if cmd:
                        exec('print(bin(' + exp + '))')
                    else:
                        var =  eval(exp)
                        return bin(var)
    elif('x' in args):
        fmtindex = args.index('x')
        if(fmtindex == 1):
            exp = args[2]
        else:
            exp = args[1]
        if cmd:
            exec('print(hex(' + exp + '))')
        else:
            var = eval(exp)
            return hex(var)
        exit()
    elif('b' in args):
        fmtindex = args.index('b')
        if(fmtindex == 1):
            exp = args[2]
        else:
            exp = args[1]
        if cmd:
            exec('print(bin(' + exp + '))')
        else:
            var = eval(exp)
            return bin(var)
    else:
        exp = args[1]
        if('f' in args):
            if cmd:
                exec('print(1.0*' + exp + ')')
            else:
                return str(eval('1.0*' + exp))
        else:
            if cmd:
                exec('print(' + exp + ')')
            else:
                var = eval(exp)
                return str(var)

def calc_command():
    calc(args=None, cmd=True)

Fl = File
fl = File
shell = Shell
screen = Screen
menu = Menu

def list_uniq(lst):
    lst_uniq = []
    for x in lst:
        if x not in lst_uniq:
            lst_uniq.append(x)
    return lst_uniq

class enerdict(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        key_lst = list(kwargs)
        lst = []
        for key in key_lst:
            lst.append([key, self[key]])
        self.list = lst
        self.keys = list(dict.keys(self))
        self.values = list(dict.values(self))

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.list.append([key, value])
        self.keys = list(dict.keys(self))
        self.values = list(dict.values(self))

    def key(self, idx):
        """
        Will Delete
        """
        return '[+]Enert Is Updated! Please Modify "self.key(n) -> self.keys[n]" !!'

    def value(self, idx):
        """
        Will Delete
        """
        return '[+]Enert Is Updated! Please Modify "self.value(n) -> self.values[n]" !!'

    def append(self, *args, **kwargs):
        if len(args) > 1:
            key = args[0]
            value = args[1]
            self[key] = value
        elif len(kwargs) > 0:
            for key in kwargs:
                self[key] = kwargs[key]

def search(arg, out=False):
    lst,err = Shell("find -type f").linedata()
    length_str = str(len(lst))
    result = []
    for i in range(len(lst)):
        f = File(lst[i])
        data = f.data()
        if type(data) == bytes:
            data = dmp(data)
        if i%100 == 0:
            if out:
                if type(f.data()) == bytes:
                    if len(data) > 50:
                        inf(data[:50], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                    elif len(data) > 5:
                        inf(data[:5], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                    elif len(data) > 0:
                        inf(data[:1], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                    elif len(data) == 0:
                        inf(blue('None', 'bold'), '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                else:
                    if len(data) > 50:
                        tmp = data[:50]
                        if tmp.count('\n') > 0:
                            tmp = regex_before_n.findall(tmp)[0]
                    elif len(data) == 0:
                        tmp = blue('None', 'bold')
                    inf(tmp, '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
        if data.count(arg) > 0:
            result.append(lst[i])

    if out:
        output = ''
        for x in result:
            output += x + '\n'
        inf(output, '[+]RESULT:\n')

    return result

def search_binary(arg, out=False):
    lst,err = Shell("find -type f").linedata()
    length_str = str(len(lst))
    result = []
    for i in range(len(lst)):
        f = File(lst[i])
        data = f.binary()
        if i%100 == 0:
            if out:
                if len(data) > 100:
                    inf(data[:100], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) > 50:
                    inf(data[:50], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) > 5:
                    inf(data[:5], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) > 0:
                    inf(data[:1], '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
                elif len(data) == 0:
                    inf(blue('None', 'bold'), '[' + str(i) + '/' + length_str + ']' + f.name + ':\n')
        if data.count(arg) > 0:
            result.append(lst[i])

    if out:
        output = ''
        for x in result:
            output += x + '\n'
        inf(output, '[+]RESULT:\n')

    return result

def to_ascii(arg):
    result = ''
    for x in arg:
        result += hex(ord(x))[2:]
    return result

def get_now():
    now = datetime.datetime.now() 
    year = str(now.year)[2:]
    month = '{0:02d}'.format(now.month)
    day = '{0:02d}'.format(now.day)
    hour = '{0:02d}'.format(now.hour)
    minute = '{0:02d}'.format(now.minute)
    second = '{0:02d}'.format(now.second)
    return enerdict(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

def to_binary(n):
    byte_len = (len(hex(n))-2)/2
    byte_len = math.ceil(byte_len)
    res = n.to_bytes(byte_len, 'big')
    return res

def split_byte(n):
    hexed = hex(n)[2:]
    lst = splitn(hexed, 2)
    for i in range(len(lst)):
        lst[i] = int(lst[i], 16)
    return lst

def int2bins(int_data):
    int_lst = split_byte(int_data)
    lst = []
    for x in int_lst:
        tmp = b''
        tmp += x.to_bytes(1, 'big')
        lst.append(tmp)
    return lst

def int2bin(int_data):
    int_lst = split_byte(int_data)
    tmp = b''
    for x in int_lst:
        tmp += x.to_bytes(1, 'big')
    return tmp

def bin2ints(n):
    lst = []
    for x in n:
        lst.append(x)
    return lst

def bin2int(bin_data):
    return int.from_bytes(bin_data, 'big')

def bin2hexes(bin_data):
    res_hex_str = bin2ints(bin_data)
    tmp = []
    for x in res_hex_str:
        tmp.append('{0:02x}'.format(x))
    return tmp

def bin2hex(bin_data):
    res_hex_str = bin2ints(bin_data)
    tmp = []
    for x in res_hex_str:
        tmp.append('{0:02x}'.format(x))
    return ''.join(tmp)

def hex2bins(hex_str):
    lst = splitn(hex_str, 2)
    ans = []
    for x in lst:
        a = int(x, 16)
        tmp = b''
        tmp += a.to_bytes(1, 'big')
        ans.append(tmp)
    return ans

def hex2bin(hex_str):
    lst = splitn(hex_str, 2)
    tmp = b''
    for x in lst:
        a = int(x, 16)
        tmp += a.to_bytes(1, 'big')
    return tmp

def hex2ints(hex_str):
    bin_data = hex2bin(hex_str)
    return bin2ints(bin_data)

def hex2int(hex_str):
    bin_data = hex2bin(hex_str)
    return bin2int(bin_data)

def int2hex(int_data):
    bin_data = int2bin(int_data)
    return bin2hex(bin_data)

def int2hexes(int_data):
    bin_data = int2bin(int_data)
    return bin2hexes(bin_data)
        
def sanitize(text):
    return text.encode('utf-8', 'replace').decode('utf-8')

def pad(s, b_size):
    length = len(s)
    n = math.ceil(length / b_size)
    s += n.to_bytes(1, 'big')*n
    #return s + (b_size - len(s) % b_size) * chr(b_size - len(s) % b_size)
    return s

def unpad(s):
    last = s[-2:-1]
    last = bin2int(last)
    padding = s[-ord(s[len(s)-1:]):]
    for x in padding:
        if x != last:
            print('padding-error.')
            exit()
    return s[:-ord(s[len(s)-1:])]

class Ssl:
    def __init__(self, R_HOST, R_PORT):
        self.R_HOST = R_HOST
        self.R_PORT = R_PORT
        self.ssock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.ssock.connect((self.R_HOST, self.R_PORT))

    def send(self, request):
        self.ssock.send(request)
        response = self.ssock.recv(65536)
        self.ssock.close()
        return response

def mkparser(usage, lst=None):
    """
    usage = '''\
    Usage: git2nd [status] [add] [commit]
    '''
    lst = ['status', 'add', 'commit']
    parser = mkparser(usage, lst)
    args = parser.parse_args(argv[1:])
    ->
    args.command == status or add or commit
    args.args == ['file01', 'file02']
    """
    parser = ArgumentParser(usage=usage, formatter_class=RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    if not lst == None:
        parser.add_argument('command', choices=lst)
    parser.add_argument('args', nargs='*')
    return parser

def grep(data, regex):
    return re.compile(regex).findall(data)

def sed(data, regex, after):
    return re.compile(regex).sub(after, data)

def grep(victim, regex):
    if type(victim) != list:
        tmp = []
        tmp.append(victim)
        victim = tmp
    regex = re.compile(regex)
    ret = []
    for i in range(len(victim)):
        tmp = regex.findall(victim[i])
        for j in range(len(tmp)):
            ret.append(tmp[j])
    if ret:
        return victim
    else:
        return None

def ogrep(victim, regex):
    victim = grep(victim, regex)
    regex = re.compile(regex)
    ret = []
    for i in range(len(victim)):
        tmp_ret = regex.findall(victim[i])
        for j in range(len(tmp_ret)):
            ret.append(tmp_ret[j])
    return ret

def exdir(obj):
    import inspect 
    import types
    obj_attrs = dir(obj)
    obj_str = str(type(obj))
    text = "#   %s - UNCALLABLE   #" % obj_str
    print("")
    print("#" * len(text))
    print(text)
    print("#" * len(text))
    print("")
    for obj_attr_str in obj_attrs:
        try:
            obj_attr = getattr(obj, obj_attr_str)
        except:
            print("err: %s" % obj_attr_str)
            continue
        #if not isinstance(obj_attr, types.FunctionType):
        if not callable(obj_attr):
            print(obj_attr_str)
    text = "#    %s - CALLABLE    #" % obj_str
    print("")
    print("#" * len(text))
    print(text)
    print("#" * len(text))
    print("")
    excepts = []
    for obj_attr_str in obj_attrs:
        try:
            obj_attr = getattr(obj, obj_attr_str)
        except:
            print("err: %s" % obj_attr_str)
            continue
        if callable(obj_attr):
            try:
                argspec = inspect.getargspec(obj_attr)
            except:
                print("%s(?)" % obj_attr_str)
                continue
            argspec_args = argspec.args
            argspec_varargs = argspec.varargs
            argspec_keywords = argspec.keywords
            argspec_defaults = argspec.defaults
            print("%s(" % obj_attr_str, end="")
            if argspec_defaults != None:
                defaults_len = len(argspec_defaults)
            else:
                defaults_len = 0
            if argspec_args != None:
                args_len = len(argspec_args)
            else:
                args_len = 0
            defaults_start = args_len - defaults_len
            for (i, x) in enumerate(argspec_args):
                if i != 0:
                    print(", ", end="")
                print("%s" % x, end="")
                if i < defaults_start:
                    continue
                default_value = argspec_defaults[i-defaults_start]
                if type(default_value) == str:
                    print("='%s'" % default_value, end="")
                else:
                    print("=%s" % repr(default_value), end="")
            if argspec_varargs != None:
                print(", *args", end="")
            if argspec_keywords != None:
                print(", **kwargs", end="")
            print(")")
