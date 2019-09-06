ExGDB
=====

ExGDB - Extension for GDB

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
* `contextmode <mode>` -- Set context mode (e.g. `contextmode reg,code`, `contextmode infonow` )
* `infox <addr>` -- Customized xinfo command of peda
* `patch <addr> <value> [size]` -- Customized patch command of peda
* `parseheap` -- Customized parseheap command of Pwngdb
* ... and all commands of peda and Pwngdb.

## Usage

### Usage when just debugging:

    $ gdb {any_binary}
    gdb-peda$ start
    gdb-peda$ contextmode infonow,code,stack
    gdb-peda$ nuntil call
    gdb-peda$ grp 'pdisass' '.*call.*'
    => 0x402a2c:    call   0x40db00
       0x402a3b:    call   0x402840 <setlocale@plt>
       0x402a4a:    call   0x4024b0 <bindtextdomain@plt>
       0x402a54:    call   0x402470 <textdomain@plt>

### Usage as a library:

    $ cat gdbrc.py
    c.start()
    c.contextmode("infonow,code,stack")
    c.nuntil("call")
    c.grp("pdisass", ".*call.*")
    $ gdb {any_binary} -x gdbrc.py

    ...

    => 0x402a2c:    call   0x40db00
       0x402a3b:    call   0x402840 <setlocale@plt>
       0x402a4a:    call   0x4024b0 <bindtextdomain@plt>
       0x402a54:    call   0x402470 <textdomain@plt>
    gdb-peda$

### Usage as a library when just debugging:

    $ gdb {any_binary}
    gdb-peda$ start
    gdb-peda$ contextmode infonow,code,stack
    gdb-peda$ nuntil call
    gdb-peda$ edit tmp.py # You must have set `$EDITOR` . And you can use `vim` or `emacs` instead of `editor` .
    gdb-peda$ cat tmp.py
    c.grp("pdisass", ".*call.*")
    gdb-peda$ source tmp.py
    => 0x402a2c:    call   0x40db00
       0x402a3b:    call   0x402840 <setlocale@plt>
       0x402a4a:    call   0x4024b0 <bindtextdomain@plt>
       0x402a54:    call   0x402470 <textdomain@plt>

## Installation:

### 1. Clone:

    $ git clone https://github.com/miyagaw61/exgdb.git /path/to/exgdb

### 2. Export EXGDBPATH

    $ cd /path/to/exgdb/
    $ export EXGDBPATH=$PWD
    $ echo "export EXGDBPATH=$PWD" >> ~/.bashrc

### 3. Install Plugin Manager (exgdbctl) :

    $ cd /path/to/exgdb
    $ cp -a ./bin/exgdbctl /usr/local/bin/

### 4. Install some plugins:

    $ exgdbctl install peda # git clone https://github.com/longld/peda.git ./plugins/peda
    $ exgdbctl install Pwngdb # git clone https://github.com/scwuaptx/Pwngdb.git ./plugins/Pwngdb

### 5. Prepare .gdbinit

    $ echo "source $(realpath gdbinit.py)" >> ~/.gdbinit

## Usage (exgdbctl) :

    usage: exgdbctl <command> [<args>]
    command: list
             install <peda/Pwngdb/ANY PLUGIN URL>
             update  <exgdb/peda/Pwngdb/ANY PLUGIN NAME>
             enable  <exgdb/peda/Pwngdb/ANY PLUGIN NAME>
             disable <exgdb/peda/Pwngdb/ANY PLUGIN NAME>

## Add New Plugin:

### 1. Prepare new plugin:

You need "{any name}.py" and "import_to_exgdb.py".

- {any name}.py: main script of your plugin.
- import_to_exgdb.py: setattr your functions to Exgdb or ExgdbCmd

    $ pwd
    /path/to/myplugin
    $ ls
    myplugin.py import_to_exgdb.py
    $ cat import_to_exgdb.py
    cmds = [cmd for cmd in dir(MyPlugin) if callable(getattr(MyPlugin, cmd))]
    for cmd in cmds:
        if not cmd.startswith("_"):
            cmd_obj = getattr(MyPlugin, cmd)
            setattr(Exgdb, cmd, cmd_obj)
    $ git remote -v
    https://github.com/username/myplugin.git
    $ git push origin master

### 2. Install your plugin:

    $ exgdbctl install https://github.com/username/myplugin.git
    $ cat $EXGDBPATH/gdbinit.py
    ・・・
    peda_is_enabled = os.path.exists("%s/peda" % pluginpath)
    pwngdb_is_enabled = os.path.exists("%s/Pwngdb" % pluginpath)
    #yourplugin_is_enabled = os.path.exists("%s/yourplugin" % pluginpath)

    if peda_is_enabled:
        __file__ = "%s/peda/peda.py" % pluginpath
        gdb.execute("source %s/peda/peda.py" % pluginpath)
    if pwngdb_is_enabled:
        sys.path.insert(0, "%s/Pwngdb/angelheap" % pluginpath)
        gdb.execute("source %s/Pwngdb/pwngdb.py" % pluginpath)
        gdb.execute("source %s/Pwngdb/angelheap/gdbinit.py" % pluginpath)
        gdb.execute("source %s/Pwngdb/angelheap/command_wrapper.py" % pluginpath)
        gdb.execute("source %s/Pwngdb/angelheap/angelheap.py" % pluginpath)
    #if yourplugin_is_enabled:
    #    gdb.execute("source %s/yourplugin/gdbinit.py" % pluginpath)

	if os.path.exists("%s/exgdb.py" % exgdbpath):
		gdb.execute("source %s/exgdb.py" % exgdbpath)
    $ vim $EXGDBPATH/gdbinit.py
    $ cat $EXGDBPATH/gdbinit.py
    ・・・
    peda_is_enabled = os.path.exists("%s/peda" % pluginpath)
    pwngdb_is_enabled = os.path.exists("%s/Pwngdb" % pluginpath)
    myplugin_is_enabled = os.path.exists("%s/myplugin" % pluginpath)

    if peda_is_enabled:
		__file__ = "%s/peda/peda.py" % pluginpath
        gdb.execute("source %s/peda/peda.py" % pluginpath)
    if pwngdb_is_enabled:
        sys.path.insert(0, "%s/Pwngdb/angelheap" % pluginpath)
        gdb.execute("source %s/Pwngdb/pwngdb.py" % pluginpath)
        gdb.execute("source %s/Pwngdb/angelheap/gdbinit.py" % pluginpath)
        gdb.execute("source %s/Pwngdb/angelheap/command_wrapper.py" % pluginpath)
        gdb.execute("source %s/Pwngdb/angelheap/angelheap.py" % pluginpath)
    if myplugin_is_enabled:
        gdb.execute("source %s/myplugin/myplugin.py" % pluginpath)

	if os.path.exists("%s/exgdb.py" % exgdbpath):
		gdb.execute("source %s/exgdb.py" % exgdbpath)

## If you have any demands or questions

Please ask everything [here](https://peing.net/ja/miyagaw61)
