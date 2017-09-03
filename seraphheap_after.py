
def infoh(victim):
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    chunkaddr = victim
    try :
        get_heap_info()
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
        #print("===================================")
        #print("             Heap info             ")
        #print("===================================")
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                #sys.stdout.write(blue("Freed", "bold"))
                usedflag = False
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                #sys.stdout.write(red("Used ", "bold"))
                usedflag = True
        #else :
        if not status:
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            #sys.stdout.write(blue("Freed", "bold"))
            usedflag = False
            #unlinkable(chunkaddr,fd,bk)
        #print("\033[32mprev_size :\033[37m 0x%x                  " % prev_size)
        if usedflag:
            sys.stdout.write(green(to_hex(chunkaddr), "bold"))
        if not usedflag:
            sys.stdout.write(blue(to_hex(chunkaddr), "bold"))
        for i in range(19 - len(hex(chunkaddr))):
            sys.stdout.write(" ")
        #sys.stdout.write("    ")
        sys.stdout.write(white(hex(prev_size), "bold"))
        #print("\033[32msize :\033[37m 0x%x                  " % (size & 0xfffffffffffffff8))
        for i in range(10 - len(hex(prev_size))):
            sys.stdout.write(" ")
        realsize = size & 0xfffffffffffffff8
        sys.stdout.write(white(hex(realsize), "bold"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        for i in range(9 - len(hex(realsize))):
            sys.stdout.write(" ")
        nm = size & 4 #non_mainarea
        if(nm == 4):
            sys.stdout.write(red(str(1), "bold"))
        else:
            sys.stdout.write(red(str(0)))
        #sys.stdout.write(hex(pi))
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        sys.stdout.write("  ")
        im = size & 2 #is_mmaped
        if(im == 2):
            sys.stdout.write(green(str(1), "bold"))
        else:
            sys.stdout.write(green(str(0)))
        #sys.stdout.write(hex(im))
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        sys.stdout.write("  ")
        pi = size & 1 #prev_inuse
        if(pi == 1):
            sys.stdout.write(blue(str(1), "bold"))
        else:
            sys.stdout.write(blue(str(0)))
        #sys.stdout.write(hex(nm))
        if not status :
            #print("\033[32mfd :\033[37m 0x%x                  " % fd)
            #print("\033[32mbk :\033[37m 0x%x                  " % bk)
            sys.stdout.write("     ")
            sys.stdout.write(white(to_hex(fd), "bold"))
            for i in range(19 - len(hex(fd))):
                sys.stdout.write(" ")
            print(white(to_hex(bk), "bold"))
        else:
            sys.stdout.write("     ")
            sys.stdout.write("None")
            for i in range(19 - len("None")):
                sys.stdout.write(" ")
            print("None")
        if size >= 512*(capsize/4) :
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            #print("\033[32mfd_nextsize :\033[37m 0x%x  " % fd_nextsize)
            #print("\033[32mbk_nextsize :\033[37m 0x%x  " % bk_nextsize) 
        #return nextaddr
        return chunkaddr + (size & 0xfffffffffffffff8)
    except :
        #print("Can't access memory")
        sys.stdout.write("")
        return -1

def getinfoh(victim):
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    chunkaddr = victim
    try :
        get_heap_info()
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
        #print("===================================")
        #print("             Heap info             ")
        #print("===================================")
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                #sys.stdout.write(blue("Freed", "bold"))
                usedflag = False
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                #sys.stdout.write(red("Used ", "bold"))
                usedflag = True
        #else :
        if not status:
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            #sys.stdout.write(blue("Freed", "bold"))
            usedflag = False
            #unlinkable(chunkaddr,fd,bk)
        #print("\033[32mprev_size :\033[37m 0x%x                  " % prev_size)
        if usedflag:
            #sys.stdout.write(green(to_hex(chunkaddr), "bold"))
            sys.stdout.write("")
        if not usedflag:
            #sys.stdout.write(blue(to_hex(chunkaddr), "bold"))
            sys.stdout.write("")
        for i in range(19 - len(hex(chunkaddr))):
            #sys.stdout.write(" ")
            sys.stdout.write("")
        #sys.stdout.write("    ")
        #sys.stdout.write(white(hex(prev_size), "bold"))
        #print("\033[32msize :\033[37m 0x%x                  " % (size & 0xfffffffffffffff8))
        for i in range(10 - len(hex(prev_size))):
            #sys.stdout.write(" ")
            sys.stdout.write("")
        realsize = size & 0xfffffffffffffff8
        #sys.stdout.write(white(hex(realsize), "bold"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        for i in range(9 - len(hex(realsize))):
            #sys.stdout.write(" ")
            sys.stdout.write("")
        nm = size & 4 #non_mainarea
        if(nm == 4):
            #sys.stdout.write(red(str(1), "bold"))
            sys.stdout.write("")
        else:
            sys.stdout.write("")
            #sys.stdout.write(red(str(0)))
        #sys.stdout.write(hex(pi))
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        #sys.stdout.write("  ")
        im = size & 2 #is_mmaped
        if(im == 2):
            sys.stdout.write("")
            #sys.stdout.write(green(str(1), "bold"))
        else:
            sys.stdout.write("")
            #sys.stdout.write(green(str(0)))
        #sys.stdout.write(hex(im))
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        #sys.stdout.write("  ")
        pi = size & 1 #prev_inuse
        if(pi == 1):
            sys.stdout.write("")
            #sys.stdout.write(blue(str(1), "bold"))
        else:
            sys.stdout.write("")
            #sys.stdout.write(blue(str(0)))
        #sys.stdout.write(hex(nm))
        if not status :
            sys.stdout.write("")
            #print("\033[32mfd :\033[37m 0x%x                  " % fd)
            #print("\033[32mbk :\033[37m 0x%x                  " % bk)
            #sys.stdout.write("     ")
            #sys.stdout.write(white(to_hex(fd), "bold"))
            for i in range(19 - len(hex(fd))):
                sys.stdout.write("")
                #sys.stdout.write(" ")
            #print(white(to_hex(bk), "bold"))
        else:
            sys.stdout.write("")
            #sys.stdout.write("     ")
            #sys.stdout.write("None")
            for i in range(19 - len("None")):
                sys.stdout.write("")
                #sys.stdout.write(" ")
            #print("None")
        if size >= 512*(capsize/4) :
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            #print("\033[32mfd_nextsize :\033[37m 0x%x  " % fd_nextsize)
            #print("\033[32mbk_nextsize :\033[37m 0x%x  " % bk_nextsize) 
        #return nextaddr
        return chunkaddr + (size & 0xfffffffffffffff8)
    except :
        #print("Can't access memory")
        #sys.stdout.write("")
        return -1

#def parseh():
#    print(yellow("addr               prev      size     ", "bold") + red("NM", "bold") + "/" + green("IM", "bold") + "/" + blue("PI", "bold") + "    " + yellow("fd", "bold") + "                 " + yellow("bk", "bold"))
#    if capsize == 0 :
#        arch = getarch()
#    addr = pwngdb.getheapbase()
#    addr = infoh(addr)
#    while(addr != -1):
#        addr = infoh(addr)

def ph(arena=None):
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
    size_str = yellow("size", "bold")
    fd_str = yellow("fd", "bold")
    bk_str = yellow("bk", "bold")
    NM = red("NM", "bold")
    IM = green("IM", "bold")
    PI = blue("PI", "bold")
    print('{:<32}{:<22}{:<22}{:<48}{:<30}{:<28}'.format(addr_str, prev_str, size_str, NM+"/"+IM+"/"+PI, fd_str, bk_str))
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
                NM = red("0")
            else:
                NM = red("1", "bold")
            IM = str(size & 2)
            if(IM == "0"):
                IM = green("0")
            else:
                IM = green("1", "bold")
            PI = str(size & 1)
            if(PI == "0"):
                PI = blue("0")
            else:
                PI = blue("1", "bold")
            bits = NM + "  " + IM + "  " + PI
            size = size & 0xfffffffffffffff8
            if size == 0 :
                print("\033[31mCorrupt ?! \033[0m(size == 0) (0x%x)" % chunkaddr)
                break 
            if status :
                if chunkaddr in fastchunk :
                    msg = "\033[1;34m Freed \033[0m"
                    chunkaddr_str = blue(hex(chunkaddr), "bold")
                    print('{:<32}0x{:<8x}0x{:<8x}{:<10}{:>18}{:>18}'.format(chunkaddr_str, prev_size, size, bits, hex(fd), "None"))
                else :
                    msg = "\033[31m Used \033[0m"
                    chunkaddr_str = green(hex(chunkaddr), "bold")
                    print('{:<32}0x{:<8x}0x{:<8x}{:<10}{:>18}{:>18}'.format(chunkaddr_str, prev_size, size, bits, "None", "None"))
            else :
                msg = "\033[1;34m Freed \033[0m"
                chunkaddr_str = blue(hex(chunkaddr), "bold")
                print('{:<32}0x{:<8x}0x{:<8x}{:<10}{:>18}{:>18}'.format(chunkaddr_str, prev_size, size, bits, hex(fd), hex(bk)))
            chunkaddr = chunkaddr + (size & 0xfffffffffffffff8)

            if chunkaddr > top["addr"] :
                print("\033[31mCorrupt ?!\033[0m")
                break 
        except :
            print("Corrupt ?!")
            break


def getheaplist(lst):
    #print(yellow("addr               prev      size     ", "bold") + red("NM", "bold") + "/" + green("IM", "bold") + "/" + blue("PI", "bold") + "    " + yellow("fd", "bold") + "                 " + yellow("bk", "bold"))
    if capsize == 0 :
        arch = getarch()
    addr = pwngdb.getheapbase()
    lst.append(addr)
    addr = getinfoh(addr)
    lst.append(addr)
    while(addr != -1):
        addr = getinfoh(addr)
        lst.append(addr)


def ci_old(victim):
    print("===================================")
    print("            Chunk info             ")
    print("===================================")
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    if(capsize == 8):
        capstr = "qword"
    else:
        capstr = "dword"
    chunkaddr = victim
    if(int(chunkaddr) < 100):
        lst = []
        getheaplist(lst)
        chunkaddr = int(lst[victim-1])
    try :
        get_heap_info()
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
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                usedflag = False
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                usedflag = True
        else :
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            usedflag = False
            unlinkable(chunkaddr,fd,bk)
        pi = size & 1
        im = size & 2
        nm = size & 4
        if(pi == 1):
            pistr = white("1", "bold")
            pistr = "1"
        else:
            pistr = "0"
        if(im == 2):
            imstr = white("1", "bold")
            imstr = "1"
        else:
            imstr = "0"
        if(nm == 4):
            nmstr = white("1", "bold")
            nmstr = "1"
        else:
            nmstr = "0"
        realsize = size & 0xfffffffffffffff8
        if usedflag:
            sys.stdout.write(green(hex(chunkaddr), "bold") + " --> ")
            #print(green("prev_size : ", "bold") + white(hex(prev_size), "bold"))
            print(white(hex(prev_size), "bold") + green(" (prev_size)", "bold"))
            sys.stdout.write(green(hex(chunkaddr+capsize), "bold") + " --> ")
            print(white(hex(realsize), "bold") + yellow("|"+nmstr+"|"+imstr+"|"+pistr+"|", "bold") + green(" (size)", "bold"))
        if not usedflag:
            sys.stdout.write(blue(hex(chunkaddr), "bold") + " --> ")
            #print(blue("prev_size : ", "bold") + white(hex(prev_size), "bold"))
            print(white(hex(prev_size), "bold") + blue(" (prev_size)", "bold"))
            sys.stdout.write(blue(hex(chunkaddr+capsize), "bold") + " --> ")
            #print(blue("size : ", "bold") + white(hex(realsize), "bold") + green(" (", "bold") + nmstr + green("|", "bold") + imstr + green("|", "bold") + pistr + green(")", "bold"))
            print(white(hex(realsize), "bold") + yellow("|"+nmstr+"|"+imstr+"|"+pistr+"|", "bold") + blue(" (size)", "bold"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        if not status :
            if usedflag:
                #print(green("fd : ", "bold") + white(hex(fd), "bold"))
                #print(green("bk : ", "bold") + white(hex(bk), "bold"))
                print(green("fd : ", "bold") + white(hex(fd), "bold"))
                print(green("bk : ", "bold") + white(hex(bk), "bold"))
            if not usedflag:
                #print(blue("fd : ", "bold") + white(hex(fd), "bold"))
                #print(blue("bk : ", "bold") + white(hex(bk), "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*2), "bold") + " --> ")
                print(white(hex(fd), "bold") + blue(" (fd)", "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*3), "bold") + " --> ")
                print(white(hex(bk), "bold") + blue(" (bk)", "bold"))
        nextsizeflag = False
        if size >= 512*(capsize/4) :
            nextsizeflag = True
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            if usedflag:
            #    #print(green("fd_nextsize : ", "bold") + white(hex(fd_nextsize), "bold"))
            #    #print(green("bk_nextsize : ", "bold") + white(hex(bk_nextsize), "bold"))
                sys.stdout.write(green(hex(chunkaddr+capsize*4), "bold") + " --> ")
                print(white(hex(fd_nextsize), "bold") + green(" (fd_nextsize)", "bold"))
                sys.stdout.write(green(hex(chunkaddr+capsize*5), "bold") + " --> ")
                print(white(hex(bk_nextsize), "bold") + green(" (bk_nextsize)", "bold"))
            if not usedflag:
                #print(blue("fd_nextsize : ", "bold") + white(hex(fd_nextsize), "bold"))
                #print(blue("bk_nextsize : ", "bold") + white(hex(bk_nextsize), "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*4), "bold") + " --> ")
                print(white(hex(fd_nextsize), "bold") + blue(" (fd_nextsize)", "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*5), "bold") + " --> ")
                print(white(hex(bk_nextsize), "bold") + blue(" (bk_nextsize)", "bold"))
        #gdb.execute(capstr + " " + hex(chunkaddr+capsize*2) + " " + hex(int(realsize/capsize-2)))
    except :
        print("Can't access memory")

def white(x):
    return "\033[1;37m" + x + "\033[37m"

def ci(victim):
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    chunkaddr = victim
    try :
        if not get_heap_info() :
            print("Can't find heap info")
            return
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
        #print("==================================")
        #print("            Chunk info            ")
        #print("==================================")
        used_flag = 0
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                used_flag = 0
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                used_flag = 1
        else :
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            used_flag = 0
            unlinkable(chunkaddr,fd,bk)
        #print("\033[32mprev_size :\033[37m 0x%x                  " % prev_size)
        #print("\033[32msize :\033[37m 0x%x                  " % (size & 0xfffffffffffffff8))
        aligned_size = size & 0xfffffffffffffff8
        NM = size & 4
        IM = size & 2
        PI = size & 1
        if(used_flag == 1):
            print(green(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size)) + green(" (prev_size)", "bold"))
            print(green(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size)) + yellow("|" + str(NM) + "|" + str(IM) + "|" + str(PI) + "|", "bold") + green(" (size)", "bold"))
        else:
            print(blue(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size), "bold") + blue(" (prev_size)", "bold"))
            print(blue(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size), "bold") + yellow("|" + str(NM) + "|" + str(IM) + "|" + str(PI) + "|", "bold") + blue(" (size)", "bold"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        if not status :
            #print("\033[32mfd :\033[37m 0x%x                  " % fd)
            #print("\033[32mbk :\033[37m 0x%x                  " % bk)
            print(blue(hex(chunkaddr + capsize*2), "bold") + " --> " + white(hex(fd)) + blue(" (fd)", "bold"))
            print(blue(hex(chunkaddr + capsize*3), "bold") + " --> " + white(hex(bk)) + blue(" (bk)", "bold"))
        next_size_flag = False
        if size >= 512*(capsize/4) :
            next_size_flag = True
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            #print("\033[32mfd_nextsize :\033[37m 0x%x  " % fd_nextsize)
            #print("\033[32mbk_nextsize :\033[37m 0x%x  " % bk_nextsize) 
            if(used_flag == 1):
                print(green(hex(chunkaddr + capsize*4), "bold") + " --> " + white(hex(fd_nextsize)) + green(" (fd_nextsize)", "bold"))
                print(green(hex(chunkaddr + capsize*5), "bold") + " --> " + white(hex(bk_nextsize)) + green(" (bk_nextsize)", "bold"))
            else:
                print(blue(hex(chunkaddr + capsize*4), "bold") + " --> " + white(hex(fd_nextsize)) + blue(" (fd_nextsize)", "bold"))
                print(blue(hex(chunkaddr + capsize*5), "bold") + " --> " + white(hex(bk_nextsize)) + blue(" (bk_nextsize)", "bold"))
    except :
        print("Can't access memory")

def cix(victim):
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    chunkaddr = victim
    try :
        if not get_heap_info() :
            print("Can't find heap info")
            return
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
        used_flag = 0
        fast_flag = 0
        if status:
            if chunkaddr in fastchunk :
                fast_flag = 1
                used_flag = 0
            else :
                used_flag = 1
        else :
            used_flag = 0
            unlinkable(chunkaddr,fd,bk)
            print("==================================================================")
        aligned_size = size & 0xfffffffffffffff8
        NM = size & 4
        IM = size & 2
        PI = size & 1
        if(used_flag == 1):
            print(green(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size)) + green(" (prev_size)", "bold"))
            print(green(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size)) + \
                    yellow("|" + str(NM) + "|" + str(IM) + "|" + str(PI) + "|", "bold") + green(" (size)", "bold"))
        else:
            if(fast_flag == 0):
                print(blue(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size)) + blue(" (prev_size)", "bold"))
                print(blue(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size)) + \
                    yellow("|" + str(NM) + "|" + str(IM) + "|" + str(PI) + "|", "bold") + blue(" (size)"))
            else:
                print(blue(hex(chunkaddr)) + " --> " + white(hex(prev_size)) + blue(" (prev_size)"))
                print(blue(hex(chunkaddr+capsize)) + " --> " + white(hex(aligned_size)) + \
                    yellow("|" + str(NM) + "|" + str(IM) + "|" + str(PI) + "|", "bold") + blue(" (size)"))
        if not status :
            if(fast_flag == 0):
                print(blue(hex(chunkaddr + capsize*2), "bold") + " --> " + white(hex(fd)) + blue(" (fd)", "bold"))
                print(blue(hex(chunkaddr + capsize*3), "bold") + " --> " + white(hex(bk)) + blue(" (bk)", "bold"))
            else:
                print(blue(hex(chunkaddr + capsize*2)) + " --> " + white(hex(fd)) + blue(" (fd)"))
                print(blue(hex(chunkaddr + capsize*3)) + " --> " + white(hex(bk)) + blue(" (bk)"))
        next_size_flag = False
        if size >= 512*(capsize/4) :
            next_size_flag = True
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            if(used_flag == 1):
                print(green(hex(chunkaddr + capsize*4), "bold") + " --> " + white(hex(fd_nextsize)) + green(" (fd_nextsize)", "bold"))
                print(green(hex(chunkaddr + capsize*5), "bold") + " --> " + white(hex(bk_nextsize)) + green(" (bk_nextsize)", "bold"))
            else:
                if(fast_flag == 0):
                    print(blue(hex(chunkaddr + capsize*4), "bold") + " --> " + white(hex(fd_nextsize)) + blue(" (fd_nextsize)", "bold"))
                    print(blue(hex(chunkaddr + capsize*5), "bold") + " --> " + white(hex(bk_nextsize)) + blue(" (bk_nextsize)", "bold"))
                else:
                    print(blue(hex(chunkaddr + capsize*4)) + " --> " + white(hex(fd_nextsize)) + blue(" (fd_nextsize)"))
                    print(blue(hex(chunkaddr + capsize*5)) + " --> " + white(hex(bk_nextsize)) + blue(" (bk_nextsize)"))
        if used_flag:
            if next_size_flag:
                gdb.execute("ix " + hex(chunkaddr+capsize*4) + " " + hex(int(aligned_size/capsize-2)))
            else:
                gdb.execute("ix " + hex(chunkaddr+capsize*2) + " " + hex(int(aligned_size/capsize-2)))
        else:
            if next_size_flag:
                gdb.execute("ix " + hex(chunkaddr+capsize*6) + " " + hex(int(aligned_size/capsize-2)))
            else:
                gdb.execute("ix " + hex(chunkaddr+capsize*4) + " " + hex(int(aligned_size/capsize-2)))
    except :
        print("Can't access memory")


def cix_old(victim):
    print("===================================")
    print("            Chunk info             ")
    print("===================================")
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    if(capsize == 8):
        capstr = "qword"
    else:
        capstr = "dword"
    chunkaddr = victim
    if(int(chunkaddr) < 100):
        lst = []
        getheaplist(lst)
        chunkaddr = int(lst[victim-1])
    try :
        get_heap_info()
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
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                usedflag = False
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                usedflag = True
        else :
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            usedflag = False
            unlinkable(chunkaddr,fd,bk)
        pi = size & 1
        im = size & 2
        nm = size & 4
        if(pi == 1):
            pistr = white("1", "bold")
            pistr = "1"
        else:
            pistr = "0"
        if(im == 2):
            imstr = white("1", "bold")
            imstr = "1"
        else:
            imstr = "0"
        if(nm == 4):
            nmstr = white("1", "bold")
            nmstr = "1"
        else:
            nmstr = "0"
        realsize = size & 0xfffffffffffffff8
        if usedflag:
            sys.stdout.write(green(hex(chunkaddr), "bold") + " --> ")
            #print(green("prev_size : ", "bold") + white(hex(prev_size), "bold"))
            print(white(hex(prev_size), "bold") + green(" (prev_size)", "bold"))
            sys.stdout.write(green(hex(chunkaddr+capsize), "bold") + " --> ")
            print(white(hex(realsize), "bold") + yellow("|"+nmstr+"|"+imstr+"|"+pistr+"|", "bold") + green(" (size)", "bold"))
        if not usedflag:
            sys.stdout.write(blue(hex(chunkaddr), "bold") + " --> ")
            #print(blue("prev_size : ", "bold") + white(hex(prev_size), "bold"))
            print(white(hex(prev_size), "bold") + blue(" (prev_size)", "bold"))
            sys.stdout.write(blue(hex(chunkaddr+capsize), "bold") + " --> ")
            #print(blue("size : ", "bold") + white(hex(realsize), "bold") + green(" (", "bold") + nmstr + green("|", "bold") + imstr + green("|", "bold") + pistr + green(")", "bold"))
            print(white(hex(realsize), "bold") + yellow("|"+nmstr+"|"+imstr+"|"+pistr+"|", "bold") + blue(" (size)", "bold"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        if not status :
            if usedflag:
                #print(green("fd : ", "bold") + white(hex(fd), "bold"))
                #print(green("bk : ", "bold") + white(hex(bk), "bold"))
                print(green("fd : ", "bold") + white(hex(fd), "bold"))
                print(green("bk : ", "bold") + white(hex(bk), "bold"))
            if not usedflag:
                #print(blue("fd : ", "bold") + white(hex(fd), "bold"))
                #print(blue("bk : ", "bold") + white(hex(bk), "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*2), "bold") + " --> ")
                print(white(hex(fd), "bold") + blue(" (fd)", "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*3), "bold") + " --> ")
                print(white(hex(bk), "bold") + blue(" (bk)", "bold"))
        nextsizeflag = False
        if size >= 512*(capsize/4) :
            nextsizeflag = True
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            if usedflag:
                #print(green("fd_nextsize : ", "bold") + white(hex(fd_nextsize), "bold"))
                #print(green("bk_nextsize : ", "bold") + white(hex(bk_nextsize), "bold"))
                sys.stdout.write(green(hex(chunkaddr+capsize*4), "bold") + " --> ")
                print(white(hex(fd_nextsize), "bold") + green(" (fd_nextsize)", "bold"))
                sys.stdout.write(green(hex(chunkaddr+capsize*5), "bold") + " --> ")
                print(white(hex(bk_nextsize), "bold") + green(" (bk_nextsize)", "bold"))
            if not usedflag:
                #print(blue("fd_nextsize : ", "bold") + white(hex(fd_nextsize), "bold"))
                #print(blue("bk_nextsize : ", "bold") + white(hex(bk_nextsize), "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*4), "bold") + " --> ")
                print(white(hex(fd_nextsize), "bold") + blue(" (fd_nextsize)", "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*5), "bold") + " --> ")
                print(white(hex(bk_nextsize), "bold") + blue(" (bk_nextsize)", "bold"))
        if usedflag:
            if nextsizeflag:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*4) + " " + hex(int(realsize/capsize-2)))
            else:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*2) + " " + hex(int(realsize/capsize-2)))
        else:
            if nextsizeflag:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*6) + " " + hex(int(realsize/capsize-2)))
            else:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*4) + " " + hex(int(realsize/capsize-2)))
    except :
        print("Can't access memory")

