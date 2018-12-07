
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

#import __main__
#__main__.unlinkable_flag = 1
def ci(victim):
    global fastchunk
    if capsize == 0 :
        arch = getarch()
    chunkaddr = victim
    try :
        if(victim < 100):
            lst = []
            getheaplist(lst)
            chunkaddr = lst[victim]
        if not get_heap_info() :
            print("Can't find heap info")
            return
        cmd = "x/" + word + hex(chunkaddr)
        prev_size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + capsize*1)
        size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        aligned_size = size & 0xfffffffffffffff8
        cmd = "x/" + word + hex(chunkaddr + capsize*2)
        fd = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + capsize*3)
        bk = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(chunkaddr + aligned_size + capsize)
        nextsize = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        status = nextsize & 1
        #print("==================================")
        #print("            Chunk info            ")
        #print("==================================")
        used_flag = 0
        fast_flag = 0
        unlinkable_result = []
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                used_flag = 0
                fast_flag = 1
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                used_flag = 1
        else :
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            used_flag = 0
            unlinkable_result = new_unlinkable(chunkaddr,fd,bk)
            #print("==================================================================")
        #print("\033[32mprev_size :\033[37m 0x%x                  " % prev_size)
        #print("\033[32msize :\033[37m 0x%x                  " % (size & 0xfffffffffffffff8))
        NM = size & 4
        IM = size & 2
        PI = size & 1
        if(used_flag == 1):
            print(green("prev| ", "bold") + yellow(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size)))
            print(green("size| ", "bold") + yellow(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size)) + yellow("|") + red(str(NM), "bold") + yellow("|") + green(str(IM), "bold") + yellow("|") + blue(str(PI), "bold") + yellow("|"))
        else:
            if(fast_flag == 0):
                print(blue("prev| ", "bold") + yellow(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size)))
                print(blue("size| ", "bold") + yellow(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size)) + yellow("|") + red(str(NM), "bold") + yellow("|") + green(str(IM), "bold") + yellow("|") + blue(str(PI), "bold") + yellow("|"))
            else:
                print(blue("prev| ") + yellow(hex(chunkaddr), "bold") + " --> " + white(hex(prev_size)))
                print(blue("size| ") + yellow(hex(chunkaddr+capsize), "bold") + " --> " + white(hex(aligned_size)) + yellow("|") + red(str(NM), "bold") + yellow("|") + green(str(IM), "bold") + yellow("|") + blue(str(PI), "bold") + yellow("|"))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        unlinkable_flag = 0
        if not used_flag:
            #print("\033[32mfd :\033[37m 0x%x                  " % fd)
            #print("\033[32mbk :\033[37m 0x%x                  " % bk)
            fd_str = white(hex(fd))
            bk_str = white(hex(bk))
            if(len(unlinkable_result) == 2):
                if(unlinkable_result[0] != 1):
                    unlinkable_flag = 1
                    fd_str += green(" [Unlinkable: *" + hex(unlinkable_result[0]) + "]")
                    bk_str += green(" [Unlinkable: *" + hex(unlinkable_result[1]) + "]")
            if(fast_flag == 0):
                print(blue(" fd | ", "bold") + yellow(hex(chunkaddr + capsize*2), "bold") + " --> " + fd_str)
                print(blue(" bk | ", "bold") + yellow(hex(chunkaddr + capsize*3), "bold") + " --> " + bk_str)
            else:
                print(blue(" fd | ") + yellow(hex(chunkaddr + capsize*2), "bold") + " --> " + fd_str)
                print(blue(" bk | ") + yellow(hex(chunkaddr + capsize*3), "bold") + " --> " + bk_str)
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
                print(green("fdNS|", "bold") + yellow(hex(chunkaddr + capsize*4), "bold") + " --> " + white(hex(fd_nextsize)))
                print(green("bkNS|", "bold") + yellow(hex(chunkaddr + capsize*5), "bold") + " --> " + white(hex(bk_nextsize)))
            else:
                print(blue("fdNS", "bold") + yellow(hex(chunkaddr + capsize*4), "bold") + " --> " + white(hex(fd_nextsize)))
                print(blue("bkNS", "bold") + yellow(hex(chunkaddr + capsize*5), "bold") + " --> " + white(hex(bk_nextsize)))
        if(unlinkable_flag == 1):
            sys.stdout.write(green("FD->bk: "))
            gdb.execute("infox " + hex(unlinkable_result[0]))
            sys.stdout.write(green("BK->fd: "))
            gdb.execute("infox " + hex(unlinkable_result[1]))
        return {'chunkaddr': chunkaddr, 'used_flag': used_flag, 'next_size_flag':next_size_flag, 'aligned_size': aligned_size}
    except :
        print("Can't access memory")

