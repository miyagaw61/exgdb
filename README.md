Exgdb
=====

Exgdb - Extension for GDB

## New Key Features:

* `ctn, c` -- Execute continue command
* `brk, b` -- Execute break command
* `next, n` -- Execute next command
* `step, s` -- Execute step command
* `nexti, ni` -- Execute nexti command
* `stepi, si` -- Execute stepi command
* `afterpc, af` -- Show instructions after now program-counter
* `beforepc, bef` -- Show instructions before now program-counter
* `grp` -- Grep command output
* `allstack` -- Show all stack data
* `nuntil` -- Execute nexti command until given regexp
* `suntil` -- Execute stepi command until given regexp
* `nextcalluntil` -- Execute nextcall command until given regexp
* `stepcalluntil` -- Execute nextcall and step command until given regexp and given depth
* `infonow, inow` -- Show detail information of the instruction now specified program-counter
* `infox` -- Customed xinfo command
* `contextmode` -- Set context mode
* ... and all commands of peda.

## Usage as a library:

    $ cat gdbrc.py
    e = Exgdb()
    c = ExgdbCmd()
    c.start()
    c.nuntil("call")
    c.grp("afterpc 10", ".*call.*")
    $ gdb /bin/ls -x gdbrc.py

    ...

    => 0x402a2c:    call   0x40db00
       0x402a3b:    call   0x402840 <setlocale@plt>
       0x402a4a:    call   0x4024b0 <bindtextdomain@plt>
       0x402a54:    call   0x402470 <textdomain@plt>
    exgdb-peda$ 

## Usage when just debugging:

    $ gdb /bin/ls -x gdbrc.py

    ...

    => 0x402a2c:    call   0x40db00
       0x402a3b:    call   0x402840 <setlocale@plt>
       0x402a4a:    call   0x4024b0 <bindtextdomain@plt>
       0x402a54:    call   0x402470 <textdomain@plt>
    gdb-expeda$ editor tmp.py # You must have set `$EDITOR` . And you can use `vim` or `emacs` instead of `editor` .
    gdb-expeda$ cat tmp.py
    while True:
        c.next() # You can use `e` and `c` suddenly if you have used `e = Exgdb()` and `c = ExgdbCmd()` in `gdbrc.py` .
        eax = e.getreg("eax")
        if eax == 0:
            break
    exgdb-peda$ source tmp.py

## Installation:

    $ git clone https://github.com/miyagaw61/exgdb.git /path/to/exgdb
    $ echo "source /path/to/exgdb/gdbinit.py" >> ~/.gdbinit