def cixoff(victim):
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    if(capsize == 8):
        capstr = "qword"
    else:
        capstr = "dword"
    chunkaddr = victim
    if(int(chunkaddr) < 100):
        lst = []
        getheaplist(lst)
        chunkaddr = int(lst[victim-1])
    try :
        get_heap_info()
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
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                usedflag = False
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                usedflag = True
        else :
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            usedflag = False
            #unlinkable(chunkaddr,fd,bk)
        pi = size & 1
        im = size & 2
        nm = size & 4
        if(pi == 1):
            pistr = white("1", "bold")
            pistr = "1"
        else:
            pistr = "0"
        if(im == 2):
            imstr = white("1", "bold")
            imstr = "1"
        else:
            imstr = "0"
        if(nm == 4):
            nmstr = white("1", "bold")
            nmstr = "1"
        else:
            nmstr = "0"
        realsize = size & 0xfffffffffffffff8
        if usedflag:
            sys.stdout.write(green(hex(chunkaddr), "bold") + " --> ")
            #print(green("prev_size : ", "bold") + white(hex(prev_size), "bold"))
            print(white(hex(prev_size), "bold") + green(" (prev_size)", "bold"))
            sys.stdout.write(green(hex(chunkaddr+capsize), "bold") + " --> ")
            print(white(hex(realsize), "bold") + yellow("|"+nmstr+"|"+imstr+"|"+pistr+"|", "bold") + green(" (size)", "bold"))
        if not usedflag:
            sys.stdout.write(blue(hex(chunkaddr), "bold") + " --> ")
            #print(blue("prev_size : ", "bold") + white(hex(prev_size), "bold"))
            print(white(hex(prev_size), "bold") + blue(" (prev_size)", "bold"))
            sys.stdout.write(blue(hex(chunkaddr+capsize), "bold") + " --> ")
            #print(blue("size : ", "bold") + white(hex(realsize), "bold") + green(" (", "bold") + nmstr + green("|", "bold") + imstr + green("|", "bold") + pistr + green(")", "bold"))
            print(white(hex(realsize), "bold") + yellow("|"+nmstr+"|"+imstr+"|"+pistr+"|", "bold") + blue(" (size)", "bold"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        if not status :
            if usedflag:
                #print(green("fd : ", "bold") + white(hex(fd), "bold"))
                #print(green("bk : ", "bold") + white(hex(bk), "bold"))
                print(green("fd : ", "bold") + white(hex(fd), "bold"))
                print(green("bk : ", "bold") + white(hex(bk), "bold"))
            if not usedflag:
                #print(blue("fd : ", "bold") + white(hex(fd), "bold"))
                #print(blue("bk : ", "bold") + white(hex(bk), "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*2), "bold") + " --> ")
                print(white(hex(fd), "bold") + blue(" (fd)", "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*3), "bold") + " --> ")
                print(white(hex(bk), "bold") + blue(" (bk)", "bold"))
        nextsizeflag = False
        if size >= 512*(capsize/4) :
            nextsizeflag = True
            cmd = "x/" + word + hex(chunkaddr + capsize*4)
            fd_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            cmd = "x/" + word + hex(chunkaddr + capsize*5)
            bk_nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
            if usedflag:
            #    #print(green("fd_nextsize : ", "bold") + white(hex(fd_nextsize), "bold"))
            #    #print(green("bk_nextsize : ", "bold") + white(hex(bk_nextsize), "bold"))
                sys.stdout.write(green(hex(chunkaddr+capsize*4), "bold") + " --> ")
                print(white(hex(fd_nextsize), "bold") + green(" (fd_nextsize)", "bold"))
                sys.stdout.write(green(hex(chunkaddr+capsize*5), "bold") + " --> ")
                print(white(hex(bk_nextsize), "bold") + green(" (bk_nextsize)", "bold"))
            if not usedflag:
                #print(blue("fd_nextsize : ", "bold") + white(hex(fd_nextsize), "bold"))
                #print(blue("bk_nextsize : ", "bold") + white(hex(bk_nextsize), "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*4), "bold") + " --> ")
                print(white(hex(fd_nextsize), "bold") + blue(" (fd_nextsize)", "bold"))
                sys.stdout.write(blue(hex(chunkaddr+capsize*5), "bold") + " --> ")
                print(white(hex(bk_nextsize), "bold") + blue(" (bk_nextsize)", "bold"))
        if usedflag:
            if nextsizeflag:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*4) + " " + hex(int(realsize/capsize-2)))
            else:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*2) + " " + hex(int(realsize/capsize-2)))
        else:
            if nextsizeflag:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*6) + " " + hex(int(realsize/capsize-2)))
            else:
                gdb.execute(capstr + " " + hex(chunkaddr+capsize*4) + " " + hex(int(realsize/capsize-2)))
    except :
        print("Can't access memory")

def allci():
    lst = []
    getheaplist(lst)
    for i in range(len(lst)-2):
        gdb.execute("ci " + str(i+1))

def allcix():
    lst = []
    getheaplist(lst)
    for i in range(len(lst)-2):
        gdb.execute("cixoff " + str(i+1))

