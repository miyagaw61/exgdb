import utils

EXGDBFILE = os.path.abspath(os.path.expanduser(__file__))
sys.path.insert(0, os.path.dirname(EXGDBFILE) + "/lib/")

from enert import *

pd = PEDA()
pc = PEDACmd()

class Exgdb():
    def read_int(self, address, intsize=None):
        """
        Customized read_int from https://github.com/longld/peda
        """
        if not intsize:
            intsize = self.intsize()
        value = self.readmem(address, intsize)
        if value == 0:
            return 0
        if value:
            value = to_int("0x" + codecs.encode(value[::-1], 'hex'))
            return value
        else:
            return None

    def read_long(self, address):
        """
        Read a long long value from memory
        """
        return self.read_int(address, 8)

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

class ExgdbCmd(object):
    commands = []
    def __init__(self):
        self.commands = [cmd for cmd in dir(self) if callable(getattr(self, cmd)) ]  

    def ctn(self):
        """
        Continue
        Usage:
            MYNAME
        """
        gdb.execute("continue")

    c = ctn
    setattr(PEDACmd, "ctn", ctn)
    setattr(PEDACmd, "c", ctn)

    def brk(self, *arg):
        """
        Set break point
        Usage:
            MYNAME symbol
        """
        (sym, ) = utils.normalize_argv(arg, 1)
        pd.set_breakpoint(sym)

    b = brk
    setattr(PEDACmd, "brk", brk)
    setattr(PEDACmd, "b", brk)

    def next(self, *arg):
        """
        Next n times
        Usage:
            MYNAME [n]
        """
        (n, ) = utils.normalize_argv(arg, 1)

        if n == None:
            n = 1
        gdb.execute("nexti " + str(n))

    n = next
    setattr(PEDACmd, "next", next)
    setattr(PEDACmd, "n", next)

    def step(self, *arg):
        """
        Nexti n times
        Usage:
            MYNAME [n]
        """
        (n, ) = utils.normalize_argv(arg, 1)

        if n == None:
            n = 1
        gdb.execute("stepi " + str(n))

    s = step
    setattr(PEDACmd, "step", step)
    setattr(PEDACmd, "s", step)

    def afterpc(self, *arg):
        """
        Show n instructions after pc
        Usage:
            MYNAME n
        """
        arch = pd.getarch()
        (expr, ) = utils.normalize_argv(arg,1)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        if arch[1] == 64:
            ip = "$rip"
        else:
            ip = "$eip"
        pd.execute('pdisas %s /%s' % (ip, n))

    afpc = afterpc
    setattr(PEDACmd, "afterpc", afterpc)
    setattr(PEDACmd, "af", afterpc)

    def beforepc(self, *arg):
        """
        Show n instructions before pc
        Usage:
            MYNAME n
        """
        arch = pd.getarch()
        (expr, ) = utils.normalize_argv(arg,1)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = pd.getreg("rip")
        else:
            ip = pd.getreg("eip")
        if n == 1:
            pd.execute('pdisas %s /%s' % (ip, n))
        else:
            addr = pd.prev_inst(ip, n)[1][0]
            pd.execute('pdisas %s /%s' % (addr, n))

    befpc = beforepc
    setattr(PEDACmd, "beforepc", beforepc)
    setattr(PEDACmd, "bef", beforepc)

    def afteraddr(self, *arg):
        """
        Show n instructions after given addr
        Usage:
            MYNAME addr n
        """
        arch = pd.getarch()
        (addr, expr) = utils.normalize_argv(arg,2)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = pd.getreg("rip")
        else:
            ip = pd.getreg("eip")
        pd.execute('pdisas %s /%s' % (addr, n))

    afad = afteraddr
    setattr(PEDACmd, "afteraddr", afteraddr)
    setattr(PEDACmd, "afad", afteraddr)

    def beforeaddr(self, *arg):
        """
        Show n instructions after given addr
        Usage:
            MYNAME addr n
        """
        arch = pd.getarch()
        (addr, expr) = utils.normalize_argv(arg,2)
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = pd.getreg("rip")
        else:
            ip = pd.getreg("eip")
        if n == 1:
            pd.execute('pdisas %s /%s' % (ip, n))
        else:
            addr = pd.prev_inst(ip, n)[1][0]
            pd.execute('pdisas %s /%s' % (addr, n))

    befad = beforeaddr
    setattr(PEDACmd, "beforeaddr", beforeaddr)
    setattr(PEDACmd, "befad", beforeaddr)

    def grp(self, *arg):
        """
        Grep command-output
        Usage:
            MYNAME command regexp
        """
        try:
            (cmd, regex) = utils.normalize_argv(arg, 2)
            print(utils.__file__)
            print(cmd)
            print(regex)
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

    setattr(PEDACmd, "grp", grp)

    def allstack(self):
        """
        Show all stack
        Usage:
            MYNAME
        """
        arch = pd.getarch()
        if arch[1] == 64:
            sp = pd.getreg("rsp")
            bp = pd.getreg("rbp")
        else:
            sp = pd.getreg("esp")
            bp = pd.getreg("ebp")
        arg = bp - sp
        intsize = pd.intsize()
        arg = arg/intsize
        arg += 1
        arg = utils.to_i(arg)
        pd.execute("stack %s" % arg)
        return

    setattr(PEDACmd, "allstack", allstack)

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

    setattr(PEDACmd, "lpout", lpout)

    def nuntil(self, *arg):
        """
        Execute nexti until regex
        Usage:
            MYNAME regex callonlyflag=False
        """
        (regex, callonlyflag) = utils.normalize_argv(arg, 2)
        regex = str(regex)
        r = re.compile(regex)
        arch = pd.getarch()
        ctx = config.Option.get("context")
        config.Option.set("context", "code")
        if callonlyflag == True or callonlyflag == "True":
            cmd = pc.nextcall
        else:
            cmd = pc.next
        pc.next()
        while True:
            (addr, code) = pd.current_inst(pd.getreg("pc"))
            regexed_code = r.findall(code)
            if len(regexed_code) > 0:
                config.Option.set("context", ctx)
                gdb.execute("context")
                break
            else:
                cmd()

    setattr(PEDACmd, "nuntil", nuntil)

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
            cmd = pc.nextcall
        else:
            cmd = pc.next
        next_when_call = pc.next
        step_when_call = pc.step
        arch = pd.getarch()
        ctx = config.Option.get("context")
        config.Option.set("context", "code")
        pc.step()
        while True:
            (addr, code) = pd.current_inst(pd.getreg("pc"))
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
                        pc.step()
                        now_depth = now_depth + 1
                        continue
                elif len(ret_code) > 0:
                    if now_depth <= depth:
                        now_depth = now_depth - 1
                        pc.next()
                        continue
                cmd()

    setattr(PEDACmd, "suntil", suntil)

    def nextcalluntil(self, *arg):
        """
        Execute nextcall until regex
        Usage:
            MYNAME regex
        """
        (regex, ) = utils.normalize_argv(arg, 1)
        regex = str(regex)
        pc.nuntil(regex, True)

    setattr(PEDACmd, "nextcalluntil", nextcalluntil)

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
        pc.suntil(regex, depth, True)

    setattr(PEDACmd, "stepcalluntil", stepcalluntil)

    def nuntilxor(self):
        """
        Execute nexti until jmp-cmds
        Usage:
            MYNAME
        """
        pc.nuntil("xor")

    setattr(PEDACmd, "nuntilxor", nuntilxor)

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
        pc.suntil("xor", depth)

    setattr(PEDACmd, "suntilxor", suntilxor)

    def infonow(self):
        """
        Show detail information of now instruction
        Usage:
            MYNAME
        """
        (addr, code) = pd.current_inst(pd.getreg("pc"))

        # " ANY_REG" or ",ANY_REG"
        for reg in REGISTERS[8]:
            reg_A = " " + reg
            reg_B = "," + reg
            if reg_A in code or reg_B in code:
                reg = reg.replace(" ", "")
                print(green("%s" % reg.upper(), "bold"), end=": ")
                pc.infox(gdb.parse_and_eval("$%s" % reg))
        for reg in REGISTERS[16]:
            regexed_code = re.findall("[ ,]%s" % reg, code)
            if len(regexed_code) > 0:
                print(green("%s" % reg.upper(), "bold"), end=": ")
                pc.infox(gdb.parse_and_eval("$%s" % reg))
        for i in (32, 64):
            for reg in REGISTERS[i]:
                reg_A = " " + reg
                reg_B = "," + reg
                if reg_A in code or reg_B in code:
                    print(green("%3s" % reg.upper(), "bold"), end=": ")
                    if reg == "rip":
                        now_code_str = gdb.execute("pdisass $rip /1", to_string=True)
                        print(now_code_str[6:])
                    else:
                        pc.infox(gdb.parse_and_eval("$%s" % reg))

        # addrs that 0xNNNNNN and more except "[ANY_REG+0xNNNNNN]" from code strings
        addrs = re.findall("[^+](0x[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]+)", code)
        if len(addrs) > 0:
            for addr in addrs:
                #print(green("%s" % addr, "bold"), end=": ")
                pc.infox(addr)

        # "[ANY_EXPR]"
        addrs = re.findall(r"\[[^ ]*\]", code)
        if len(addrs) > 0:
            for addr in addrs:
                displayed_addr = addr
                for reg in REGISTERS[8]:
                    if reg in addr:
                        pc.infox("register", reg)
                        addr = addr.replace(reg, "$" + reg)
                        displayed_addr = displayed_addr.replace(reg, reg.upper())
                for reg in REGISTERS[16]:
                    regexed_code = re.findall("[ ,]%s" % reg, code)
                    if len(regexed_code) > 0:
                        pc.infox("register", reg)
                        addr = addr.replace(reg, "$" + reg)
                        displayed_addr = displayed_addr.replace(reg, reg.upper())
                for i in (32, 64):
                    for reg in REGISTERS[i]:
                        if reg in addr:
                            pc.infox("register", reg)
                            addr = addr.replace(reg, "$" + reg)
                            displayed_addr = displayed_addr.replace(reg, reg.upper())
                addr = addr.replace("[", "")
                addr = addr.replace("]", "")
                addr = str(gdb.parse_and_eval(addr))

                # "0x12341234 <'hogefunction'>" -> "0x12341234"
                addr = re.findall("0x[0-9a-f]+", addr)[0]

                print(green("%s" % displayed_addr, "bold"), end=": ")
                pc.infox(addr)

    inow = infonow
    setattr(PEDACmd, "infonow", infonow)
    setattr(PEDACmd, "inow", infonow)

    def infox(self, *arg):
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
            chain = pd.examine_mem_reference(v)
            text += utils.format_reference_chain(chain)
            text += "\n"
            return text

        (arch, bits) = pd.getarch()
        if str(address).startswith("r"):
            # Register
            regs = pd.getregs(" ".join(arg[1:]))
            if regname is None:
                for r in REGISTERS[bits]:
                    if r in regs:
                        text += get_reg_text(r, regs[r])
            else:
                for (r, v) in sorted(regs.items()):
                    text += get_reg_text(r, v)
            if text:
                utils.msg(text.strip())
            if regname is None or "eflags" in regname:
                self.eflags()
            return

        elif utils.to_int(address) is None:
            warning_utils.msg("not a register nor an address")
        else:
            # Address
            chain = pd.examine_mem_reference(address)
            #text += '\n'
            #text += 'info: '
            text += utils.format_reference_chain(chain) # + "\n"
            vmrange = pd.get_vmrange(address)
            if vmrange:
                (start, end, perm, name) = vmrange
        utils.msg(text)
        return

    setattr(PEDACmd, "infox", infox)

    def contextmode(self, *arg):
        """
        Set context options
        Usage:
            MYNAME options
        """
        (opt, ) = utils.normalize_argv(arg, 1)
        print(opt)
        if opt == None:
            return
        config.Option.set("context", opt)

    setattr(PEDACmd, "contextmode", contextmode)

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
    exgdbcmd = ExgdbCmd()
    ExgdbCmdWrapper()
    for cmd in exgdbcmd.commands :
        ExgdbAlias(cmd,"exgdb %s" % cmd)

