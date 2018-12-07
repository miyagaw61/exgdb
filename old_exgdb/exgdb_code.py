
#----add by me----#

    def my_normalize_argv(args, size=0):
        """
        Normalize argv to list with predefined length
        """
        args = list(args)
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

    def str_normalize_argv(args, size=0):
        """
        Normalize argv to list with predefined length
        """
        args = list(args)
        for (idx, val) in enumerate(args):
           if size and idx == size:
                return args[:idx]

        if size == 0:
            return args
        for i in range(len(args), size):
            args += [None]
        return args

    def flg(self,*arg):
        """
        hogehoge
        """
        peda.execute('xinfo register eflags')
        return

    def pc(self,*arg):
        """
        hogehoge
        """
        arch = getarch()
        #(arg, ) = normalize_argv(arg,1)
        arg = arg[0]
        argstr = str(arg)
        if(arch == "x86-64"):
            peda.execute('pdisas $rip /%s' % gdb.parse_and_eval(argstr))
        else:
            peda.execute('pdisas $eip /%s' % gdb.parse_and_eval(argstr))
        return

    def lpout(self,*arg):
        """
        hogehoge
        """
        arch = getarch()
        if(arch == "x86-64"):
            peda.execute('n $rcx')
        else:
            peda.execute('n $ecx')
        return

    def allstack(self,*arg):
        """
        hogehoge
        """
        arch = getarch()
        if(arch == "x86-64"):
            sp = peda.getreg('rsp')
            bp = peda.getreg('rbp')
        else:
            sp = peda.getreg('esp')
            bp = peda.getreg('ebp')
        arg = bp - sp
        arg = arg/4
        arg += 1
        arg = int(arg)
        peda.execute('stack %s' % arg)
        return
    
    def xgrep(self,*arg):
        """
        hogehoge
        """
        cmd = arg[0]
        arg1 = arg[1]
        regex_arg = re.compile(r".*" + arg1 + ".*")
        regex_num = re.compile(r"^\d*:")
        out = gdb.execute(cmd, to_string=True)
        if(os.path.exists("peda-out.tmp")):
            os.system("rm -rf peda-out.tmp")
        fd = open("peda-out-color.tmp", "w")
        fd.write(out)
        fd.close()
        #gdb.execute("shell wcat peda-out-color.tmp > peda-out-noncolor.tmp")
        f = fl("peda-out-color.tmp")
        white_data = fl("peda-out-color.tmp").white_data()
        fl("peda-out-noncolor.tmp").write(white_data)
        gdb.execute("shell cp -a peda-out-noncolor.tmp peda-out.tmp")
        out = open("peda-out.tmp", "r").read()
        res = regex_arg.findall(out)
        regex_tmp1 = re.compile(r"\[")
        regex_tmp2 = re.compile(r"\]")
        for i in range(len(res)):
            #os.system("cat peda-out-noncolor.tmp | grep -n \"" + res[i] + "\" > peda-one.tmp")
            tmp = regex_tmp1.sub("\\\[", res[i])
            tmp = regex_tmp2.sub("\\\]", tmp)
            gdb.execute("shell cat peda-out-noncolor.tmp | grep -n \"" + tmp + "\" > peda-one.tmp")
            num = open("peda-one.tmp", "r").read()
            num = regex_num.findall(num)[0][0:-1]
            gdb.execute("shell head -n " + num + " peda-out-color.tmp | tail -n 1")
            #os.system("head -n " + num + " peda-out-color.tmp | tail -n 1 > peda-res.tmp")
            #ans = open("peda-res.tmp", "r").read()
            #sys.stdout.write(ans)
        if(os.path.exists("peda-out-color.tmp")):
            os.system("rm -rf peda-out-color.tmp")
        if(os.path.exists("peda-out.tmp")):
            os.system("rm -rf peda-out.tmp")
        if(os.path.exists("peda-one.tmp")):
            os.system("rm -rf peda-one.tmp")
        #if(os.path.exists("peda-res.tmp")):
        #    os.system("rm -rf peda-res.tmp")
        return
    
    def infox(self, *arg):
        """
        Display detail information of address/registers
        Usage:
            MYNAME address
            MYNAME register [reg1 reg2]
        """

        (address, regname) = normalize_argv(arg, 2)
        if address is None:
            self._missing_argument()

        text = ""
        if not self._is_running():
            return


        def get_reg_text(r, v):
            text = green("%s" % r.upper().ljust(3)) + ": "
            chain = peda.examine_mem_reference(v)
            text += format_reference_chain(chain)
            text += "\n"
            return text

        (arch, bits) = peda.getarch()
        if str(address).startswith("r"):
            # Register
            regs = peda.getregs(" ".join(arg[1:]))
            if regname is None:
                for r in REGISTERS[bits]:
                    if r in regs:
                        text += get_reg_text(r, regs[r])
            else:
                for (r, v) in sorted(regs.items()):
                    text += get_reg_text(r, v)
            if text:
                msg(text.strip())
            if regname is None or "eflags" in regname:
                self.eflags()
            return

        elif to_int(address) is None:
            warning_msg("not a register nor an address")
        else:
            # Address
            chain = peda.examine_mem_reference(address)
            #text += '\n'
            #text += 'info: '
            text += format_reference_chain(chain) # + "\n"
            vmrange = peda.get_vmrange(address)
            if vmrange:
                (start, end, perm, name) = vmrange
        msg(text)
        return

    def tel(self, *arg):
        """
        Usage:
            ix [address] [count]
        """
        if(len(arg) == 1):
            (address,) = normalize_argv(arg, 1)
            peda.execute("telescope " + str(address) + " 1")
        if(len(arg) == 2):
            (address, count) = normalize_argv(arg, 2)
            peda.execute("telescope " + str(address) + " " + str(count))

