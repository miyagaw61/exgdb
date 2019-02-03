Exgdb
=====

Exgdb - Extension for GDB

## New Classes:

* `Exgdb` -- This has many methods to coding debug automation script
* `ExgdbCmd` -- This has many methods that can execute as gdb command

## Methods of Exgdb:


* `read_int(addr)` -- Customized read_int of peda
* `read_int_bytes(addr, intsize=None)` -- Read bytes as intsize list
* `read_byte(addr, intsize=None)` -- Read one byte
* `read_bytes(addr, size)` -- Read bytes as any size list
* ... and all commands of peda and Pwngdb.

## Methods of ExgdbCmd:

* `ctn, c` -- Execute continue command
* `brk, b <symbol>` -- Execute break command
* `next, n, [count]` -- Execute next command
* `step, s [count]` -- Execute step command
* `nexti, ni [count]` -- Execute nexti command
* `stepi, si [count]` -- Execute stepi command
* `afterpc, af <count>` -- Show instructions after now program-counter
* `beforepc, bef <count>` -- Show instructions before now program-counter
* `grp <command> <regex>` -- Grep command output
* `allstack` -- Show all stack data
* `nuntil <regex>` -- Execute nexti command until given regexp
* `suntil <regex>` -- Execute stepi command until given regexp
* `nextcalluntil <regex>` -- Execute nextcall command until given regexp
* `stepcalluntil <regex>` -- Execute nextcall and step command until given regexp and given depth
* `infonow, inow` -- Show detail information of the instruction now specified program-counter
* `contextmode <mode>` -- Set context mode
* `infox <addr>` -- Customized xinfo command of peda
* `patch <addr> <value> [size]` -- Customized patch command of peda
* `parseheap` -- Customized parseheap command of Pwngdb
* ... and all commands of peda and Pwngdb.

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
    exgdb-peda$ python
    >c.nuntil("call.*plt") # You can use `c` suddenly if you have used `c = ExgdbCmd()` in `gdbrc.py` .
    >rsp = e.getreg("rsp") # You can use `e` suddenly if you have used `e = Exgdb()` in `gdbrc.py` .
    >print(rsp)
    > # If you finish coding, you should send Ctrl+D

    ...

    140737488345888
    exgdb-peda$ editor tmp.py # You must have set `$EDITOR` . And you can use `vim` or `emacs` instead of `editor` .
    exgdb-peda$ cat tmp.py
    while True:
        c.next()
        rax = e.getreg("rax")
        if rax == 0:
            break
    exgdb-peda$ source tmp.py

## Installation:

    $ git clone https://github.com/miyagaw61/exgdb.git
    $ cd exgdb/
    $ ./exgdbctl install expeda # git clone https://github.com/miyagaw61/expeda.git plugins/expeda
    $ ./exgdbctl install Pwngdb # git clone https://github.com/scwuaptx/Pwngdb.git plugins/Pwngdb
    $ echo "source $(realpath gdbinit.py)" >> ~/.gdbinit

## Plugin Manager:

### Installation:

    $ sudo ln -s $(realpath exgdbctl) /usr/local/bin/exgdbctl

### Usage:

    usage: exgdbctl <command> [<args>]
    command: list
             install <peda/expeda/Pwngdb/ANY PLUGIN URL>
             update  <peda/expeda/Pwngdb/ANY PLUGIN NAME>
             enable  <peda/expeda/Pwngdb/ANY PLUGIN NAME>
             disable <peda/expeda/Pwngdb/ANY PLUGIN NAME>

### Add New Plugins:

    $ cat inits/init.conf
    new_plugin_init.py NewPlugin/newplugin.py
    new_plugin_init_2.py NewPlugin2/gdbinit.py
    $ exgdbctl install https://github.com/anybody/anyplugin

## If you have any demands or questions

Please ask everything [here](https://odaibako.net/u/miyagaw61)
