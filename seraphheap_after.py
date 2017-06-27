
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
        sys.stdout.write(green(to_hex(chunkaddr), "bold"))
        for i in range(12 - len(hex(chunkaddr))):
            sys.stdout.write(" ")
        if status:
            if chunkaddr in fastchunk :
                #print("\033[1;32mStatus : \033[1;34m Freed (fast) \033[37m")
                sys.stdout.write(blue("Freed", "bold"))
            else :
                #print("\033[1;32mStatus : \033[31m Used \033[37m")
                sys.stdout.write(red("Used ", "bold"))
        #else :
        if not status:
            #print("\033[1;32mStatus : \033[1;34m Freed \033[37m")
            sys.stdout.write(blue("Freed", "bold"))
            #unlinkable(chunkaddr,fd,bk)
        #print("\033[32mprev_size :\033[37m 0x%x                  " % prev_size)
        sys.stdout.write("    ")
        sys.stdout.write(hex(prev_size))
        #print("\033[32msize :\033[37m 0x%x                  " % (size & 0xfffffffffffffff8))
        for i in range(9 - len(hex(prev_size))):
            sys.stdout.write(" ")
        realsize = size & 0xfffffffffffffff8
        sys.stdout.write(hex(realsize))
        #print("\033[32mprev_inused :\033[37m %x                    " % (size & 1) )
        for i in range(9 - len(hex(realsize))):
            sys.stdout.write(" ")
        pi = size & 1
        if(pi == 1):
            sys.stdout.write(str(1))
        else:
            sys.stdout.write(str(0))
        #sys.stdout.write(hex(pi))
        #print("\033[32mis_mmap :\033[37m %x                    " % (size & 2) )
        sys.stdout.write("     ")
        im = size & 2
        if(im == 2):
            sys.stdout.write(str(1))
        else:
            sys.stdout.write(str(0))
        #sys.stdout.write(hex(im))
        #print("\033[32mnon_mainarea :\033[37m %x                     " % (size & 4) )
        sys.stdout.write("     ")
        nm = size & 4
        if(nm == 4):
            sys.stdout.write(str(1))
        else:
            sys.stdout.write(str(0))
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
            print("")
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

def parseh():
    print(yellow("addr        status   prev     size     PI    IM    NM    fd          bk         ", "bold"))
    if capsize == 0 :
        arch = getarch()
    addr = pwngdb.getheapbase()
    addr = infoh(addr)
    while(addr != -1):
        addr = infoh(addr)

