class ExgdbMethods():
    def get_infox_text(self, address, regname=None, color=None):
        """
        Customized xinfo command from https://github.com/longld/peda
        Usage:
            MYNAME address
            MYNAME register [reg1 reg2]
        """
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

    def readmem(self, address, size):
        """
        Customized readmem from https://github.com/longld/peda

        Args:
            - address: start address to read (Int)
            - size: bytes to read (Int)

        Returns:
            - memory content (raw bytes)
        """
        # try fast dumpmem if it works
        mem = self.dumpmem(address, address+size)
        if mem is not None:
            return mem

        # failed to dump, use slow x/gx way
        mem = ""
        try:
            cmd = "x/%dbx 0x%x" % (size, address)
            out = gdb.execute(cmd, to_string=True)
        except:
            return None
        if out:
            for line in out.splitlines():
                bytes = line.split(":\t")[-1].split()
                mem += "".join([chr(int(c, 0)) for c in bytes])

        return mem

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
            return [0]*intsize
        if value:
            byte_list = bin2ints(value)
            return byte_list
        else:
            return None

    def read_byte(self, address):
        """
        Read one byte

        Args:
            - address: address to read (Int)
            - intsize: force read size (Int)

        Returns:
            - one byte data (Int)
        """
        value = e.read_int_bytes(address)[0]
        if value == 0:
            return 0
        if value:
            return value
        else:
            return None

    def read_bytes(self, address, n):
        capsize = e.intsize()
        loopcnt = int(n/capsize)
        rem = n % capsize
        bytes_list = []
        for i in range(loopcnt):
            for x in e.read_int_bytes(address+capsize*i):
                bytes_list.append(x)
        if rem == 0:
            return bytes_list
        for i in range(rem):
            byte = e.read_byte(address+i)
            bytes_list.append(byte)
        return bytes_list

    def getchunkinfo(self, victim, showsize=None):
        global fastchunk
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
        return {'next': chunkaddr + aligned_size, 'prev_size': prev_size, 'aligned_size': aligned_size, 'nextsize': nextsize, 'used_flag': used_flag, 'fast_flag': fast_flag, 'size': size, 'showsize': showsize, 'NM': NM, 'IM': IM, 'PI': PI, 'fd': fd, 'bk': bk}

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

    def get_addrs_by_regex(self, regex, start_addr=None, end_addr=None):
        fpath = e.getfile()

        out, err = Shell("md5sum %s" % fpath).readlines()
        md5sum = 0
        if out != []:
            md5sum = out[0]
            md5sum = md5sum.split()[0]
            md5sum = str(md5sum)
        disass_file = "%s/.cache/%s.disass" % (exgdbpath, md5sum)
        f = File(disass_file)
        if not f.exist():
            codebase, codeend = codeaddr()
            if start_addr == None:
                codebase = start_addr
            if end_addr == None:
                codeend = end_addr
            disass_data = e.disassemble(hex(codebase), hex(codeend))
            print(disass_data)
            f.write(disass_data)
        cmd = "cat " + disass_file + " | grep -E ':.*" + regex + "' | grep -o -E '^ *0x[0-9a-f]+'"
        lines = Shell(cmd).readlines()[0]
        if lines == []:
            return lines
        addrs = []
        for line in lines:
            line = line.split()[0]
            addr = int(line, 16)
            if start_addr == None and end_addr == None:
                addrs.append(addr)
            elif start_addr <= addr <= end_addr:
                addrs.append(addr)
        return addrs

    def to_bytes(self, i, size=None, endian=None):
        if size == None:
            capsize = e.intsize()
            size = capsize
        if endian == None:
            endian = 'little'
        byte_data = i.to_bytes(size, endian)
        bytes_list = list(byte_data)
        return bytes_list

    def is_address(self, value, maps=None, pid=None):
        """
        Customized is_address from https://github.com/longld/peda

        Args:
            - value (Int)
            - maps: only check in provided maps (List)

        Returns:
            - True if value belongs to an address range (Bool)
        """
        if pid == None:
            vmrange = self.get_vmrange(value, maps)
        else:
            vmrange = self.get_vmrange(value, maps, pid=pid)
        return vmrange is not None

    def examine_mem_value(self, value, pid=None):
        """
        Customized examine_mem_value from https://github.com/longld/peda
        Args:
            - value: value to examine (Int)

        Returns:
            - tuple of (value(Int), type(String), next_value(Int))
        """
        def examine_data(value, bits=32):
            out = self.execute_redirect("x/%sx 0x%x" % ("g" if bits == 64 else "w", value))
            if out:
                v = out.split(":\t")[-1].strip()
                if is_printable(int2hexstr(to_int(v), bits//8)):
                    out = self.execute_redirect("x/s 0x%x" % value)
            return out

        result = (None, None, None)
        if value is None:
            return result

        if pid == None:
            maps = e.get_vmmap()
            binmap = e.get_vmmap("binary")
        else:
            maps = e.get_vmmap(pid=pid)
            binmap = e.get_vmmap(pid=pid, name="binary")

        (arch, bits) = self.getarch()
        if not e.is_address(value, pid=pid): # a value
            result = (to_hex(value), "value", "")
            return result
        else:
            (_, _, _, mapname) = self.get_vmrange(value, pid=pid)

        # check for writable first so rwxp mem will be treated as data
        if e.is_writable(value, pid=pid): # writable data address
            out = examine_data(value, bits)
            if out:
                result = (to_hex(value), "data", out.split(":", 1)[1].strip())

        elif e.is_executable(value, pid=pid): # code/rodata address
            if self.is_address(value, binmap):
                headers = e.elfheader(pid=pid)
            else:
                headers = e.elfheader_solib(mapname, pid=pid)

            if headers:
                headers = sorted(headers.items(), key=lambda x: x[1][1])
                for (k, (start, end, type)) in headers:
                    if value >= start and value < end:
                        if type == "code":
                            out = self.get_disasm(value)
                            if "\n" in out:
                                n_idx = out.index("\n")
                                out_before = out[:n_idx]
                                out_after = out[n_idx+1:]
                                out = out_before
                                while out_after[0] == " ":
                                    out_after = out_after[1:]
                                out += out_after
                            p = re.compile(".*?0x[^ ]*?\s(.*)")
                            m = p.search(out)
                            result = (to_hex(value), "code", m.group(1))
                        else: # rodata address
                            out = examine_data(value, bits)
                            result = (to_hex(value), "rodata", out.split(":", 1)[1].strip())
                        break

                if result[0] is None: # not fall to any header section
                    out = examine_data(value, bits)
                    result = (to_hex(value), "rodata", out.split(":", 1)[1].strip())

            else: # not belong to any lib: [heap], [vdso], [vsyscall], etc
                out = self.get_disasm(value)
                if "(bad)" in out:
                    out = examine_data(value, bits)
                    result = (to_hex(value), "rodata", out.split(":", 1)[1].strip())
                else:
                    p = re.compile(".*?0x[^ ]*?\s(.*)")
                    m = p.search(out)
                    result = (to_hex(value), "code", m.group(1))

        else: # readonly data address
            out = examine_data(value, bits)
            if out:
                result = (to_hex(value), "rodata", out.split(":", 1)[1].strip())
            else:
                result = (to_hex(value), "rodata", "MemError")

        return result

    def examine_mem_reference(self, value, pid=None, depth=5):
        """
        Customized examine_mem_reference from https://github.com/longld/peda

        Args:
            - value: value to examine (Int)

        Returns:
            - list of tuple of (value(Int), type(String), next_value(Int))
        """
        result = []
        if depth <= 0:
            depth = 0xffffffff

        (v, t, vn) = e.examine_mem_value(value, pid=pid)
        while vn is not None:
            if len(result) > depth:
                _v, _t, _vn = result[-1]
                result[-1] = (_v, _t, "--> ...")
                break

            result += [(v, t, vn)]
            if v == vn or to_int(v) == to_int(vn): # point to self
                break
            if to_int(vn) is None:
                break
            if to_int(vn) in [to_int(v) for (v, _, _) in result]: # point back to previous value
                break
            (v, t, vn) = e.examine_mem_value(to_int(vn), pid=pid)

        return result

    def parse_arg(self, arg_str, text, f_log, f_symbol_memo):
        b = 0
        appending_one_log = ""
        arg_data_str = ""
        arg_reg_str = ""
        arg_reg_data_str = ""
        # arg_str has symbol
        if "#" in arg_str:
            f_symbol_memo.add(hex(pc) + ": " + arg_str + "\n")
            arg_str_before = r_comment_before.sub("", arg_str)
            arg_str_after = r_comment.sub("", arg_str)
            arg_str_after = r_comment1.sub("", arg_str_after)
            arg_str = arg_str_before
            arg_str += "["
            arg_str += arg_str_after
            arg_str += "]"
        # arg_str is ptr
        if "PTR" in arg_str:
            typ = ""
            if "QWORD PTR" in arg_str:
                typ = "long"
                b = 8
            elif "DWORD PTR" in arg_str:
                typ = "int"
                b = 4
            elif "WORD PTR" in arg_str:
                typ = "short"
                b = 2
            elif "BYTE PTR" in arg_str:
                typ = "char"
                b = 1
            else:
                print("unknown error")
                f_log.add("unknown error\n")
                return
            try:
                idx_start = arg_str.index("[") + 1
                idx_end = arg_str.index("]")
                appending_one_log = arg_str[:idx_end+1]
                arg_str = arg_str[idx_start:idx_end]
                arg_data_str = e.parse_and_eval(arg_str)

                # remove symbol
                if "<" in arg_data_str:
                    idx = arg_data_str.index("<") - 1
                    f_symbol_memo.add(hex(pc) + ": " + arg_data_str + "\n")
                    arg_data_str = arg_data_str[:idx]

                arg_reg_str = ""
                for ch in list(arg_str):
                    if ch in ["+", "-"]:
                        break
                    arg_reg_str += ch
                arg_reg_data_str = hex(e.getreg(arg_reg_str))
            except: # for segment register
                idx_start = arg_str.index("PTR ") + 4
                arg_str = arg_str[idx_start:]
                appending_one_log = arg_str
                arg_data_str = arg_str
            new_arg_str = "(" + typ + "*)" + arg_data_str
            text = text.replace("arg_str", new_arg_str)
        # arg_str is register
        elif arg_str in regs:
            appending_one_log = arg_str
            arg_data_str = e.getreg(arg_str)
            arg_data_str = hex(arg_data_str)
        # arg_str is imm
        else:
            # arg_str has symbol ( TODO: this is difficult for me now )
            if "#" in arg_str:
                f_symbol_memo.add(hex(pc) + ": " + arg_str + "\n")
                arg_str_before = r_comment_before.sub("", arg_str)
                arg_str_after = r_comment.sub("", arg_str)
                arg_str_after = r_comment1.sub("", arg_str_after)
                arg_str = arg_str_before
                arg_str += "["
                arg_str += arg_str_after
                arg_str += "]"
                appending_one_log = ""
            # arg_str is normal imm
            elif arg_str != "":
                appending_one_log = arg_str
                if arg_str[0] == "[":
                    arg_str = arg_str[1:-1]
                    arg_reg_str = ""
                    for ch in list(arg_str):
                        if ch in ["+", "-"]:
                            break
                        arg_reg_str += ch
                    arg_reg_data_str = hex(e.getreg(arg_reg_str))
                arg_data_str = e.parse_and_eval(arg_str)
            # arg_str is ""
            else:
                arg_data_str = ""
                appending_one_log = ""
        return (arg_str, arg_data_str, arg_reg_str, arg_reg_data_str, b, appending_one_log)

    def get_vmmap(self, pid=None, name=None):
        """
        Cutomized get_vmmap from https://github.com/longld/peda

        Args:
            - name: name/address of binary/library to get mapping range (String)
                + name = "binary" means debugged program
                + name = "all" means all virtual maps

        Returns:
            - list of virtual mapping ranges (start(Int), end(Int), permission(String), mapname(String))

        """
        def _get_offline_maps():
            name = self.getfile()
            if not name:
                return None
            headers = self.elfheader()
            binmap = []
            hlist = [x for x in headers.items() if x[1][2] == 'code']
            hlist = sorted(hlist, key=lambda x:x[1][0])
            binmap += [(hlist[0][1][0], hlist[-1][1][1], "rx-p", name)]

            hlist = [x for x in headers.items() if x[1][2] == 'rodata']
            hlist = sorted(hlist, key=lambda x:x[1][0])
            binmap += [(hlist[0][1][0], hlist[-1][1][1], "r--p", name)]

            hlist = [x for x in headers.items() if x[1][2] == 'data']
            hlist = sorted(hlist, key=lambda x:x[1][0])
            binmap += [(hlist[0][1][0], hlist[-1][1][1], "rw-p", name)]

            return binmap

        def _get_allmaps_osx(pid, remote=False):
            maps = []
            #_DATA                 00007fff77975000-00007fff77976000 [    4K] rw-/rw- SM=COW  /usr/lib/system/libremovefile.dylib
            pattern = re.compile("([^\n]*)\s*  ([0-9a-f][^-\s]*)-([^\s]*) \[.*\]\s([^/]*).*  (.*)")

            if remote: # remote target, not yet supported
                return maps
            else: # local target
                try:  out = execute_external_command("/usr/bin/vmmap -w %s" % pid)
                except: error_msg("could not read vmmap of process")

            matches = pattern.findall(out)
            if matches:
                for (name, start, end, perm, mapname) in matches:
                    if name.startswith("Stack"):
                        mapname = "[stack]"
                    start = to_int("0x%s" % start)
                    end = to_int("0x%s" % end)
                    if mapname == "":
                        mapname = name.strip()
                    maps += [(start, end, perm, mapname)]
            return maps


        def _get_allmaps_freebsd(pid, remote=False):
            maps = []
            mpath = "/proc/%s/map" % pid
            # 0x8048000 0x8049000 1 0 0xc36afdd0 r-x 1 0 0x1000 COW NC vnode /path/to/file NCH -1
            pattern = re.compile("0x([0-9a-f]*) 0x([0-9a-f]*)(?: [^ ]*){3} ([rwx-]*)(?: [^ ]*){6} ([^ ]*)")

            if remote: # remote target, not yet supported
                return maps
            else: # local target
                try:  out = open(mpath).read()
                except: error_msg("could not open %s; is procfs mounted?" % mpath)

            matches = pattern.findall(out)
            if matches:
                for (start, end, perm, mapname) in matches:
                    if start[:2] in ["bf", "7f", "ff"] and "rw" in perm:
                        mapname = "[stack]"
                    start = to_int("0x%s" % start)
                    end = to_int("0x%s" % end)
                    if mapname == "-":
                        if start == maps[-1][1] and maps[-1][-1][0] == "/":
                            mapname = maps[-1][-1]
                        else:
                            mapname = "mapped"
                    maps += [(start, end, perm, mapname)]
            return maps

        def _get_allmaps_linux(pid, remote=False):
            maps = []
            mpath = "/proc/%s/maps" % pid
            #00400000-0040b000 r-xp 00000000 08:02 538840  /path/to/file
            pattern = re.compile("([0-9a-f]*)-([0-9a-f]*) ([rwxps-]*)(?: [^ ]*){3} *(.*)")

            if remote: # remote target
                tmp = tmpfile()
                self.execute("remote get %s %s" % (mpath, tmp.name))
                tmp.seek(0)
                out = tmp.read()
                tmp.close()
            else: # local target
                out = open(mpath).read()

            matches = pattern.findall(out)
            if matches:
                for (start, end, perm, mapname) in matches:
                    start = to_int("0x%s" % start)
                    end = to_int("0x%s" % end)
                    if mapname == "":
                        mapname = "mapped"
                    maps += [(start, end, perm, mapname)]
            return maps

        result = []
        if pid == None:
            pid = self.getpid()
        if not pid: # not running, try to use elfheader()
            try:
                return _get_offline_maps()
            except:
                return []

        # retrieve all maps
        os   = self.getos()
        rmt  = self.is_target_remote()
        maps = []
        try:
            if   os == "FreeBSD": maps = _get_allmaps_freebsd(pid, rmt)
            elif os == "Linux"  : maps = _get_allmaps_linux(pid, rmt)
            elif os == "Darwin" : maps = _get_allmaps_osx(pid, rmt)
        except Exception as e:
            if config.Option.get("debug") == "on":
                msg("Exception: %s" %e)
                traceback.print_exc()

        # select maps matched specific name
        if name == "binary":
            name = self.getfile()
        if name is None or name == "all":
            name = ""

        if to_int(name) is None:
            for (start, end, perm, mapname) in maps:
                if name in mapname:
                    result += [(start, end, perm, mapname)]
        else:
            addr = to_int(name)
            for (start, end, perm, mapname) in maps:
                if start <= addr and addr < end:
                    result += [(start, end, perm, mapname)]

        return result

    def get_vmrange(self, address, maps=None, pid=None):
        """
        Customized get_vmrange from https://github.com/longld/peda

        Args:
            - address: target address (Int)
            - maps: only find in provided maps (List)

        Returns:
            - tuple of virtual memory info (start, end, perm, mapname)
        """
        if address is None:
            return None
        if maps is None:
            if pid ==None:
                maps = e.get_vmmap()
            else:
                maps = e.get_vmmap(pid=pid)
        if maps:
            for (start, end, perm, mapname) in maps:
                if start <= address and end > address:
                    return (start, end, perm, mapname)
        # failed to get the vmmap
        else:
            try:
                gdb.selected_inferior().read_memory(address, 1)
                start = address & 0xfffffffffffff000
                end = start + 0x1000
                return (start, end, 'rwx', 'unknown')
            except:
                return None

    def is_executable(self, address, maps=None, pid=None):
        """
        Check if an address is executable

        Args:
            - address: target address (Int)
            - maps: only check in provided maps (List)

        Returns:
            - True if address belongs to an executable address range (Bool)
        """
        if pid == None:
            vmrange = self.get_vmrange(address, maps, pid)
        else:
            vmrange = self.get_vmrange(address, maps, pid=pid)
        if vmrange and "x" in vmrange[2]:
            return True
        else:
            return False

    def is_writable(self, address, maps=None, pid=None):
        """
        Customized is_writable from https://github.com/longld/peda

        Args:
            - address: target address (Int)
            - maps: only check in provided maps (List)

        Returns:
            - True if address belongs to a writable address range (Bool)
        """
        vmrange = self.get_vmrange(address, maps, pid=pid)
        if vmrange and "w" in vmrange[2]:
            return True
        else:
            return False

    def elfheader(self, name=None, pid=None):
        """
        Customized elfheader from https://github.com/longld/peda

        Args:
            - name: specific header name (String)

        Returns:
            - dictionary of headers {name(String): (start(Int), end(Int), type(String))}
        """
        elfinfo = {}
        elfbase = 0
        if pid == None:
            pid = self.getpid()
        if pid:
            binmap = e.get_vmmap(name="binary", pid=pid)
            elfbase = binmap[0][0] if binmap else 0

        out = self.execute_redirect("maintenance info sections")
        if not out:
            return {}

        p = re.compile("\s*(0x[^-]*)->(0x[^ ]*) at (0x[^:]*):\s*([^ ]*)\s*(.*)")
        matches = p.findall(out)

        for (start, end, offset, hname, attr) in matches:
            start, end, offset = to_int(start), to_int(end), to_int(offset)
            # skip unuseful header
            if start < offset:
                continue
            # if PIE binary, update with runtime address
            if start < elfbase:
                start += elfbase
                end += elfbase

            if "CODE" in attr:
                htype = "code"
            elif "READONLY" in attr:
                htype = "rodata"
            else:
                htype = "data"

            elfinfo[hname.strip()] = (start, end, htype)

        result = {}
        if name is None:
            result = elfinfo
        else:
            if name in elfinfo:
                result[name] = elfinfo[name]
            else:
                for (k, v) in elfinfo.items():
                    if name in k:
                        result[k] = v
        return result

    def elfheader_solib(self, solib=None, name=None, pid=None):
        """
        Customized elfheader_solib from https://github.com/longld/peda

        Args:
            - solib: shared library name (String)
            - name: specific header name (String)

        Returns:
            - dictionary of headers {name(String): start(Int), end(Int), type(String))
        """
        # hardcoded ELF header type
        header_type = {"code": [".text", ".fini", ".init", ".plt", "__libc_freeres_fn"],
            "data": [".dynamic", ".data", ".ctors", ".dtors", ".jrc", ".got", ".got.plt",
                    ".bss", ".tdata", ".tbss", ".data.rel.ro", ".fini_array",
                    "__libc_subfreeres", "__libc_thread_subfreeres"]
        }

        @memoized
        def _elfheader_solib_all():
            out = self.execute_redirect("info files")
            if not out:
                return None

            p = re.compile("[^\n]*\s*(0x[^ ]*) - (0x[^ ]*) is (\.[^ ]*) in (.*)")
            soheaders = p.findall(out)

            result = []
            for (start, end, hname, libname) in soheaders:
                start, end = to_int(start), to_int(end)
                result += [(start, end, hname, os.path.realpath(libname))] # tricky, return the realpath version of libraries
            return result

        elfinfo = {}

        headers = _elfheader_solib_all()
        if not headers:
            return {}

        if solib is None:
            return headers

        vmap = e.get_vmmap(solib, pid=pid)
        elfbase = vmap[0][0] if vmap else 0

        for (start, end, hname, libname) in headers:
            if solib in libname:
                # if PIE binary or DSO, update with runtime address
                if start < elfbase:
                    start += elfbase
                if end < elfbase:
                    end += elfbase
                # determine the type
                htype = "rodata"
                if hname in header_type["code"]:
                    htype = "code"
                elif hname in header_type["data"]:
                    htype = "data"
                elfinfo[hname.strip()] = (start, end, htype)

        result = {}
        if name is None:
            result = elfinfo
        else:
            if name in elfinfo:
                result[name] = elfinfo[name]
            else:
                for (k, v) in elfinfo.items():
                    if name in k:
                        result[k] = v
        return result
