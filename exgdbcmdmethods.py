r_asmStr = re.compile(r"0x[0-9a-f]*\x1b\[0m\s\((.*)\)")
r_asmStr_2 = re.compile(r"<.*>:\s*(.*)")
r_asmStr_3 = re.compile(r"^([^\s]*)\s*(.*)")
r_args = re.compile(r"(.*),(.*)")
regs = sum(REGISTERS.values(), [])
asm_ops = {};
asm_ops["mov"] = "mov_reg_imm:mov_reg_reg:mov_reg_ptr:mov_ptr_imm:mov_ptr_reg:mov_ptr_imm"
asm_ops["mov_reg_imm"] = "Write[arg1]:arg2"
asm_ops["mov_reg_reg"] = "Read[arg2]:arg2_data,Write[arg1]:arg2_data"
asm_ops["mov_reg_ptr"] = "Read[arg2_reg]:arg2_reg_data,Read[arg2_data]:main_data,Write[arg1]:main_data"
asm_ops["mov_ptr_imm"] = "Read[arg1_reg]:arg1_reg_data,Write[arg1_data]:arg2"
asm_ops["mov_ptr_reg"] = "Read[arg2]:arg2_data,Read[arg1_reg]:arg1_reg_data,Write[arg1_data]:arg2_data"
asm_ops["mov_ptr_ptr"] = "Read[arg2_reg]:arg2_reg_data,Read[arg2_data]:main_data,Read[arg1_reg]:arg1_reg_data,Write[arg1_data]:main_data"
asm_ops["lea"] = "Read[arg2_reg]:arg2_reg_data,Write[arg1]:arg2_data"
asm_ops["cmp"] = "Read[arg1]:arg1_data"
asm_ops["add"]     = "add_reg_reg:add_reg_imm:add_reg_ptr:add_ptr_imm:add_ptr_reg"
asm_ops["add_reg_reg"] = "Read[arg1]:arg1_data,Read[arg2]:arg2_data,Write[arg1]:new_data"
asm_ops["add_reg_imm"] = "Read[arg1]:arg1_data,Write[arg1]:new_data"
asm_ops["add_reg_ptr"] = "Read[arg1]:arg1_data,Read[arg2_reg]:arg2_reg_data,Read[arg2_data]:org_data,Write[arg1]:new_data"
asm_ops["add_ptr_imm"] = ""
asm_ops["add_ptr_reg"] = ""
asm_ops["sub"]     = "sub_reg_reg:sub_reg_imm:sub_reg_ptr:sub_ptr_imm:sub_ptr_reg"
asm_ops["sub_reg_reg"] = "Read[arg1]:arg1_data,Read[arg2]:arg2_data,Write[arg1]:new_data"
asm_ops["sub_reg_imm"] = "Read[arg1]:arg1_data,Write[arg1]:new_data"
asm_ops["sub_reg_ptr"] = "Read[arg1]:arg1_data,Read[arg2_reg]:arg2_reg_data,Read[arg2_data]:org_data,Write[arg1]:new_data"
asm_ops["sub_ptr_imm"] = ""
asm_ops["sub_ptr_reg"] = ""
asm_ops["nop"] = ""
(arch, bits) = peda.getarch()
if bits == 64:
    asm_ops["push"] = "Read[rsp]:sp_addr,Write[rsp]:new_sp_addr,Read[rsp]:new_sp_addr,Write[new_sp_addr]:arg1_data"
if bits == 32:
    asm_ops["push"] = "Read[esp]:sp_addr,Write[esp]:new_sp_addr,Read[esp]:new_sp_addr,Write[new_sp_addr]:arg1_data"
if bits == 64:
    asm_ops["ret"] = "Read[rsp]:sp_addr,Read[sp_addr]:sp_data,Write[rip]:sp_data,Read[rsp]:sp_addr,Write[rsp]new_sp_addr"