def cix(victim):
    try:
        res = ci(victim)
        chunkaddr = res['chunkaddr']
        used_flag = res['used_flag']
        next_size_flag = res['next_size_flag']
        aligned_size = res['aligned_size']
        if used_flag:
            if next_size_flag:
                gdb.execute("tel " + hex(chunkaddr+capsize*4) + " " + hex(int(aligned_size/capsize-4)))
            else:
                gdb.execute("tel " + hex(chunkaddr+capsize*2) + " " + hex(int(aligned_size/capsize-2)))
        else:
            if next_size_flag:
                gdb.execute("tel " + hex(chunkaddr+capsize*6) + " " + hex(int(aligned_size/capsize-6)))
            else:
                gdb.execute("tel " + hex(chunkaddr+capsize*4) + " " + hex(int(aligned_size/capsize-4)))
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
        __main__.unlinkable_flag = 0
        gdb.execute("ci " + hex(lst[i]))
        if lst[i+2] != -1:
            print("================================")

def allcix():
    lst = []
    getheaplist(lst)
    for i in range(len(lst)-2):
        __main__.unlinkable_flag = 0
        gdb.execute("cix " + hex(lst[i]))
        #if lst[i+2] != -1:
        #    print("==================================================================")

def new_unlinkable(chunkaddr,fd = None ,bk = None):
    if capsize == 0 :
        arch = getarch()
    try :
        cmd = "x/" + word + hex(chunkaddr + capsize)
        chunk_size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16) & 0xfffffffffffffff8
        cmd = "x/" + word + hex(chunkaddr + chunk_size)
        next_prev_size = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        if chunk_size != next_prev_size :
            #print("\033[32mUnlinkable :\033[1;31m False (corrupted size chunksize(0x%x) != prev_size(0x%x)) ) \033[37m " % (chunk_size,next_prev_size))
            tmp = "tmp"
        if not fd :
            cmd = "x/" + word + hex(chunkaddr + capsize*2)
            fd = int(gdb.execute(cmd,to_string=true).split(":")[1].strip(),16)
        if not bk :
            cmd = "x/" + word + hex(chunkaddr + capsize*3)
            bk = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(fd + capsize*3)
        fd_bk = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        cmd = "x/" + word + hex(bk + capsize*2)
        bk_fd = int(gdb.execute(cmd,to_string=True).split(":")[1].strip(),16)
        if (chunkaddr == fd_bk ) and (chunkaddr == bk_fd) :
#            print("\033[32mUnlinkable :\033[1;33m True\033[37m")
#            print("\033[32mResult of unlink :\033[37m")
            #print("\033[32m [Unlinkable]\033[37m")
            #print("\033[1;34m FD->bk (\033[1;33m*0x%x\033[1;34m) = BK (\033[1;37m0x%x ->\033[1;33m 0x%x\033[1;34m)\033[37m " % (fd+capsize*3,fd_bk,bk))
            #print("\033[1;34m BK->fd (\033[1;33m*0x%x\033[1;34m) = FD (\033[1;37m0x%x ->\033[1;33m 0x%x\033[1;34m)\033[37m " % (bk+capsize*2,bk_fd,fd))
            return [fd+capsize*3, bk+capsize*2]
        else :
            if chunkaddr != fd_bk :
                #print("\033[32mUnlinkable :\033[1;31m False (FD->bk(0x%x) != (0x%x)) \033[37m " % (fd_bk,chunkaddr))
                tmp = "tmp"
            else :
                #print("\033[32mUnlinkable :\033[1;31m False (BK->fd(0x%x) != (0x%x)) \033[37m " % (bk_fd,chunkaddr))
                tmp = "tmp"
            return [1]
    except :
        #print("\033[32mUnlinkable :\033[1;31m False (FD or BK is corruption) \033[37m ")
        tmp = "tmp"
        return [1]

