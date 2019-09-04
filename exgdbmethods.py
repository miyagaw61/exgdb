class ExgdbMethods():
    def get_infox_text(self, *arg, color=None):
        """
        Customized xinfo command from https://github.com/longld/peda
        Usage:
            MYNAME address
            MYNAME register [reg1 reg2]
        """

        (address, regname) = utils.normalize_argv(arg, 2)
        if address is None:
            pedacmd._missing_argument()

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
                e.eflags()
            return

        elif utils.to_int(address) is None:
            print("not a register nor an address")
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
        value = e.readmem(address, intsize)
        if value:
            value = codecs.encode(value[::-1], 'hex')
            value = value.decode("utf-8")
            value = "0x" + value
            value = utils.to_int(value)
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
            intsize = e.intsize()
        value = e.readmem(address, intsize)
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
            intsize = e.intsize()
        value = e.read_int_bytes(address)[0]
        if value == 0:
            return 0
        if value:
            return value
        else:
            return None

    def read_bytes(self, addr, n):
        capsize = e.intsize()
        loopcnt = int(n/capsize)
        rem = n % capsize
        bytes_list = []
        for i in range(loopcnt):
            for x in e.read_int_bytes(addr+capsize*i):
                bytes_list.append(x)
        if rem == 0:
            return bytes_list
        for i in range(rem):
            byte = e.read_byte(addr+i)
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
        try:
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
        except:
            return None
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
        return {'next': chunkaddr + aligned_size, 'prev_size': prev_size, 'aligned_size': aligned_size, 'nextsize': nextsize, 'used_flag': used_flag, 'fast_flag': fast_flag, 'size': showsize, 'NM': NM, 'IM': IM, 'PI': PI, 'fd': fd, 'bk': bk}

    def getchunklist(self):
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

    def get_addrs_by_regex(self, regex):
        fname = e.getfile()
        cmd = "objdump -M intel -D " + fname + " | grep -E '" + regex + "' | grep -o -E '^ [0-9a-f]+'"
        lines = Shell(cmd).readlines()[0]
        if lines == []:
            return lines
        addrs = []
        for line in lines:
            line = "0x" + line[1:]
            addrs.append(int(line, 16))
        return addrs