else:
    asm_ops["ret"] = "Read[esp]:sp_addr,Read[sp_addr]:sp_data,Write[rip]:sp_data,Read[esp]:sp_addr,Write[esp]new_sp_addr"
if bits == 64:
    asm_ops["leave"] = "Read[rbp]:bp_addr,Write[rsp]:bp_addr,Read[rsp]:sp_addr,Read[sp_addr]:sp_data,Write[rbp]:sp_data,Read[rsp]:sp_addr,Write[rsp]new_sp_addr"
else:
    asm_ops["leave"] = "Read[ebp]:bp_addr,Write[esp]:bp_addr,Read[esp]:sp_addr,Read[sp_addr]:sp_data,Write[ebp]:sp_data,Read[esp]:sp_addr,Write[esp]:new_sp_addr"
#r_comment = re.compile(r"\s*#.*$")
r_comment_before = re.compile(r"\[.*$")
r_comment = re.compile(r".*#\s")
r_comment2 = re.compile(r"\s.*$")

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
    def __init__(self, id_str, stop=False, ret=False, stop_ret=False, fn=None, ret_fn=None, debug=False, source=None, source_ret=None):
        gdb.Breakpoint.__init__(self, id_str, type=gdb.BP_BREAKPOINT, internal=False)
        self.id = id_str
        self.ret = ret
        self.stop_ = stop
        self.stop_ret = stop_ret
        self.fn = fn
        self.ret_fn = ret_fn
        self.debug = debug
        self.source = source
        self.source_ret = source_ret

    def stop(self):
        if self.debug:
            print("[+]enter  detected: " + self.id)
        if self.fn != None:
            self.fn()
        if self.source != None:
            gdb.execute("source " + self.source)
        if self.ret or self.source_ret:
            BpRetHandler(self.id, stop=self.stop_ret, fn=self.ret_fn, source=self.source_ret, debug=self.debug)
        if self.stop_:
            return True
        else:
            return False

class TraceHandler(gdb.Breakpoint):
    def __init__(self, id_str, fpath, pid, silent=False):
        gdb.Breakpoint.__init__(self, id_str, type=gdb.BP_BREAKPOINT, internal=False)
        self.id = id_str
        self.fpath = fpath
        self.silent = silent
        self.pid = pid

    def stop(self):
        try:
            c.memtrace(self.fpath, pid=self.pid)
        except Exception as e:
            traceback.print_exc()
        if not self.silent:
            gdb.execute("shell cat " + self.fpath + " | tail -1")
        return False

