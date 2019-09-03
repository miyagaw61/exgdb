import utils
import re

EXGDBFILE = os.path.abspath(os.path.expanduser(__file__))
sys.path.insert(0, os.path.dirname(EXGDBFILE) + "/lib/")
RE_BLUE = re.compile(r";34m")

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
        if to_int(val) is not None:
            args[idx] = to_int(val)
        if size and idx == size:
            return args[:idx]

    if size == 0:
        return args
    for i in range(len(args), size):
        args += [None]
    return args

utils.normalize_argv = normalize_argv

class Exgdb():
    def __init__(self):
        pass

class ExgdbCmd():
    def __init__(self):
        pass

def import_other_plugin():
    if "PEDA" in globals():
        cmds = [cmd for cmd in dir(PEDA) if cmd != "SAVED_COMMANDS" and callable(getattr(PEDA, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PEDA, cmd)
                setattr(Exgdb, cmd, cmd_obj)

    if "PEDACmd" in globals():
        cmds = [cmd for cmd in dir(PEDACmd) if callable(getattr(PEDACmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PEDACmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

        cmds = [cmd for cmd in dir(PEDACmd) if callable(getattr(PEDACmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PEDACmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

    if "PwnCmd" in globals():
        cmds = [cmd for cmd in dir(PwnCmd) if callable(getattr(PwnCmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PwnCmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

    if "AngelHeapCmd" in globals():
        cmds = [cmd for cmd in dir(AngelHeapCmd) if callable(getattr(AngelHeapCmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(AngelHeapCmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

import_other_plugin()

e = Exgdb()
c = ExgdbCmd()

class ExgdbMethods():
    global e
    global c

    def get_infox_text(self, *arg, color=None):
        """
        Customized xinfo command from https://github.com/longld/peda
        Usage:
            MYNAME address
            MYNAME register [reg1 reg2]
        """

        (address, regname) = utils.normalize_argv(arg, 2)
        if address is None:
            self._missing_argument()

        text = ""
        #if not self._is_running():
        if False:
            return

        def get_reg_text(r, v):
            text = green("%s" % r.upper().ljust(3), "bold") + ": "
            chain = e.examine_mem_reference(v)
            text += utils.format_reference_chain(chain)
            text += "\n"
            return text

        (arch, bits) = e.getarch()
        if str(address).startswith("r"):
            # Register
            regs = e.getregs(" ".join(arg[1:]))
            if regname is None:
                for r in REGISTERS[bits]:
                    if r in regs:
                        text += get_reg_text(r, regs[r])
            else:
                for (r, v) in sorted(regs.items()):
                    text += get_reg_text(r, v)
            if text:
                return text.strip()
            if regname is None or "eflags" in regname:
                self.eflags()
            return

        elif utils.to_int(address) is None:
            warning_utils.msg("not a register nor an address")
        else:
            # Address
            chain = e.examine_mem_reference(address)
            #text += '\n'
            #text += 'info: '
            text += utils.format_reference_chain(chain) # + "\n"
            if color == "yellow":
                text = RE_BLUE.sub(r";33;01m", text)
            elif color == "white":
                text = RE_BLUE.sub(r";37;01m", text)
            elif color == "gray":
                text = RE_BLUE.sub(r";37m", text)
            #vmrange = e.get_vmrange(address)
            #if vmrange:
            #    (start, end, perm, name) = vmrange
        return text

    def read_int(self, address, intsize=None):
        """
        Customized read_int from https://github.com/longld/peda
        """
        if not intsize:
            intsize = e.intsize()
        value = self.readmem(address, intsize)
        if value:
            value = codecs.encode(value[::-1], 'hex')
            value = value.decode("utf-8")
            value = "0x" + value
            value = to_int(value)
            return value
        else:
            return None

    def read_int_bytes(self, address, intsize=None):
        """
        Customized read_int

        Args:
            - address: address to read (Int)
            - intsize: force read size (Int)

        Returns:
            - byte list ([Int, ...])
        """
        if not intsize:
            intsize = self.intsize()
        value = self.readmem(address, intsize)
        if value == 0:
            return [0]*capsize
        if value:
            byte_list = bin2ints(value)
            return byte_list
        else:
            return None

    def read_byte(self, address, intsize=None):
        """
        Read one byte

        Args:
            - address: address to read (Int)
            - intsize: force read size (Int)

        Returns:
            - one byte data (Int)
        """
        if not intsize:
            intsize = self.intsize()
        value = self.read_int_bytes(address)[0]
        if value == 0:
            return 0
        if value:
            return value
        else:
            return None

    def read_bytes(self, addr, n):
        capsize = self.intsize()
        loopcnt = int(n/capsize)
        rem = n % capsize
        bytes_list = []
        for i in range(loopcnt):
            for x in self.read_int_bytes(addr+capsize*i):
                bytes_list.append(x)
        if rem == 0:
            return bytes_list
        for i in range(rem):
            byte = self.read_byte(addr+i)
            bytes_list.append(byte)
        return bytes_list

    def getchunkinfo(self, *arg):
        global fastchunk
        (victim, showsize) = utils.normalize_argv(arg, 2)
        if capsize == 0 :
            arch = getarch()
        chunkaddr = victim
        if(victim < 100):
            lst = getchunklist()
            chunkaddr = lst[victim]
        if not get_heap_info() :
            print("Can't find heap info")
            return None
        cmd = "x/" + word + hex(chunkaddr)
        prev_size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + capsize*1)
        size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        aligned_size = size & 0xfffffffffffffff8
        if showsize == None:
            showsize = aligned_size
        cmd = "x/" + word + hex(chunkaddr + capsize*2)
        fd = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + capsize*3)
        bk = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        try:
            cmd = "x/" + word + hex(chunkaddr + aligned_size + capsize)
            nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            status = nextsize & 1
            used_flag = 0
            fast_flag = 0
            if status:
                if chunkaddr in fastchunk :
                    used_flag = 0
                    fast_flag = 1
                else :
                    used_flag = 1
            else :
                used_flag = 0
        except:
            used_flag = None
            fast_flag = None
            nextsize = None
        NM = size & 4
        IM = size & 2
        PI = size & 1
        return {'next': chunkaddr + aligned_size, 'aligned_size': aligned_size, 'nextsize': nextsize, 'used_flag': used_flag, 'fast_flag': fast_flag, 'size': showsize, 'NM': NM, 'IM': IM, 'PI': PI, 'fd': fd, 'bk': bk}

    def getchunklist(self):
        #print(yellow("addr               prev      size     ", "bold") + red("NM", "bold") + "/" + green("IM", "bold") + "/" + blue("PI", "bold") + "    " + yellow("fd", "bold") + "                 " + yellow("bk", "bold"))
        if capsize == 0 :
            arch = getarch()
        addr = getheapbase()
        addr = addr + capsize*2
        lst = []
        lst.append(addr)
        chunkinfo = e.getchunkinfo(addr)
        if chunkinfo == None:
            return lst
        addr = chunkinfo['next']
        size = chunkinfo['aligned_size']
        while(addr != -1 and size != 0):
            lst.append(addr)
            chunkinfo = e.getchunkinfo(addr)
            if chunkinfo == None:
                return lst
            addr = chunkinfo['next']
            size = chunkinfo['aligned_size']
        return lst

class ExgdbCmdMethods(object):
    def _is_running(self):
        """
        Customized _is_running function from https://github.com/longld/peda
        This always return 1
        """
        return 1

    setattr(ExgdbCmd, "_is_running", _is_running)

    def st(self):
        """
        Start debugging with ./gdbrc.py
        Usage:
            st
        """
        os.system('rm -rf /tmp/gdb.pause')
        gdb.execute('source ./gdbrc.py')

    def ctn(self):
        """
        Continue
        Usage:
            MYNAME
        """
        gdb.execute("continue")

    c = ctn

    def brk(self, *arg):
        """
        Set break point
        Usage:
            MYNAME symbol
        """
        (sym, ) = utils.normalize_argv(arg, 1)
        e.set_breakpoint(sym)

    b = brk

    def next(self, *arg):
        """
        Next n times
        Usage:
            MYNAME [n]
        """
        (n, ) = utils.normalize_argv(arg, 1)

        if n == None:
            n = 1
        gdb.execute("next " + str(n))

    n = next

    def nexti(self, *arg):
        """
        Next n times
        Usage:
            MYNAME [n]
        """
        (n, ) = utils.normalize_argv(arg, 1)

        if n == None:
            n = 1
        gdb.execute("nexti " + str(n))

    ni = nexti

    def step(self, *arg):
        """
        Nexti n times
        Usage:
            MYNAME [n]
        """
        (n, ) = utils.normalize_argv(arg, 1)

        if n == None:
            n = 1
        gdb.execute("step " + str(n))

    s = step

    def stepi(self, *arg):
        """
        Nexti n times
        Usage:
            MYNAME [n]
        """
        (n, ) = utils.normalize_argv(arg, 1)

        if n == None:
            n = 1
        gdb.execute("stepi " + str(n))

    si = stepi

    def afterpc(self, *arg):
        """
        Show n instructions after pc
        Usage:
            MYNAME n
        """
        arch = e.getarch()
        (expr, ) = utils.normalize_argv(arg,1)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        if arch[1] == 64:
            ip = "$rip"
        else:
            ip = "$eip"
        e.execute('pdisas %s /%s' % (ip, n))

    afpc = afterpc

    def beforepc(self, *arg):
        """
        Show n instructions before pc
        Usage:
            MYNAME n
        """
        arch = e.getarch()
        (expr, ) = utils.normalize_argv(arg,1)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = e.getreg("rip")
        else:
            ip = e.getreg("eip")
        if n == 1:
            e.execute('pdisas %s /%s' % (ip, n))
        else:
            addr = e.prev_inst(ip, n)[1][0]
            e.execute('pdisas %s /%s' % (addr, n))

    befpc = beforepc

    def afteraddr(self, *arg):
        """
        Show n instructions after given addr
        Usage:
            MYNAME addr n
        """
        arch = e.getarch()
        (addr, expr) = utils.normalize_argv(arg,2)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = e.getreg("rip")
        else:
            ip = e.getreg("eip")
        e.execute('pdisas %s /%s' % (addr, n))

    afad = afteraddr

    def beforeaddr(self, *arg):
        """
        Show n instructions after given addr
        Usage:
            MYNAME addr n
        """
        arch = e.getarch()
        (addr, expr) = utils.normalize_argv(arg,2)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = e.getreg("rip")
        else:
            ip = e.getreg("eip")
        if n == 1:
            e.execute('pdisas %s /%s' % (ip, n))
        else:
            addr = e.prev_inst(ip, n)[1][0]
            e.execute('pdisas %s /%s' % (addr, n))

    befad = beforeaddr

    def grp(self, *arg):
        """
        Grep command-output
        Usage:
            MYNAME command regexp
        """
        try:
            (cmd, regex) = utils.normalize_argv(arg, 2)
            cmd = str(cmd)
            regex = str(regex)
            output = gdb.execute(cmd, to_string=True)
            regexed = re.findall(regex, output)
            for line in regexed:
                print(line)
        except Exception as e:
            utils.msg("Exception in grp(%s, %s): %s" % (repr(cmd), repr(regex), e), "red")
            traceback.print_exc()
            return False

    def allstack(self):
        """
        Show all stack
        Usage:
            MYNAME
        """
        arch = e.getarch()
        if arch[1] == 64:
            sp = e.getreg("rsp")
            bp = e.getreg("rbp")
        else:
            sp = e.getreg("esp")
            bp = e.getreg("ebp")
        arg = bp - sp
        intsize = e.intsize()
        arg = arg/intsize
        arg += 1
        arg = int(arg)
        e.execute("stack %s" % arg)
        return

    def lpout(self):
        """
        Execute nexti until loop-end
        Usage:
            MYNAME
        """
        arch = getarch()
        if arch[1] == 64:
            peda.execute("nexti $rcx")
        else:
            peda.execute("nexti $ecx")
        return

    def nuntil(self, *arg):
        """
        Execute nexti until regex
        Usage:
            MYNAME regex callonlyflag=False
        """
        (regex, callonlyflag) = utils.normalize_argv(arg, 2)
        regex = str(regex)
        r = re.compile(regex)
        arch = e.getarch()
        ctx = config.Option.get("context")
        config.Option.set("context", "code")
        if callonlyflag == True or callonlyflag == "True":
            cmd = c.nextcall
        else:
            cmd = c.nexti
        c.nexti()
        while True:
            (addr, code) = e.current_inst(e.getreg("pc"))
            regexed_code = r.findall(code)
            if len(regexed_code) > 0:
                config.Option.set("context", ctx)
                gdb.execute("context")
                break
            else:
                cmd()

    def suntil(self, *arg):
        """
        Execute stepi until regex
        Usage:
            MYNAME regex depth=1 callonlyflag=False
        """
        (regex, depth, callonlyflag) = utils.normalize_argv(arg, 3)
        regex = str(regex)
        depth = utils.to_int(depth)
        r = re.compile(regex)
        r_call = re.compile("call")
        r_ret = re.compile("ret")
        if depth == None:
            depth = 1
        now_depth = 0
        if callonlyflag == True or callonlyflag == "True":
            cmd = c.nextcall
        else:
            cmd = c.nexti
        next_when_call = c.nexti
        step_when_call = c.stepi
        arch = e.getarch()
        ctx = config.Option.get("context")
        config.Option.set("context", "code")
        c.stepi()
        while True:
            (addr, code) = e.current_inst(e.getreg("pc"))
            regexed_code = r.findall(code)
            if len(regexed_code) > 0:
                config.Option.set("context", ctx)
                gdb.execute("context")
                break
            else:
                call_code = r_call.findall(code)
                ret_code = r_ret.findall(code)
                if len(call_code) > 0:
                    if now_depth < depth:
                        c.stepi()
                        now_depth = now_depth + 1
                        continue
                elif len(ret_code) > 0:
                    if now_depth <= depth:
                        now_depth = now_depth - 1
                        c.next()
                        continue
                cmd()

    def nextcalluntil(self, *arg):
        """
        Execute nextcall until regex
        Usage:
            MYNAME regex
        """
        (regex, ) = utils.normalize_argv(arg, 1)
        regex = str(regex)
        c.nuntil(regex, True)

    def stepcalluntil(self, *arg):
        """
        Execute stepcall until regex
        Usage:
            MYNAME regex depth=1
        """
        (regex, depth) = utils.normalize_argv(arg, 2)
        regex = str(regex)
        depth = utils.to_int(depth)
        if depth == None:
            depth = 1
        c.suntil(regex, depth, True)

    def nuntilxor(self):
        """
        Execute nexti until jmp-cmds
        Usage:
            MYNAME
        """
        c.nuntil("xor")

    def suntilxor(self, *arg):
        """
        Execute nexti until jmp-cmds
        Usage:
            MYNAME depth=1
        """
        (depth, ) = utils.normalize_argv(arg, 1)
        depth = utils.to_int(depth)
        if depth == None:
            depth = 1
        c.suntil("xor", depth)

    def infonow(self):
        """
        Show detail information of now instruction
        Usage:
            MYNAME
        """
        (addr, code) = e.current_inst(e.getreg("pc"))

        # " ANY_REG" or ",ANY_REG"
        for reg in REGISTERS[8]:
            reg_A = " " + reg
            reg_B = "," + reg
            if reg_A in code or reg_B in code:
                reg = reg.replace(" ", "")
                prefix = green("%s" % reg.upper(), "bold") + ": "
                infox_text = e.get_infox_text(gdb.parse_and_eval("$%s" % reg))
                print(prefix + infox_text)
        for reg in REGISTERS[16]:
            #regexed_code = re.findall("[ ,]%s" % reg, code)
            #if len(regexed_code) > 0:
            #    print(green("%s" % reg.upper(), "bold"), end=": ")
            #    c.infox(gdb.parse_and_eval("$%s" % reg))
            reg_A = " " + reg
            reg_B = "," + reg
            if reg_A in code or reg_B in code:
                reg = reg.replace(" ", "")
                prefix = green("%s" % reg.upper(), "bold") + ": "
                infox_text = c.get_infox_text(gdb.parse_and_eval("$%s" % reg))
                print(prefix + infox_text)
        for i in (32, 64):
            for reg in REGISTERS[i]:
                reg_A = " " + reg
                reg_B = "," + reg
                if reg_A in code or reg_B in code:
                    prefix = green("%s" % reg.upper(), "bold") + ": "
                    if reg == "rip":
                        now_code_str = gdb.execute("pdisass $rip /1", to_string=True)
                        print(prefix + now_code_str[6:])
                    else:
                        infox_text = e.get_infox_text(gdb.parse_and_eval("$%s" % reg))
                        print(prefix + infox_text)

        # addrs that 0xNNNNNN and more except "[ANY_REG+0xNNNNNN]" from code strings
        addrs = re.findall("[^+](0x[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]+)", code)
        if len(addrs) > 0:
            for addr in addrs:
                #print(green("%s" % addr, "bold"), end=": ")
                c.infox(addr)

        # "[ANY_EXPR]"
        addrs = re.findall(r"\[[^ ]*\]", code)
        if len(addrs) > 0:
            for addr in addrs:
                displayed_addr = addr
                for reg in REGISTERS[8]:
                    if reg in addr:
                        c.infox("register", reg)
                        addr = addr.replace(reg, "$" + reg)
                        displayed_addr = displayed_addr.replace(reg, reg.upper())
                for reg in REGISTERS[16]:
                    #regexed_code = re.findall("[ ,]%s" % reg, code)
                    #if len(regexed_code) > 0:
                    if reg in addr:
                        c.infox("register", reg)
                        addr = addr.replace(reg, "$" + reg)
                        displayed_addr = displayed_addr.replace(reg, reg.upper())
                for i in (32, 64):
                    for reg in REGISTERS[i]:
                        if reg in addr:
                            c.infox("register", reg)
                            addr = addr.replace(reg, "$" + reg)
                            displayed_addr = displayed_addr.replace(reg, reg.upper())
                addr = addr.replace("[", "")
                addr = addr.replace("]", "")
                addr = str(gdb.parse_and_eval(addr))

                # "0x12341234 <'hogefunction'>" -> "0x12341234"
                addr = re.findall("0x[0-9a-f]+", addr)[0]

                prefix = green("%s" % displayed_addr, "bold") + ": "
                infox_text = e.get_infox_text(addr)
                print(prefix + infox_text)

    inow = infonow

    def infox(self, *arg, color=None):
        """
        Customized xinfo command from https://github.com/longld/peda
        Usage:
            MYNAME address
            MYNAME register [reg1 reg2]
        """
        text = e.get_infox_text(*arg, color=color)
        utils.msg(text)
        return

    def contextmode(self, *arg):
        """
        Set context options
        Usage:
            MYNAME options
        """
        (opt, ) = utils.normalize_argv(arg, 1)
        if opt == None:
            return
        config.Option.set("context", opt)

    def patch(self, *arg):
        (addr, value, size) = utils.normalize_argv(arg, 3)
        if type(value) == str:
            c.patch(addr, value)
        elif type(value) == list:
            for (i, x) in enumerate(value):
                c.patch(addr+i, x)
        elif type(value) == int:
            if size == None:
                print("Please specify size.")
                return False
            bytes_list = int2bins(value)
            length = len(bytes_list)
            if size < length:
                print("ERROR: invalid size")
                return False
            n = size - length
            for i in range(n):
                c.patch(addr+i, 0)
            for (i, x) in enumerate(bytes_list):
                c.patch(addr+i, bytes_list[i])
            return True

    def context(self, *arg):
        """
        Customized context command from https://github.com/longld/peda
        """
        (opt, count) = normalize_argv(arg, 2)

        if to_int(count) is None:
            count = 8
        if opt is None:
            opt = config.Option.get("context")
        if opt == "all":
            opt = "register,code,stack"

        opt = opt.replace(" ", "").split(",")

        if not opt:
            return

        #if not self._is_running():
        if False:
            return

        clearscr = config.Option.get("clearscr")
        if clearscr == "on":
            clearscreen()

        status = peda.get_status()
        # display registers
        if "reg" in opt or "register" in opt:
            self.context_register()

        if "infonow" in opt:
            print(red("======================================inow======================================", "bold"))
            c.infonow()
            print(red("================================================================================", "bold"))
            #self.context_code(8)
            if not "stack" in opt:
                msg("[%s]" % ("-"*78), "blue", "light")
                msg("Legend: %s, %s, %s, value" % (red("code"), blue("data"), green("rodata")))

        # display assembly code
        if "code" in opt:
            self.context_code(count)

        # display stack content, forced in case SIGSEGV
        if "stack" in opt or "SIGSEGV" in status:
            self.context_stack(count)
            #if "infonow" in opt:
            #    msg("[%s]" % ("-"*78), "blue", "light")
            #    msg("Legend: %s, %s, %s, value" % (red("code"), blue("data"), green("rodata")))

        if "reg" in opt or "code" in opt or "stack" in opt:
            msg("[%s]" % ("-"*78), "blue", "light")
            msg("Legend: %s, %s, %s, value" % (red("code"), blue("data"), green("rodata")))

        # display stopped reason
        if "SIG" in status:
            msg("Stopped reason: %s" % red(status))

        return

    if "PEDACmd" in globals():
        setattr(PEDACmd, "context", context)

    def showchunk(self, *arg, is_only_header=False):
        global fastchunk
        (victim, showsize) = utils.normalize_argv(arg, 2)
        if capsize == 0 :
            arch = getarch()
        chunkaddr = victim
        if(victim < 100):
            lst = getchunklist()
            chunkaddr = lst[victim]
        if not get_heap_info() :
            print("Can't find heap info")
            return
        cmd = "x/" + word + hex(chunkaddr)
        prev_size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + capsize*1)
        size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        aligned_size = size & 0xfffffffffffffff8
        if showsize == None:
            showsize = aligned_size
        cmd = "x/" + word + hex(chunkaddr + capsize*2)
        fd = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + capsize*3)
        bk = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        try:
            cmd = "x/" + word + hex(chunkaddr + aligned_size + capsize)
            nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            status = nextsize & 1
            used_flag = 0
            fast_flag = 0
            if status:
                if chunkaddr in fastchunk :
                    used_flag = 0
                    fast_flag = 1
                else :
                    used_flag = 1
            else :
                used_flag = 0
        except:
            used_flag = 2
            fast_flag = 2
            nextsize = None
        NM = size & 4
        IM = size & 2
        PI = size & 1
        if used_flag == 1:
            print(
                green("prev| ", "bold")
                #+ yellow(hex(chunkaddr), "bold")
                #+ " --> "
                #+ white(hex(prev_size))
                + e.get_infox_text(chunkaddr, color="yellow")
            )
            print(
                green("size| ", "bold")
                #+ yellow(hex(chunkaddr+capsize), "bold")
                #+ " --> "
                #+ white(hex(showsize))
                + e.get_infox_text(chunkaddr+capsize, color="yellow")
                + yellow(" |")
                + red(str(NM), "bold")
                + yellow("|")
                + green(str(IM), "bold")
                + yellow("|")
                + blue(str(PI), "bold")
                + yellow("|")
                + white(" ( next: ", "bold")
                + yellow(hex(chunkaddr+showsize), "bold")
                + white(" size: ", "bold")
                + yellow(hex(nextsize), "bold")
                + white(" )", "bold")
            )
            gdb.execute("tel " + hex(chunkaddr+capsize*2) + " 2")
            if not is_only_header:
                gdb.execute("tel " + hex(chunkaddr+capsize*4) + " " + hex(int(showsize/capsize-4)))
        elif used_flag == 0:
            print(
                blue("prev| ", "bold")
                #+ yellow(hex(chunkaddr), "bold")
                #+ " --> "
                #+ white(hex(prev_size))
                + e.get_infox_text(chunkaddr, color="yellow")
            )
            print(
                blue("size| ", "bold")
                #+ yellow(hex(chunkaddr+capsize), "bold")
                #+ " --> "
                #+ white(hex(showsize))
                + e.get_infox_text(chunkaddr+capsize, color="yellow")
                + yellow(" |")
                + red(str(NM), "bold")
                + yellow("|")
                + green(str(IM), "bold")
                + yellow("|")
                + blue(str(PI), "bold")
                + yellow("|")
                + white(" ( next: ", "bold")
                + yellow(hex(chunkaddr+showsize), "bold")
                + white(" size: ", "bold")
                + yellow(hex(nextsize), "bold")
                + white(" )", "bold")
            )
            gdb.execute("tel " + hex(chunkaddr+capsize*2) + " 2")
            if not is_only_header:
                gdb.execute("tel " + hex(chunkaddr+capsize*4) + " " + hex(int(showsize/capsize-4)))
        else:
            print(
                yellow("prev| ")
                #+ white(hex(chunkaddr), "bold")
                #+ " --> "
                #+ white(hex(prev_size))
                + e.get_infox_text(chunkaddr, color="gray")
            )
            print(
                yellow("size| ")
                #+ white(hex(chunkaddr+capsize), "bold")
                #+ " --> "
                #+ white(hex(showsize))
                + e.get_infox_text(chunkaddr+capsize, color="gray")
                + white(" ( next: ", "bold")
                + yellow(hex(chunkaddr+showsize), "bold")
                + white(" )", "bold")
            )
            gdb.execute("tel " + hex(chunkaddr+capsize*2) + " 2")
            if not is_only_header:
                gdb.execute("tel " + hex(chunkaddr+capsize*4) + " " + hex(int(showsize/capsize-4)))
        return {'next': chunkaddr + aligned_size, 'nextsize': nextsize, 'used_flag': used_flag, 'fast_flag': fast_flag, 'size': showsize, 'NM': NM, 'IM': IM, 'PI': PI, 'fd': fd, 'bk': bk}

    sc = showchunk

    def showchunks(self):
        chunklist = e.getchunklist()
        for chunk_addr in chunklist:
            c.showchunk(chunk_addr)

    scs = showchunks

    def showchunkheader(self, *arg):
        (victim, ) = utils.normalize_argv(arg, 1)
        c.showchunk(victim, is_only_header=True)

    sch = showchunkheader

    def showchunkheaders(self, *arg):
        chunklist = e.getchunklist()
        for chunk_addr in chunklist:
            c.showchunkheader(chunk_addr)

    schs = showchunkheaders

class ExgdbCmdWrapper(gdb.Command):
    """ Exgdb command wrapper """
    def __init__(self):
        super(ExgdbCmdWrapper,self).__init__("exgdb",gdb.COMMAND_USER)

    def invoke(self,args,from_tty):
        global exgdbcmd
        self.dont_repeat()
        arg = args.split()
        if len(arg) > 0 :
            cmd = arg[0]
            if cmd in exgdbcmd.commands :
                func = getattr(exgdbcmd,cmd)
                func(*arg[1:])
            else :
                print("Unknown command")
        else :
            print("Unknown command")
        return 

class ExgdbAlias(gdb.Command):
    """ Exgdb Alias """
    def __init__(self,alias,command):
        self.command = command
        super(ExgdbAlias,self).__init__(alias,gdb.COMMAND_NONE)

    def invoke(self,args,from_tty):
        self.dont_repeat()
        gdb.execute("%s %s" % (self.command,args))

def init():
    global exgdbcmd
    cmds = [cmd for cmd in dir(ExgdbMethods) if callable(getattr(ExgdbMethods, cmd)) and not cmd.startswith("_")]
    exgdbcmd_cmds = []
    for cmd in cmds:
        setattr(Exgdb, cmd, getattr(ExgdbMethods, cmd))
    cmds = [cmd for cmd in dir(ExgdbCmdMethods) if callable(getattr(ExgdbCmdMethods, cmd)) and not cmd.startswith("_")]
    for cmd in cmds:
        setattr(ExgdbCmd, cmd, getattr(ExgdbCmdMethods, cmd))
    exgdbcmd = ExgdbCmd()
    exgdbcmd.commands = cmds
    ExgdbCmdWrapper()
    for cmd in exgdbcmd.commands :
        if not cmd in ["next", "step", "nexti", "stepi", "n", "s", "ni", "si"]:
            ExgdbAlias(cmd,"exgdb %s" % cmd)

init()
