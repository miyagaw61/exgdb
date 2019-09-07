class BpRetHandler(gdb.FinishBreakpoint):
    def __init__(self, id_str, stop=False, fn=None, source=None, debug=False):
        gdb.FinishBreakpoint.__init__(self, gdb.newest_frame(), internal=True)
        self.id = id_str
        self.stop_ = stop
        self.fn = fn
        self.source = source
        self.debug = debug

    def stop(self):
        if self.debug:
            print("[+]return detected: " + self.id)
        if self.fn != None:
            self.fn()
        if self.source != None:
            gdb.execute("source " + self.source)
        if self.stop_:
            return True
        else:
            return False

class BpHandler(gdb.Breakpoint):
    def __init__(self, id_str, stop=False, ret=False, stop_ret=False, fn=None, ret_fn=None, debug=False, source=None, source_ret=None, debug_ret=False):
        gdb.Breakpoint.__init__(self, id_str, type=gdb.BP_BREAKPOINT, internal=False)
        self.id = id_str
        self.ret = ret
        self.stop_ = stop
        self.stop_ret = stop_ret
        self.fn = fn
        self.ret_fn = ret_fn
        self.debug = debug
        self.debug_ret = debug_ret
        self.source = source
        self.source_ret = source_ret

    def stop(self):
        if self.debug:
            print("[+]enter detected: " + self.id)
        if self.fn != None:
            self.fn()
        if self.source != None:
            gdb.execute("source " + self.source)
        if self.ret or self.source_ret:
            BpRetHandler(self.id, stop=self.stop_ret, fn=self.ret_fn, source=self.source_ret, debug=self.debug_ret)
        if self.stop_:
            return True
        else:
            return False

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

    def grep(self, *arg):
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
            utils.msg("Exception in grep(%s, %s): %s" % (repr(cmd), repr(regex), e), "red")
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

    def tracepoint(self, *arg, fn=None, ret_fn=None, source=None, source_ret=None, stop=False, stop_ret=False, ret=False, debug=False):
        """
        tracepoint
        """
        (addr, arg2, arg3, arg4, arg5) = utils.normalize_argv(arg, 5)
        for argN in [arg2, arg3, arg4, arg5]:
            if argN == None:
                continue
            if argN == "stop=True":
                stop = True
            elif argN == "stop_ret=True":
                stop_ret = True
            elif argN == "ret=True":
                ret = True
            elif argN == "debug=True":
                debug = True
            elif argN[:7] == "source=":
                fpath = argN[7:]
                source = os.path.abspath(fpath)
            elif argN[:11] == "source_ret=":
                fpath = argN[11:]
                source_ret = os.path.abspath(fpath)
        BpHandler(addr, stop=stop, ret=ret, stop_ret=stop_ret, fn=fn, ret_fn=ret_fn, debug=debug, source=source, source_ret=source_ret)
        return

    def rbreak(self, *arg, silent=False):
        """
        regex break
        Usage:
            MYNAME regex(intel)
        """
        (regex, ) = utils.normalize_argv(arg, 1)
        regex = str(regex)
        addrs = e.get_addrs_by_regex(regex)
        if addrs == []:
            print("Not found")
            return -1
        bp_nrs = []
        addr = addrs[0]
        gdb.execute("break *" + hex(addr), to_string=silent)
        bp_info_list = e.get_breakpoints()
        last_binfo = bp_info_list[-1]
        bp_nr = int(last_binfo[0])
        bp_nrs.append(bp_nr)
        for addr in addrs[1:]:
            gdb.execute("break *" + hex(addr), to_string=silent)
            bp_nr += 1
            bp_nrs.append(bp_nr)
        return bp_nrs

    def alldelete(self, *arg):
        """
        delete which can handle list argument too
        """
        (addr, ) = utils.normalize_argv(arg, 1)
        if addr == None:
            return
        if type(addr) == str:
            gdb.execute("delete " + addr)
        elif type(addr) == int:
            gdb.execute("delete " + str(addr))
        elif type(addr) == list:
            addrs = addr
            for addr in addrs:
                c.alldelete(addr)

    def radvance(self, *arg):
        """
        regex advance
        Usage:
            MYNAME regex
        """
        (regex, ) = utils.normalize_argv(arg, 1)
        regex = str(regex)
        bp_nrs = c.rbreak(regex, silent=True)
        if bp_nrs == -1:
            return
        gdb.execute("continue")
        c.alldelete(bp_nrs)

    rad = radvance

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
            regexed_code = re.findall("[ ,]%s" % reg, code)
            reg_A = " " + reg
            reg_B = "," + reg
            if (reg_A in code or reg_B in code) and len(regexed_code) > 0:
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
                        #c.infox("register", reg)
                        addr = addr.replace(reg, "$" + reg)
                        displayed_addr = displayed_addr.replace(reg, reg.upper())
                for reg in REGISTERS[16]:
                    regexed_code = re.findall("[ ,]%s" % reg, code)
                    if reg in addr and len(regexed_code) > 0:
                        #c.infox("register", reg)
                        addr = addr.replace(reg, "$" + reg)
                        displayed_addr = displayed_addr.replace(reg, reg.upper())
                for i in (32, 64):
                    for reg in REGISTERS[i]:
                        if reg in addr:
                            #c.infox("register", reg)
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

        # display "Return value" routine
        data = gdb.execute("beforepc 2", to_string=True)
        before_inst = data.split("\n")[0]
        before_inst = before_inst.split()[3]
        if before_inst == "call":
            arch = e.getarch()
            if arch[1] == 64:
                reg = "rax"
            else:
                reg = "eax"
            prefix = green("RETURN-VALUE", "bold") + ": "
            infox_text = e.get_infox_text(gdb.parse_and_eval("$%s" % reg))
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
            config.Option.set("context", "None")
            return
        config.Option.set("context", opt)

    def clearmode(self, *arg):
        """
        Set clear options
        Usage:
            MYNAME options
        """
        (opt, ) = utils.normalize_argv(arg, 1)
        if opt == None:
            return
        config.Option.set("clearscr", opt)

    peda_patch = PEDACmd.patch

    def hexpatch(self, *arg):
        """
        patch hex-str to addr
        Usage:
            MYNAME <addr> <value> [size]
        """
        addr = None
        value = None
        size = None

        argc = len(arg)
        if argc >= 1:
            addr = arg[0]
            if type(addr) != int:
                addr = int(addr, 0)
        if argc >= 2:
            value = arg[1]
            if type(value) != str:
                print("error: value must be str type")
                return -1
            leng = len(value)
            if leng < 2:
                print("error: value must be hex")
                return -1
        if argc >= 3:
            size = arg[2]
            if type(size) != int:
                size = int(size, 0)

        if size != None:
            for i in range(size):
                gdb.execute("peda_patch " + str(addr+i) + " 0", to_string=True)

        chr_list = list(value)
        chr_nr = len(chr_list)
        i = 0
        idx = 0
        while chr_nr > idx:
            n = chr_list[idx] + chr_list[idx+1]
            n = int(n, 16)
            gdb.execute("peda_patch " + str(addr+i) + " " + hex(n), to_string=True)
            idx += 2
            i += 1

        return 0

    def strpatch(self, *arg):
        """
        patch str to addr
        Usage:
            MYNAME <addr> <value> [size]
        """
        addr = None
        value = None
        size = None

        argc = len(arg)
        if argc >= 1:
            addr = arg[0]
            if type(addr) != int:
                addr = int(addr, 0)
        if argc >= 2:
            value = arg[1]
            value = str(value)
        if argc >= 3:
            size = arg[2]
            if type(size) != int:
                size = int(size, 0)

        if size != None:
            for i in range(size):
                gdb.execute("peda_patch " + str(addr+i) + " 0", to_string=True)

        if not value.isdigit():
            gdb.execute("peda_patch " + str(addr) + " " + value, to_string=True)
            return 0

        chr_list = list(value)
        for (i, x) in enumerate(chr_list):
            gdb.execute("peda_patch " + str(addr+i) + " " + hex(ord(x)), to_string=True)

        return 0

    def wordpatch(self, *arg):
        """
        patch word-data to addr
        Usage:
            MYNAME <addr> <value>
        """
        (addr, value) = utils.normalize_argv(arg, 2)
        for i in range(capsize):
            gdb.execute("peda_patch " + str(addr+i) + " 0", to_string=True)
        gdb.execute("peda_patch " + str(addr) + " " + hex(value), to_string=True)

        return 0

    def context_infonow(self):
        """
        context_infonow
        """
        print(red("======================================inow======================================", "bold"))
        c.infonow()
        print(red("================================================================================", "bold"))

    def context(self, *arg):
        """
        Customized context command from https://github.com/longld/peda
        """
        (opt, count) = normalize_argv(arg, 2)

        if utils.to_int(count) is None:
            count = 8
        if opt is None:
            opt = config.Option.get("context")
        if opt == "all":
            opt = "register,code,stack"

        opt = opt.replace(" ", "").split(",")

        if not opt:
            return

        # do not display
        if "none" in opt or "None" in opt:
            return

        #if not self._is_running():
        if False:
            return

        clearscr = config.Option.get("clearscr")
        if clearscr == "on":
            utils.clearscreen()

        status = peda.get_status()

        # display registers
        if "none" in opt or "None" in opt:
            c.context_none()

        # display registers
        if "reg" in opt or "register" in opt:
            c.context_register()

        # display infonow
        if "infonow" in opt or "inow" in opt:
            c.context_infonow()

        # display assembly code
        if "code" in opt:
            c.context_code(count)

        # display stack content, forced in case SIGSEGV
        if "stack" in opt or "SIGSEGV" in status:
            c.context_stack(count)
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
            return None
        cinfo = e.getchunkinfo(victim)
        if cinfo != None:
            prev_size = cinfo['prev_size']
            size = cinfo['size']
            aligned_size = cinfo['aligned_size']
            if showsize == None:
                showsize = aligned_size
            fd = cinfo['fd']
            bk = cinfo['bk']
            used_flag = cinfo['used_flag']
            fast_flag = cinfo['fast_flag']
            nextsize = cinfo['nextsize']
            NM = cinfo['NM']
            IM = cinfo['IM']
            PI = cinfo['PI']
        else:
            print("Cannot access memory address")
            return -1
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

    def edit(self, *arg):
        """
        edit file by $EDITOR
        """
        (fname, ) = utils.normalize_argv(arg, 1)
        editor = os.environ.get("EDITOR")
        if editor == None: editor = "vi"
        gdb.execute("shell" + " " +  editor + " " + fname)

    vim = edit
    emacs = edit