class ExgdbCmdMethods(object):
    def _is_running(self):
        """
        Customized _is_running function from https://github.com/longld/peda
        This always return 1
        """
        return 1

    setattr(ExgdbCmd, "_is_running", _is_running)

    def start(self, *arg):
        """
        Start debugging
        Usage:
            start [buf filename]
        """
        (script_name, ) = utils.normalize_argv(arg, 1)
        if script_name == None:
            gdb.execute("start")
        else:
            gdb.execute("start < " + script_name)

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

    def nextnow(self, *arg):
        """
        Show n instructions next now
        Usage:
            MYNAME n
        """
        arch = e.getarch()
        (expr, ) = utils.normalize_argv(arg,1)
        if expr == None:
            expr = 10
        expr = str(expr)
        n = gdb.parse_and_eval(expr)
        if arch[1] == 64:
            ip = "$rip"
        else:
            ip = "$eip"
        e.execute('pdisas %s /%s' % (ip, n))

    nnow = nextnow

    def prevnow(self, *arg):
        """
        Show n instructions prev now
        Usage:
            MYNAME n
        """
        arch = e.getarch()
        (expr, ) = utils.normalize_argv(arg,1)
        if expr == None:
            expr = 10
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

    pnow = prevnow

    def nextpd(self, *arg):
        """
        Show n instructions next given addr
        Usage:
            MYNAME addr n
        """
        arch = e.getarch()
        (addr, expr) = utils.normalize_argv(arg,2)
        if expr == None:
            expr = 10
        expr = str(expr)
        if expr[0] == "/":
            expr = expr[1:]
        n = gdb.parse_and_eval(expr)
        n = utils.to_int(n)
        if arch[1] == 64:
            ip = e.getreg("rip")
        else:
            ip = e.getreg("eip")
        e.execute('pdisas %s /%s' % (addr, n))

    npd = nextpd

    def prevpd(self, *arg):
        """
        Show n instructions prev given addr
        Usage:
            MYNAME addr n
        """
        arch = e.getarch()
        (addr, expr) = utils.normalize_argv(arg,2)
        if expr == None:
            expr = 10
        expr = str(expr)
        if expr[0] == "/":
            expr = expr[1:]
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

    ppd = prevpd

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
        (addr, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9) = utils.normalize_argv(arg, 9)
        for argN in [arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9]:
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

    def rtracepoint(self, *arg, silent=False, pid=None):
        """
        regex break
        Usage:
            MYNAME regex(intel)
        """
        (regex, fpath, start_addr, end_addr, arg5, arg6) = utils.normalize_argv(arg, 6)
        def is_silent_option(arg):
            if silent == False and type(arg) == str and len(arg) > 10 and arg[:7] == "silent=":
                return True
            else:
                return False
        def is_pid_option(arg):
            if pid == None and type(arg) == str and len(arg) > 7 and arg[:4] == "pid=":
                return True
            else:
                return False
        if is_silent_option(arg5):
            silent = arg5[7:11]
        elif is_pid_option(arg5):
            pid = arg5[4:8]
        if is_silent_option(arg6):
            silent = arg6[7:11]
        elif is_pid_option(arg6):
            pid = arg6[4:8]
        regex = str(regex)
        addrs = e.get_addrs_by_regex(regex, start_addr=start_addr, end_addr=end_addr)
        if addrs == []:
            print("Not found")
            return -1
        bp_nrs = []
        addr = addrs[0]
        addr = hex(addr)
        def function():
            c.memtrace(fpath, pid=pid)
            if not silent:
                gdb.execute("shell cat " + fpath + " | tail -1")
        c.tracepoint("*" + addr, fn=function)
        bp_info_list = e.get_breakpoints()
        last_binfo = bp_info_list[-1]
        bp_nr = int(last_binfo[0])
        bp_nrs.append(bp_nr)
        for addr in addrs[1:]:
            addr = hex(addr)
            c.tracepoint("*" + addr, fn=function)
            bp_nr += 1
            bp_nrs.append(bp_nr)
        return bp_nrs

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
        data = gdb.execute("prevnow 2", to_string=True)
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
        (address, regname, color) = utils.normalize_argv(arg, 3)
        if address == None:
            print("error: missing arguments")
            return
        if regname != None and regname[:6] == "color=":
            regname = None
            color = regname[6:]
        if color != None and color[:6] == "color=":
            color = color[6:]
        text = e.get_infox_text(address, regname=regname, color=color)
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

    def strpatch(self, *arg, null=False):
        """
        patch str to addr
        Usage:
            MYNAME <addr> <value> [size]
        """
        addr = None
        value = None
        size = None

        def is_null_option(arg):
            if type(arg) == str and len(arg) > 8 and arg[:5] == "null=":
                return True
            else:
                return False

        def get_null(arg):
            if arg[5:10] == "True":
                null = True
            else:
                null = False
            return null

        argc = len(arg)
        if argc >= 1:
            if is_null_option(arg[0]):
                null = get_null(arg[0])
            else:
                addr = arg[0]
                if type(addr) != int:
                    addr = int(addr, 0)
        if argc >= 2:
            if is_null_option(arg[1]):
                null = get_null(arg[1])
            else:
                value = arg[1]
                value = str(value)
        if argc >= 3:
            if is_null_option(arg[2]):
                null = get_null(arg[2])
            else:
                size = arg[2]
                if type(size) != int:
                    size = int(size, 0)
        if argc >= 4:
            if is_null_option(arg[3]):
                null = get_null(arg[3])

        if size != None:
            for i in range(size):
                gdb.execute("peda_patch " + str(addr+i) + " 0", to_string=True)

        chr_list = list(value)
        str_size = len(chr_list)
        for (i, x) in enumerate(chr_list):
            gdb.execute("peda_patch " + str(addr+i) + " " + hex(ord(x)), to_string=True)
        if null == True:
            gdb.execute("peda_patch " + str(addr+str_size) + " 0", to_string=True) 

        return 0

    def wordpatch(self, *arg):
        """
        patch word-data to addr
        Usage:
            MYNAME <addr> <value>
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

        (arch, bits) = e.getarch()
        capsize = int(bits / 8)
        for i in range(capsize):
            gdb.execute("peda_patch " + str(addr+i) + " 0", to_string=True)
        gdb.execute("peda_patch " + str(addr) + " " + hex(int(value, 0)), to_string=True)

        return 0

    def context_infonow(self):
        """
        context_infonow
        """
        print(red("======================================inow======================================", "bold"))
        c.infonow()
        print(red("================================================================================", "bold"))

    def context_memtrace(self):
        """
        context_memtrace
        """
        print(red("======================================memt======================================", "bold"))
        c.memtrace()
        print(red("================================================================================", "bold"))

    def context_memt_inow(self):
        """
        context_memt_inow
        """
        print(red("====================================memtinow===================================", "bold"))
        try:
            c.memtrace()
        except:
            pass
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

        # display memtrace and infonow
        if ("memtrace" in opt or "memt" in opt) and ("infonow" in opt or "inow" in opt):
            c.context_memt_inow()
        elif "memtrace" in opt or "memt" in opt:
            c.context_memtrace()
        elif "infonow" in opt or "inow" in opt:
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
            lst = get_chunklist()
            chunkaddr = lst[victim]
        if not get_heap_info() :
            print("Can't find heap info")
            return None
        cinfo = e.get_chunkinfo(victim)
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
                + yellow(hex(chunkaddr+capsize), "bold")
                + " --> "
                + white(hex(size), "bold")
                #+ e.get_infox_text(chunkaddr+capsize, color="yellow")
                + yellow(" |")
                + white(hex(aligned_size), "bold")
                + yellow("|")
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
                + yellow(hex(chunkaddr+capsize), "bold")
                + " --> "
                + white(hex(size), "bold")
                #+ e.get_infox_text(chunkaddr+capsize, color="yellow")
                + yellow(" |")
                + white(hex(aligned_size), "bold")
                + yellow("|")
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
        chunklist = e.get_chunklist()
        for chunk_addr in chunklist:
            c.showchunk(chunk_addr)

    scs = showchunks

    def showchunkheader(self, *arg):
        (victim, ) = utils.normalize_argv(arg, 1)
        c.showchunk(victim, is_only_header=True)

    sch = showchunkheader

    def showchunkheaders(self, *arg):
        chunklist = e.get_chunklist()
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

    def tracemode(self, *arg, silent=False, pid=None):
        """
        tracemode
        Usage:
            MYNAME <on/off>
        """
        (mode, logFile_path, start_addr, end_addr, arg5, arg6) = utils.normalize_argv(arg, 6)
        def is_silent_option(arg):
            if silent == False and type(arg) == str and len(arg) > 10 and arg[:7] == "silent=":
                return True
            else:
                return False
        def is_pid_option(arg):
            if pid == None and type(arg) == str and len(arg) > 7 and arg[:4] == "pid=":
                return True
            else:
                return False
        if is_silent_option(arg5):
            silent = arg5[7:11]
        elif is_pid_option(arg5):
            pid = arg5[4:8]
        if is_silent_option(arg6):
            silent = arg6[7:11]
        elif is_pid_option(arg6):
            pid = arg6[4:8]
        if pid == None:
            pid = e.getpid()
        if mode == "on":
            f_log = File(logFile_path)
            if f_log.exist():
                f_log.rm()
            f_log.create()
        exgdbpath = os.environ.get("EXGDBPATH")
        fpath = e.getfile()
        fname = os.path.basename(fpath)
        out, err = Shell("shell md5sum " + fpath).readlines()
        md5sum = ""
        if out != []:
            md5sum = out[0]
            md5sum = md5sum.split()[0]
            md5sum = str(md5sum)
        f_bpnrs = File(exgdbpath + "/.cache/" + md5sum + ".bpnrs")
        if mode == "on":
            bp_nrs = c.rtracepoint(".*", logFile_path, start_addr, end_addr, silent=silent, pid=pid)
            print(red("\n[+]tracemode: on\n", "bold"))
            if f_bpnrs.exist():
                f_bpnrs.rm()
            f_bpnrs.create()
            f_bpnrs.write(repr(bp_nrs))
        elif mode == "off":
            bp_nrs = f_bpnrs.read()
            bp_nrs = eval(bp_nrs)
            c.alldelete(bp_nrs)
            print(blue("\n[+]tracemode: off\n", "bold"))


    def tracecontinue(self, *arg):
        """
        tracing continue
        Usage:
            MYNAME log_filename
        """
        (log_filename, ) = utils.normalize_argv(arg, 1)
        br_lst = e.get_breakpoints()
        enb_br_lst = []
        for i in range(len(br_lst)):
            enb = br_lst[i][3]
            if enb:
                enb_br_lst.append(br_lst[i][4])
        context_opts = config.Option.get("context")
        config.Option.set("context", "None")
        clearscr = config.Option.get("clearscr")
        config.Option.set("clearscr", "off")
        exgdbpath = os.environ.get("EXGDBPATH")
        if log_filename == None:
            log_filename = exgdbpath + "/.cache/tracecontinue.tmp"
        f_log = File(log_filename)
        symbol_memo = "symbol_memo.txt"
        f_symbol_memo = File(symbol_memo)
        if f_log.exist():
            f_log.rm()
        f_log.create()
        if f_symbol_memo.exist():
            f_symbol_memo.rm()
        f_symbol_memo.create()
        old_pc = 0;
        while True:
            c.nexti()
            pc = e.getreg("pc")
            if pc == old_pc:
                print("error")
                f.add("error\n")
                break
            old_pc = pc
            ret = c.memtrace(log_filename)
            if ret == -1:
                break
            if pc in enb_br_lst:
                break
        if log_filename == exgdbpath + "/.cache/tracecontinue.tmp":
            gdb.execute("shell cat " + exgdbpath + "/.cache/tracecontinue.tmp")
        config.Option.set("clearscr", clearscr)
        config.Option.set("context", context_opts)

    def memtrace(self, *arg, pid=None):
        """
        tracing continue
        Usage:
            MYNAME log_filename
        """
        (log_filename, _pid) = utils.normalize_argv(arg, 2)
        if _pid == None:
            _pid = pid
        pid = _pid
        exgdbpath = os.environ.get("EXGDBPATH")
        if log_filename == None:
            log_filename = exgdbpath + "/.cache/memtrace.tmp"
        f_log = File(log_filename)
        symbol_memo = "symbol_memo.txt"
        f_symbol_memo = File(symbol_memo)
        if not f_log.exist():
            f_log.create()
        if not f_symbol_memo.exist():
            f_symbol_memo.create()
        pc = e.getreg("pc")
        chain = e.examine_mem_reference(pc, pid=pid)
        text = utils.format_reference_chain(chain)
        asm_str = r_asmStr.findall(text)
        if len(asm_str) > 0:
            asm_str = asm_str[0]
        else:
            print("error")
            return -1
        if asm_str[0] == "<":
            asm_str = r_asmStr_2.findall(asm_str)
            if len(asm_str) > 0:
                asm_str = asm_str[0]
        asm_str = r_asmStr_3.findall(asm_str)
        arg1 = ""
        arg2 = ""
        if len(asm_str) > 0:
            asm_op = asm_str[0][0]
            asm_args = asm_str[0][1]
            asm_arg1_arg2 = r_args.findall(asm_args)
            if asm_arg1_arg2 == []:
                arg1 = asm_args
            if len(asm_arg1_arg2) > 0:
                (arg1, arg2) = asm_arg1_arg2[0]
            if asm_args == "":
                one_log = hex(pc) + "!" + asm_op
            else:
                one_log = hex(pc) + "!" + asm_op + " "
        else:
            print("error")
            return -1

        # TEST CASE
        #asm_op = "cmp"
        #arg1 = "rax"
        #arg2 = "DWORD PTR [eip+0x20093a]"

        try:
            # asm_op convert
            if asm_op == "mov":
                if arg1 in regs:
                    asm_op += "_reg"
                elif "PTR" in arg1:
                    asm_op += "_ptr"
                else:
                    asm_op += "_imm"
                if arg2 in regs:
                    asm_op += "_reg"
                elif "PTR" in arg2:
                    asm_op += "_ptr"
                else:
                    asm_op += "_imm"
            elif asm_op == "add":
                if arg1 in regs:
                    asm_op += "_reg"
                elif "PTR" in arg1:
                    asm_op += "_ptr"
                else:
                    asm_op += "_imm"
                if arg2 in regs:
                    asm_op += "_reg"
                elif "PTR" in arg2:
                    asm_op += "_ptr"
                else:
                    asm_op += "_imm"
            elif asm_op == "sub":
                if arg1 in regs:
                    asm_op += "_reg"
                elif "PTR" in arg1:
                    asm_op += "_ptr"
                else:
                    asm_op += "_imm"
                if arg2 in regs:
                    asm_op += "_reg"
                elif "PTR" in arg2:
                    asm_op += "_ptr"
                else:
                    asm_op += "_imm"

            text = asm_ops[asm_op]

            (arg1, arg1_data, arg1_reg, arg1_reg_data, b, appending_one_log) = \
                e.parse_arg(arg1, text, f_log, f_symbol_memo)
            one_log += appending_one_log
            (arg2, arg2_data, arg2_reg, arg2_reg_data, b, appending_one_log) = \
                e.parse_arg(arg2, text, f_log, f_symbol_memo)
            if appending_one_log != "":
                one_log += "," + appending_one_log

            # uniq args handling for "asm_op"
            if asm_op in asm_ops["mov"].split(":"):
                main_data = e.read_int(int(arg2_data, 0))
                if main_data == None:
                    main_data = "CAN NOT ACCESS MEMORY"
                else:
                    main_data = hex(main_data)
                text = text.replace("main_data", main_data)
            elif asm_op in ["lea"]:
                pass
            elif asm_op in asm_ops["add"].split(":"):
                org_data = e.read_int(int(arg2_data, 0))
                if org_data != None:
                    new_data = int(arg1_data, 0) + org_data
                else:
                    org_data = ""
                    new_data = int(arg1_data, 0) + int(arg2_data, 0)
                new_data = hex(new_data)
                text = text.replace("new_data", new_data)
            elif asm_op in asm_ops["sub"].split(":"):
                new_data = int(arg1_data, 0) - int(arg2_data, 0)
                new_data = hex(new_data)
                text = text.replace("new_data", new_data)
            elif asm_op == "push":
                text = asm_ops[asm_op]
                (arch, bits) = e.getarch()
                if bits == 64:
                    sp_addr = e.getreg("rsp")
                else:
                    sp_addr = e.getreg("esp")
                capsize = bits / 8
                new_sp_addr = int(sp_addr - capsize)
                new_sp_addr = hex(new_sp_addr)
                sp_addr = hex(sp_addr)
                text = text.replace("new_sp_addr", new_sp_addr)
                text = text.replace("sp_addr", sp_addr)
                text = text.replace("arg1_data", arg1_data)
            elif asm_op == "ret":
                text = asm_ops[asm_op]
                (arch, bits) = e.getarch()
                if bits == 64:
                    sp_addr = e.getreg("rsp")
                else:
                    sp_addr = e.getreg("esp")
                capsize = bits / 8
                new_sp_addr = int(sp_addr + capsize)
                sp_data = e.read_int(sp_addr)
                sp_addr = hex(sp_addr)
                new_sp_addr = hex(new_sp_addr)
                sp_data = hex(sp_data)
                text = text.replace("new_sp_addr", new_sp_addr)
                text = text.replace("sp_addr", sp_addr)
                text = text.replace("sp_data", sp_data)
            elif asm_op == "leave":
                text = asm_ops[asm_op]
                (arch, bits) = e.getarch()
                if bits == 64:
                    bp_addr = e.getreg("rbp")
                else:
                    bp_addr = e.getreg("ebp")
                sp_addr = bp_addr
                capsize = bits / 8
                new_sp_addr = int(sp_addr + capsize)
                sp_data = e.read_int(sp_addr)
                sp_addr = hex(sp_addr)
                new_sp_addr = hex(new_sp_addr)
                sp_data = hex(sp_data)
                bp_addr = hex(bp_addr)
                text = text.replace("new_sp_addr", new_sp_addr)
                text = text.replace("sp_addr", sp_addr)
                text = text.replace("sp_data", sp_data)
                text = text.replace("bp_addr", bp_addr)
            elif asm_op == "cmp":
                arg1_data = int(arg1_data, 16)
                arg2_data = int(arg2_data, 16)
                subed = arg1_data - arg2_data
                #of = 0
                sf = 0
                zf = 0
                #af = 0
                #pf = 0
                #cf = 0
                #max_nr = int(2**bits / 2)
                #if subed > max_nr or subed < -1 * max_nr:
                #    of = 1
                if subed < 0:
                    sf = 1
                if subed == 0:
                    zf = 1
                one_log += ",Write[sf]:" + str(sf) + ",Write[zf]:" + str(zf)
            text = text.replace("arg1_reg_data", arg1_reg_data)
            text = text.replace("arg1_reg", arg1_reg)
            text = text.replace("arg2_reg_data", arg2_reg_data)
            text = text.replace("arg2_reg", arg2_reg)
            text = text.replace("arg1_data", arg1_data)
            text = text.replace("arg1", arg1)
            text = text.replace("arg2_data", arg2_data)
            text = text.replace("arg2", arg2)
            # finish
            if text != "":
                one_log += "!" + text
        # unknown asm_op
        except:
            if not asm_op in ["call"]:
                print("not implemented:", repr(asm_op), repr(arg1), repr(arg2))
            if "#" in arg1:
                f_symbol_memo.add(hex(pc) + ": " + arg1 + "\n")
                arg1_before = r_comment_before.sub("", arg1)
                arg1_after = r_comment.sub("", arg1)
                arg1_after = r_comment1.sub("", arg1_after)
                arg1 = arg1_before
                arg1 += "["
                arg1 += arg1_after
                arg1 += "]"
            if "#" in arg2:
                f_symbol_memo.add(hex(pc) + ": " + arg2 + "\n")
                arg2_before = r_comment_before.sub("", arg2)
                arg2_after = r_comment.sub("", arg2)
                arg2_after = r_comment2.sub("", arg2_after)
                arg2 = arg2_before
                arg2 += "["
                arg2 += arg2_after
                arg2 += "]"
            if arg1 != "":
                one_log += arg1
                if arg2 != "":
                    one_log += "," + arg2
        f_log.add(one_log + "\n")
        if log_filename == exgdbpath + "/.cache/memtrace.tmp":
            one_log = one_log.split("!")[2]
            print(one_log)

    def autosavemode(self, *arg):
        """
        set autosave option
        """
        (mode, ) = utils.normalize_argv(arg, 1)
        config.Option.set("autosave", mode)