def import_other_plugin():
    cmds = [cmd for cmd in dir(PEDA) if cmd != "SAVED_COMMANDS" and callable(getattr(PEDA, cmd))]
    for cmd in cmds:
        if not cmd.startswith("_"):
            cmd_obj = getattr(PEDA, cmd)
            setattr(Exgdb, cmd, cmd_obj)

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

    cmds = [cmd for cmd in dir(PwnCmd) if callable(getattr(PwnCmd, cmd))]
    for cmd in cmds:
        if not cmd.startswith("_"):
            cmd_obj = getattr(PwnCmd, cmd)
            setattr(ExgdbCmd, cmd, cmd_obj)

    cmds = [cmd for cmd in dir(AngelHeapCmd) if callable(getattr(AngelHeapCmd, cmd))]
    for cmd in cmds:
        if not cmd.startswith("_"):
            cmd_obj = getattr(AngelHeapCmd, cmd)
            setattr(ExgdbCmd, cmd, cmd_obj)

init()
import_other_plugin()

class ExgdbOverwriteCmd():
    def parseheap(self, *arg):
        """
        Customized parseheap command from https://github.com/longld/peda
        """
        (arena, ) = utils.normalize_argv(arg, 1)
        if capsize == 0 :
            arch = getarch()
        if not get_heap_info(arena):
            print("Can't find heap info")
            return
        if (main_arena and not enable_thread) or thread_arena == main_arena :
            heapbase = int(gdb.execute("x/" + word + " &mp_.sbrk_base",to_string=True).split(":")[1].strip(),16)
        else :
            print("Can't find heap")
        chunkaddr = heapbase
        addr_str = yellow("addr", "bold")
        prev_str = yellow("prev", "bold")
        size_str = yellow("size", "bold")+yellow("|")+red("NM", "bold")+yellow("|")+green("IM", "bold")+yellow("|")+blue("PI", "bold")+yellow("|")
        fd_str = yellow("fd", "bold")
        bk_str = yellow("bk", "bold")
        NM = red("NM", "bold")
        IM = green("IM", "bold")
        PI = blue("PI", "bold")
        print('{:<32}{:<31}{:<114}{:<30}{:<28}'.format(addr_str, prev_str, size_str, fd_str, bk_str))
        while chunkaddr != top["addr"] :
            try :
                cmd = "x/" + word + hex(chunkaddr)
                prev_size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
                cmd = "x/" + word + hex(chunkaddr + capsize*1)
                size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
                cmd = "x/" + word + hex(chunkaddr + capsize*2)
                fd = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
                cmd = "x/" + word + hex(chunkaddr + capsize*3)
                bk = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
                cmd = "x/" + word + hex(chunkaddr + (size & 0xfffffffffffffff8) + capsize)
                nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
                status = nextsize & 1 
                NM = str(size & 4)
                if(NM == "0"):
                    NM = red("0", "bold")
                else:
                    NM = red("1", "bold")
                IM = str(size & 2)
                if(IM == "0"):
                    IM = green("0", "bold")
                else:
                    IM = green("1", "bold")
                PI = str(size & 1)
                if(PI == "0"):
                    PI = blue("0", "bold")
                else:
                    PI = blue("1", "bold")
                bits = yellow("|") + NM + yellow("|") + IM + yellow("|") + PI + yellow("|")
                size = size & 0xfffffffffffffff8
                if size == 0 :
                    print("\033[31mCorrupt ?! \033[0m(size == 0) (0x%x)" % chunkaddr)
                    break 
                if status :
                    if chunkaddr in fastchunk :
                        msg = "\033[1;34m Freed \033[0m"
                        chunkaddr_str = blue(hex(chunkaddr))
                        print('{:<30}0x{:<17x}{:<102}{:<18}{:<18}'.format(chunkaddr_str, prev_size, hex(size)+bits, hex(fd), "None"))
                    else :
                        msg = "\033[31m Used \033[0m"
                        chunkaddr_str = green(hex(chunkaddr), "bold")
                        print('{:<32}0x{:<17x}{:<102}{:<18}{:<18}'.format(chunkaddr_str, prev_size, hex(size)+bits, "None", "None"))
                else :
                    if chunkaddr in fastchunk:
                        msg = "\033[1;34m Freed \033[0m"
                        chunkaddr_str = blue(hex(chunkaddr))
                        print('{:<30}0x{:<17x}{:<102}{:<18}{:<18}'.format(chunkaddr_str, prev_size, hex(size)+bits, hex(fd), hex(bk)))
                    else:
                        msg = "\033[1;34m Freed \033[0m"
                        chunkaddr_str = blue(hex(chunkaddr), "bold")
                        print('{:<32}0x{:<17x}{:<102}{:<18}{:<18}'.format(chunkaddr_str, prev_size, hex(size)+bits, hex(fd), hex(bk)))
                chunkaddr = chunkaddr + (size & 0xfffffffffffffff8)

                if chunkaddr > top["addr"] :
                    print("\033[31mCorrupt ?!\033[0m")
                    break 
            except :
                print("Corrupt ?!")
                break

    def patch(self, *arg):
        (addr, value, size) = utils.normalize_argv(arg, 3)
        if type(value) == str:
            pc.patch(addr, value)
        elif type(value) == list:
            for (i, x) in enumerate(value):
                pc.patch(addr+i, x)
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
                pc.patch(addr+i, 0)
            for (i, x) in enumerate(bytes_list):
                pc.patch(addr+i, bytes_list[i])
            return True

def overwrite_cmd():
    global exgdbcmd
    cmds = [cmd for cmd in dir(ExgdbOverwriteCmd) if callable(getattr(ExgdbOverwriteCmd, cmd))]
    for cmd in cmds:
        if not cmd.startswith("_"):
            cmd_obj = getattr(ExgdbOverwriteCmd, cmd)
            setattr(ExgdbCmd, cmd, cmd_obj)
            exgdbcmd.commands.append(cmd)
            ExgdbAlias(cmd,"exgdb %s" % cmd)

overwrite_cmd()