#    def infox_ip(self, *arg):
#        """
#        Display detail information of address/registers
#        Usage:
#            MYNAME address
#            MYNAME register [reg1 reg2]
#        """
#
#        (address, filename) = normalize_argv(arg, 2)
#        regname = address
#        if address is None:
#            self._missing_argument()
#
#        text = ""
#        if not self._is_running():
#            return
#
#
#        def get_reg_text(r, v):
#            text = green("%s" % r.upper().ljust(3)) + ": "
#            chain = peda.examine_mem_reference(v)
#            text += format_reference_chain(chain)
#            text += "\n"
#            return text
#
#        (arch, bits) = peda.getarch()
#        if str(address).startswith("r"):
#            # Register
#            regs = peda.getregs(" ".join(arg[1:]))
#            if regname is None:
#                for r in REGISTERS[bits]:
#                    if r in regs:
#                        text += get_reg_text(r, regs[r])
#            else:
#                for (r, v) in sorted(regs.items()):
#                    text += get_reg_text(r, v)
#            if text:
#                msg(text.strip())
#            if regname is None or "eflags" in regname:
#                self.eflags()
#            return
#
#        elif to_int(address) is None:
#            warning_msg("not a register nor an address")
#        else:
#            # Address
#            chain = peda.examine_mem_reference(address, depth=0)
#            #text += '\n'
#            #text += 'info: '
#            text += format_reference_chain(chain) # + "\n"
#            vmrange = peda.get_vmrange(address)
#            if vmrange:
#                (start, end, perm, name) = vmrange
#        #msg(text)
#        os.system('echo ' + '"' + text + '"' + ' >> ./reg/' + filename)
#        os.system('cat ./reg/' + filename + ' | tail -1 > ./reg/' + filename + '.tmp')
#
#    def infox_reg(self, *arg):
#        """
#        Display detail information of address/registers
#        Usage:
#            MYNAME address
#            MYNAME register [reg1 reg2]
#        """
#
#        (address, filename) = normalize_argv(arg, 2)
#        regname = address
#        if address is None:
#            self._missing_argument()
#
#        text = ""
#        if not self._is_running():
#            return
#
#
#        def get_reg_text(r, v):
#            text = green("%s" % r.upper().ljust(3)) + ": "
#            chain = peda.examine_mem_reference(v)
#            text += format_reference_chain(chain)
#            text += "\n"
#            return text
#
#        (arch, bits) = peda.getarch()
#        if str(address).startswith("r"):
#            # Register
#            regs = peda.getregs(" ".join(arg[1:]))
#            if regname is None:
#                for r in REGISTERS[bits]:
#                    if r in regs:
#                        text += get_reg_text(r, regs[r])
#            else:
#                for (r, v) in sorted(regs.items()):
#                    text += get_reg_text(r, v)
#            if text:
#                msg(text.strip())
#            if regname is None or "eflags" in regname:
#                self.eflags()
#            return
#
#        elif to_int(address) is None:
#            warning_msg("not a register nor an address")
#        else:
#            # Address
#            chain = peda.examine_mem_reference(address, depth=0)
#            #text += '\n'
#            #text += 'info: '
#            text += format_reference_chain(chain) # + "\n"
#            vmrange = peda.get_vmrange(address)
#            if vmrange:
#                (start, end, perm, name) = vmrange
#        #msg(text)
#        prev = open('./reg/' + filename + '.tmp', 'r').read()
#        if(prev != text+'\n'):
#            peda.execute('infox_ip $rip rip')
#            os.system('cat ./reg/rip.tmp >> ./reg/' + filename)
#            os.system('echo ' + '"' + text + '"' + '>> ./reg/' + filename)
#            os.system('cat ./reg/' + filename + ' | tail -1 > ' + './reg/' + filename + '.tmp')
#        return
#
    def regmake(self, *arg):
        """
        Usage: regmake
        """
        arch = getarch()
        os.system('mkdir reg')
        if(arch == "x86-64"):
            peda.execute('infox_new register rax')
            peda.execute('infox_new register rbx')
            peda.execute('infox_new register rcx')
            peda.execute('infox_new register rdx')
            peda.execute('infox_new register rsi')
            peda.execute('infox_new register rdi')
            peda.execute('infox_new register rbp')
            peda.execute('infox_new register rsp')
            peda.execute('infox_new register rip')
        else:
            peda.execute('infox_new register eax')
            peda.execute('infox_new register ebx')
            peda.execute('infox_new register ecx')
            peda.execute('infox_new register edx')
            peda.execute('infox_new register esi')
            peda.execute('infox_new register edi')
            peda.execute('infox_new register ebp')
            peda.execute('infox_new register esp')
            peda.execute('infox_new register eip')

    def code(self, *arg):
        """
        hogehoge
        """
        arch = getarch()
        arg = normalize_argv(arg,2)
        arg0 = arg[0]
        arg1 = arg[1]
        arg1str = str(arg1)
        if(arch == "x86-64"):
            ripbk = peda.getreg('rip')
            peda.execute('set $rip=%d' % arg0)
            peda.execute('pc %d' % arg1)
            peda.execute('set $rip=%d' % ripbk)
        else:
            eipbk = peda.getreg('eip')
            peda.execute('set $eip=%d' % arg0)
            peda.execute('pc %d' % arg1)
            peda.execute('set $eip=%d' % eipbk)
        return

    #def dword(self, *arg):
    #    """
    #    hogehoge
    #    """
    #    arg = normalize_argv(arg,2)
    #    addr = arg[0]
    #    i = arg[1]
    #    istr = str(i)
    #    i = gdb.parse_and_eval(istr)
    #    cnt = 0
    #    while(i > 0):
    #        peda.execute('infox %d+%d' % (addr,cnt))
    #        cnt = cnt + 4
    #        i = i - 1

    #def qword(self, *arg):
    #    """
    #    hogehoge
    #    """
    #    arg = normalize_argv(arg,2)
    #    addr = arg[0]
    #    i = arg[1]
    #    istr = str(i)
    #    i = gdb.parse_and_eval(istr)
    #    cnt = 0
    #    while(i > 0):
    #        peda.execute('infox %d+%d' % (addr,cnt))
    #        cnt = cnt + 8
    #        i = i - 1

    def regtrace(self, *arg):
        """
        Usage: regtrace
        """
        arch = getarch()
        arg = normalize_argv(arg,2)
        flag = arg[0]
        file_name = arg[1]
        if(arch == "x86-64"):
            prev_rax = open('./reg/rax', 'r').read()
            prev_rbx = open('./reg/rbx', 'r').read()
            prev_rcx = open('./reg/rcx', 'r').read()
            prev_rdx = open('./reg/rdx', 'r').read()
            prev_rsi = open('./reg/rsi', 'r').read()
            prev_rdi = open('./reg/rdi', 'r').read()
            prev_rbp = open('./reg/rbp', 'r').read()
            prev_rsp = open('./reg/rsp', 'r').read()
            prev_rip = open('./reg/rip', 'r').read()
            peda.execute('infox_new register rax')
            peda.execute('infox_new register rbx')
            peda.execute('infox_new register rcx')
            peda.execute('infox_new register rdx')
            peda.execute('infox_new register rsi')
            peda.execute('infox_new register rdi')
            peda.execute('infox_new register rbp')
            peda.execute('infox_new register rsp')
            peda.execute('infox_new register rip')
            rax = open('./reg/rax', 'r').read()
            rbx = open('./reg/rbx', 'r').read()
            rcx = open('./reg/rcx', 'r').read()
            rdx = open('./reg/rdx', 'r').read()
            rsi = open('./reg/rsi', 'r').read()
            rdi = open('./reg/rdi', 'r').read()
            rbp = open('./reg/rbp', 'r').read()
            rsp = open('./reg/rsp', 'r').read()
            rip = open('./reg/rip', 'r').read()
            prev_rip = re.sub(r'\n', '', prev_rip)
            prev_rip = re.sub(r'.*: ', '', prev_rip)
            os.system('echo "\n' + prev_rip + '" >> ./reg/regtrace')
            if(prev_rax != rax):
                rax = re.sub(r'\n', '', rax)
                os.system('echo "' + rax + '" >> ./reg/regtrace')
            if(prev_rbx != rbx):
                rbx = re.sub(r'\n', '', rbx)
                os.system('echo "' + rbx + '" >> ./reg/regtrace')
            if(prev_rcx != rcx):
                rcx = re.sub(r'\n', '', rcx)
                os.system('echo "' + rcx + '" >> ./reg/regtrace')
            if(prev_rdx != rdx):
                rdx = re.sub(r'\n', '', rdx)
                os.system('echo "' + rdx + '" >> ./reg/regtrace')
            if(prev_rsi != rsi):
                rsi = re.sub(r'\n', '', rsi)
                os.system('echo "' + rsi + '" >> ./reg/regtrace')
            if(prev_rdi != rdi):
                rdi = re.sub(r'\n', '', rdi)
                os.system('echo "' + rdi + '" >> ./reg/regtrace')
            if(prev_rbp != rbp):
                rbp = re.sub(r'\n', '', rbp)
                os.system('echo "' + rbp + '" >> ./reg/regtrace')
            if(prev_rsp != rsp):
                rsp = re.sub(r'\n', '', rsp)
                os.system('echo "' + rsp + '" >> ./reg/regtrace')
        else:
            prev_eax = open('./reg/eax', 'r').read()
            prev_ebx = open('./reg/ebx', 'r').read()
            prev_ecx = open('./reg/ecx', 'r').read()
            prev_edx = open('./reg/edx', 'r').read()
            prev_esi = open('./reg/esi', 'r').read()
            prev_edi = open('./reg/edi', 'r').read()
            prev_ebp = open('./reg/ebp', 'r').read()
            prev_esp = open('./reg/esp', 'r').read()
            prev_eip = open('./reg/eip', 'r').read()
            peda.execute('infox_new register eax')
            peda.execute('infox_new register ebx')
            peda.execute('infox_new register ecx')
            peda.execute('infox_new register edx')
            peda.execute('infox_new register esi')
            peda.execute('infox_new register edi')
            peda.execute('infox_new register ebp')
            peda.execute('infox_new register esp')
            peda.execute('infox_new register eip')
            eax = open('./reg/eax', 'r').read()
            ebx = open('./reg/ebx', 'r').read()
            ecx = open('./reg/ecx', 'r').read()
            edx = open('./reg/edx', 'r').read()
            esi = open('./reg/esi', 'r').read()
            edi = open('./reg/edi', 'r').read()
            ebp = open('./reg/ebp', 'r').read()
            esp = open('./reg/esp', 'r').read()
            eip = open('./reg/eip', 'r').read()
            prev_eip = re.sub(r'\n', '', prev_eip)
            prev_eip = re.sub(r'.*: ', '', prev_eip)
            os.system('echo "\n' + prev_eip + '" >> ./reg/regtrace')
            if(prev_eax != eax):
                eax = re.sub(r'\n', '', eax)
                os.system('echo "' + eax + '" >> ./reg/regtrace')
            if(prev_ebx != ebx):
                ebx = re.sub(r'\n', '', ebx)
                os.system('echo "' + ebx + '" >> ./reg/regtrace')
            if(prev_ecx != ecx):
                ecx = re.sub(r'\n', '', ecx)
                os.system('echo "' + ecx + '" >> ./reg/regtrace')
            if(prev_edx != edx):
                edx = re.sub(r'\n', '', edx)
                os.system('echo "' + edx + '" >> ./reg/regtrace')
            if(prev_esi != esi):
                esi = re.sub(r'\n', '', esi)
                os.system('echo "' + esi + '" >> ./reg/regtrace')
            if(prev_edi != edi):
                edi = re.sub(r'\n', '', edi)
                os.system('echo "' + edi + '" >> ./reg/regtrace')
            if(prev_ebp != ebp):
                ebp = re.sub(r'\n', '', ebp)
                os.system('echo "' + ebp + '" >> ./reg/regtrace')
            if(prev_esp != esp):
                esp = re.sub(r'\n', '', esp)
                os.system('echo "' + esp + '" >> ./reg/regtrace')
        peda.execute('n')
        
    def infox_new(self, *arg):
        """
        Display detail information of address/registers
        Usage:
            MYNAME address
            MYNAME register [reg1 reg2]
        """

        (address, regname) = normalize_argv(arg, 2)
        if address is None:
            self._missing_argument()

        text = ""
        if not self._is_running():
            return

        def get_reg_text(r, v):
            text = green("%s" % r.upper().ljust(3)) + ": "
            chain = peda.examine_mem_reference(v)
            text += format_reference_chain(chain)
            tmp = re.sub(r'\n', '', text)
            os.system('echo ' + '"' + text + '"' + ' > ./reg/' + regname)
            return text

        (arch, bits) = peda.getarch()
        if str(address).startswith("r"):
            # Register
            regs = peda.getregs(" ".join(arg[1:]))
            if regname is None:
                for r in REGISTERS[bits]:
                    if r in regs:
                        text += get_reg_text(r, regs[r])
            else:
                for (r, v) in sorted(regs.items()):
                    text += get_reg_text(r, v)
            if text:
                #msg(text.strip())
                a = 'a'
            if regname is None or "eflags" in regname:
                self.eflags()
            return

        elif to_int(address) is None:
            warning_msg("not a register nor an address")
        else:
            # Address
            chain = peda.examine_mem_reference(address, depth=0)
            text += format_reference_chain(chain) + "\n"
            vmrange = peda.get_vmrange(address)
            if vmrange:
                (start, end, perm, name) = vmrange
                text += "Virtual memory mapping:\n"
                text += green("Start : %s\n" % to_address(start))
                text += green("End   : %s\n" % to_address(end))
                text += yellow("Offset: 0x%x\n" % (address-start))
                text += red("Perm  : %s\n" % perm)
                text += blue("Name  : %s" % name)
        #msg(text)

        return

    def uc(self, *arg):
        """
        stop.
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(argc == 1):
            #(arg, ) = normalize_argv(arg,1)
            arg = arg[0]
            if(arch == "x86-64"):
                while(True):
                    peda.execute('nextcall')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg + '.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                while(True):
                    peda.execute('nextcall')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg + '.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
        elif(argc == 2):
            #(arg1, arg2) = normalize_argv(arg, 2)
            arg1 = arg[0]
            arg2 = arg[1]
            i = 0
            if(arch == "X86-64"):
                while(i < arg2):
                    peda.execute('nextcall')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg1 + '.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
            else:
                while(i < arg2):
                    peda.execute('nextcall')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg1 + '.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def uu(self, *arg):
        """
        stop.
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(arch == "x86-64"):
            if(argc == 1):
                #(arg, ) = normalize_argv(arg,1)
                arg = arg[0]
                while(True):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg + '.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            elif(argc == 2):
                #(arg1, arg2, ) = normalize_argv(arg, 2)
                arg1 = arg[0]
                arg2 = arg[1]
                i = 0
                while(i < arg2):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg1 + '.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
        else:
            if(argc == 1):
                #(arg, ) = normalize_argv(arg,1)
                arg = arg[0]
                while(True):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg + '.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
            elif(argc == 2):
                #(arg1, arg2, ) = normalize_argv(arg, 2)
                arg1 = arg[0]
                arg2 = arg[1]
                i = 0
                while(i < arg2):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg1 + '.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def uui(self, *arg):
        """
        stop.
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(arch == "x86-64"):
            if(argc == 1):
                #(arg, ) = normalize_argv(arg,1)
                arg = arg[0]
                while(True):
                    peda.execute('si')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg + '.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            elif(argc == 2):
                #(arg1, arg2) = normalize_argv(arg, 2)
                arg1 = arg[0]
                arg2 = arg[1]
                i = 0
                while(i < arg2):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg1 + '.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
        else:
            if(argc == 1):
                #(arg, ) = normalize_argv(arg,1)
                arg = arg[0]
                while(True):
                    peda.execute('si')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg + '.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
            elif(argc == 2):
                #(arg1, arg2) = normalize_argv(arg, 2)
                arg1 = arg[0]
                arg2 = arg[1]
                i = 0
                while(i < arg2):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*' + arg1 + '.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def cc(self, *arg):
        """
        Usage: cc
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(arch == "x86-64"):
            if(argc != 1):
                while(True):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
        else:
            if(argc != 1):
                while(True):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def cci(self, *arg):
        """
        Usage: cc
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(arch == "x86-64"):
            if(argc != 1):
                while(True):
                    peda.execute('si')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('si')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
        else:
            if(argc != 1):
                while(True):
                    peda.execute('si')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('si')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*call.*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def jj(self, *arg):
        """
        Usage: jj
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(arch == "x86-64"):
            if(argc != 1):
                while(True):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('ni')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
        else:
            if(argc != 1):
                while(True):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('ni')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def jji(self, *arg):
        """
        Usage: jj
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        argc = len(arg)
        if(arch == "x86-64"):
            if(argc != 1):
                while(True):
                    peda.execute('si')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('si')
                    peda.execute('infox_new register rip')
                    rip = open('./reg/rip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', rip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1
        else:
            if(argc != 1):
                while(True):
                    peda.execute('si')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        break
            else:
                #(arg1, ) = normalize_argv(arg, 1)
                arg1 = arg[0]
                i = 0
                while(i < arg1):
                    peda.execute('si')
                    peda.execute('infox_new register eip')
                    eip = open('./reg/eip', 'r').read()
                    callOrJmp = re.sub(r'.*(call|jmp|je|jne|jb|ja).*', '', eip)
                    if(callOrJmp.find(':') == -1):
                        i = i + 1

    def ii(self, *arg):
        """
        Usage: ii
        """
        if not (os.path.exists("reg")):
           gdb.execute("regmake") 
        arch = getarch()
        if(arch == "x86-64"):
            peda.execute('infox_new register rip')
            nowrip = open('./reg/rip', 'r').read()
            #beforeRegisterX = re.sub(r'.*(r.x).*.*', '\\1', nowrip)
            #beforeRegisterP = re.sub(r'.*(r.p).*.*', '\\1', nowrip)
            #beforeRegisterI = re.sub(r'.*(r.i).*.*', '\\1', nowrip)
            rax = re.sub(r'.*(rax).*', '\\1', nowrip)
            rbx = re.sub(r'.*(rbx).*', '\\1', nowrip)
            rcx = re.sub(r'.*(rcx).*', '\\1', nowrip)
            rdx = re.sub(r'.*(rdx).*', '\\1', nowrip)
            rsi = re.sub(r'.*(rsi).*', '\\1', nowrip)
            rdi = re.sub(r'.*(rdi).*', '\\1', nowrip)
            rbp = re.sub(r'.*(rbp).*', '\\1', nowrip)
            rsp = re.sub(r'.*(rsp).*', '\\1', nowrip)
            rip = re.sub(r'.*(rip).*', '\\1', nowrip)
            r8 = re.sub(r'.*(r8).*', '\\1', nowrip)
            r9 = re.sub(r'.*(r9).*', '\\1', nowrip)
            r10 = re.sub(r'.*(r10).*', '\\1', nowrip)
            r11 = re.sub(r'.*(r11).*', '\\1', nowrip)
            r12 = re.sub(r'.*(r12).*', '\\1', nowrip)
            r13 = re.sub(r'.*(r13).*', '\\1', nowrip)
            r14 = re.sub(r'.*(r14).*', '\\1', nowrip)
            r15 = re.sub(r'.*(r15).*', '\\1', nowrip)
            eax = re.sub(r'.*(eax).*', '\\1', nowrip)
            ebx = re.sub(r'.*(ebx).*', '\\1', nowrip)
            ecx = re.sub(r'.*(ecx).*', '\\1', nowrip)
            edx = re.sub(r'.*(edx).*', '\\1', nowrip)
            esi = re.sub(r'.*(esi).*', '\\1', nowrip)
            edi = re.sub(r'.*(edi).*', '\\1', nowrip)
            ebp = re.sub(r'.*(ebp).*', '\\1', nowrip)
            esp = re.sub(r'.*(esp).*', '\\1', nowrip)
            eip = re.sub(r'.*(eip).*', '\\1', nowrip)
            #afterRegisterX = re.sub(r'.*,.*(r.x).*', '\\1', nowrip)
            #afterRegisterP = re.sub(r'.*,.*(r.p).*', '\\1', nowrip)
            #afterRegisterI = re.sub(r'.*,.*(r.i).*', '\\1', nowrip)
            inregister = re.sub(r'.*(\[.*\]).*', '\\1', nowrip)
            #registerInregister = re.sub(r'.*\[.*(r..).*\].*', '\\1', nowrip)
            addr = re.sub(r'.*0x.*(0x[0-9a-f][0-9a-f][0-9a-f][0-9a-f]+).*', '\\1', nowrip)
            if(rax.find(':') == -1):
                peda.execute('xinfo register ' + rax)
            if(rbx.find(':') == -1):
                peda.execute('xinfo register ' + rbx)
            if(rcx.find(':') == -1):
                peda.execute('xinfo register ' + rcx)
            if(rdx.find(':') == -1):
                peda.execute('xinfo register ' + rdx)
            if(rsi.find(':') == -1):
                peda.execute('xinfo register ' + rsi)
            if(rdi.find(':') == -1):
                peda.execute('xinfo register ' + rdi)
            if(rbp.find(':') == -1):
                peda.execute('xinfo register ' + rbp)
            if(rsp.find(':') == -1):
                peda.execute('xinfo register ' + rsp)
            if(rip.find(':') == -1):
                peda.execute('xinfo register ' + rip)
            if(r8.find(':') == -1):
                peda.execute('xinfo register ' + r8)
            if(r9.find(':') == -1):
                peda.execute('xinfo register ' + r9)
            if(r10.find(':') == -1):
                peda.execute('xinfo register ' + r10)
            if(r11.find(':') == -1):
                peda.execute('xinfo register ' + r11)
            if(r12.find(':') == -1):
                peda.execute('xinfo register ' + r12)
            if(r13.find(':') == -1):
                peda.execute('xinfo register ' + r13)
            if(r14.find(':') == -1):
                peda.execute('xinfo register ' + r14)
            if(r15.find(':') == -1):
                peda.execute('xinfo register ' + r15)
            if(eax.find(':') == -1):
                peda.execute('xinfo register ' + eax)
            if(ebx.find(':') == -1):
                peda.execute('xinfo register ' + ebx)
            if(ecx.find(':') == -1):
                peda.execute('xinfo register ' + ecx)
            if(edx.find(':') == -1):
                peda.execute('xinfo register ' + edx)
            if(esi.find(':') == -1):
                peda.execute('xinfo register ' + esi)
            if(edi.find(':') == -1):
                peda.execute('xinfo register ' + edi)
            if(ebp.find(':') == -1):
                peda.execute('xinfo register ' + ebp)
            if(esp.find(':') == -1):
                peda.execute('xinfo register ' + esp)
            if(eip.find(':') == -1):
                peda.execute('xinfo register ' + eip)
            if(addr.find(':') == -1):
                peda.execute('infox ' + addr)
            if(inregister.find(':') == -1):
                after = re.sub(r'\n', '', inregister)
                peda.execute("shell echo -n -e '\e[32m" + after + "\e[m: '")
                after = re.sub(r'\[(r..*)\].*', '$\\1', after)
                after2 = re.sub(r'\[(e..*)\].*', '$\\1', after)
                if(len(after) < len(after2)):
                    after = after2
                peda.execute('infox ' + after)
            return
        else:
            peda.execute('infox_new register eip')
            noweip = open('./reg/eip', 'r').read()
            #beforeRegisterX = re.sub(r'.*(e.x).*.*', '\\1', noweip)
            #beforeRegisterP = re.sub(r'.*(e.p).*.*', '\\1', noweip)
            #beforeRegisterI = re.sub(r'.*(e.i).*.*', '\\1', noweip)
            eax = re.sub(r'.*(eax).*', '\\1', noweip)
            ebx = re.sub(r'.*(ebx).*', '\\1', noweip)
            ecx = re.sub(r'.*(ecx).*', '\\1', noweip)
            edx = re.sub(r'.*(edx).*', '\\1', noweip)
            esi = re.sub(r'.*(esi).*', '\\1', noweip)
            edi = re.sub(r'.*(edi).*', '\\1', noweip)
            ebp = re.sub(r'.*(ebp).*', '\\1', noweip)
            esp = re.sub(r'.*(esp).*', '\\1', noweip)
            eip = re.sub(r'.*(eip).*', '\\1', noweip)
            #afterRegisterX = re.sub(r'.*,.*(e.x).*', '\\1', noweip)
            #afterRegisterP = re.sub(r'.*,.*(e.p).*', '\\1', noweip)
            #afterRegisterI = re.sub(r'.*,.*(e.i).*', '\\1', noweip)
            inregister = re.sub(r'.*(\[.*\]).*', '\\1', noweip)
            #registerInregister = re.sub(r'.*\[.*(e..).*\].*', '\\1', noweip)
            addr = re.sub(r'.*0x.*(0x[0-9a-f][0-9a-f][0-9a-f][0-9a-f]+).*', '\\1', noweip)
            #if(beforeRegisterX.find(':') == -1):
            #    peda.execute('xinfo register ' + beforeRegisterX)
            #if(beforeRegisterP.find(':') == -1):
            #    peda.execute('xinfo register ' + beforeRegisterP)
            #if(beforeRegisterI.find(':') == -1):
            #    peda.execute('xinfo register ' + beforeRegisterI)
            if(eax.find(':') == -1):
                peda.execute('xinfo register ' + eax)
            if(ebx.find(':') == -1):
                peda.execute('xinfo register ' + ebx)
            if(ecx.find(':') == -1):
                peda.execute('xinfo register ' + ecx)
            if(edx.find(':') == -1):
                peda.execute('xinfo register ' + edx)
            if(esi.find(':') == -1):
                peda.execute('xinfo register ' + esi)
            if(edi.find(':') == -1):
                peda.execute('xinfo register ' + edi)
            if(ebp.find(':') == -1):
                peda.execute('xinfo register ' + ebp)
            if(esp.find(':') == -1):
                peda.execute('xinfo register ' + esp)
            if(eip.find(':') == -1):
                peda.execute('xinfo register ' + eip)
            #if(afterRegisterX.find(':') == -1):
            #    peda.execute('xinfo register ' + afterRegisterX)
            #if(afterRegisterP.find(':') == -1):
            #    peda.execute('xinfo register ' + afterRegisterP)
            #if(afterRegisterI.find(':') == -1):
            #    peda.execute('xinfo register ' + afterRegisterI)
            #if(registerInregister.find(':') == -1):
            #    peda.execute('xinfo register ' + registerInregister)
            if(addr.find(':') == -1):
                peda.execute('infox ' + addr)
            if(inregister.find(':') == -1):
                after = re.sub(r'\n', '', inregister)
                peda.execute("shell echo -n -e '\e[32m" + after + "\e[m: '")
                after = re.sub(r'\[(e..*)\].*', '$\\1', after)
                peda.execute('infox ' + after)
            return

    def kdbg(self, *arg):
        """
        Usage: kerneldbg [tty]
        """
        arg = arg[0]
        gdb.execute("file vmlinux")
        gdb.execute("target remote /dev/pts/" + str(arg))
        return

    def dtel(self, *arg):
        """
        Display memory content at an address with smart dereferences
        Usage:
            MYNAME [linecount] (analyze at current $SP)
            MYNAME address [linecount]
        """

        (address, count) = normalize_argv(arg, 2)

        if(1==1):
            sp = peda.getreg("sp")
        else:
            sp = None

        if count is None:
            count = 8
            if address is None:
                address = sp
            elif address < 0x1000:
                count = address
                address = sp

        if not address:
            return

        step = peda.intsize()*2
        if not peda.is_address(address): # cannot determine address
            for i in range(count):
                if not peda.execute("x/%sx 0x%x" % ("g" if step == 8 else "w", address + i*step)):
                    break
            return

        result = []
        for i in range(count):
            value = address + i*step
            if peda.is_address(value):
                result += [peda.examine_mem_reference(value)]
            else:
                result += [None]
        idx = 0
        text = ""
        for chain in result:
            text += "%04d| " % (idx)
            text += format_reference_chain(chain)
            text += "\n"
            idx += step

        pager(text)

        return

    def nii(self, *arg):
        """
        Usage: ii
        """
        gdb.execute("nexti")
        gdb.execute("ii")

###--------added by me--------------------------------###


