import os
import sys
import re
import gdb
RE_BLUE = re.compile(r";34m")

exgdbpath = os.environ.get("EXGDBPATH")
if exgdbpath == None:
    print("Please export $EXGDBPATH")
    exit()
sys.path.insert(0, exgdbpath + "/lib/")

from enert import *
import utils
import exutils

class Exgdb():
    THISDIR = ""
    def __init__(self):
        pass

class ExgdbCmd():
    def __init__(self):
        pass

def import_topFunctions(fname):
    cmd = "grep -o '^def.*:' " + fname + " | sed -E 's@^def (.*)\((.*)\) *:@\\1:\\2@g'"
    stdout, stderr = Shell(cmd).readlines()
    functions = stdout
    for function in functions:
        (function_name, function_args) = function.split(":")
        if function_name.startswith("_"):
            continue
        if hasattr(ExgdbCmd, function_name):
            continue
        if hasattr(gdb.Command, function_name):
            continue
        code = "lambda self, " + function_args + ": " + function_name + "(" + function_args + ")"
        new_function = eval(code)
        setattr(Exgdb, function_name, new_function)

def import_from_exportFile():
    exportFile_paths = Shell("ls -1 %s/plugins/*/export_to_exgdb.py" % exgdbpath).readlines()[0]
    if len(exportFile_paths) < 1: return
    for exportFile_path in exportFile_paths:
        if not File(exportFile_path).exist(): continue
        plugin_name_chrs = list(exportFile_path.replace("%s/plugins/" % exgdbpath, ""))
        plugin_name = ""
        for ch in plugin_name_chrs:
            if ch == "/": break
            plugin_name += ch
        if len(plugin_name) > len(".disabled") and plugin_name[-9:] == ".disabled": continue
        Exgdb.THISDIR = "%s/plugins/%s" % (exgdbpath, plugin_name)
        gdb.execute("source %s" % exportFile_path)

def import_other_plugins():
    if "PwnCmd" in globals():
        import_topFunctions("%s/plugins/Pwngdb/pwngdb.py" % exgdbpath)
        import_topFunctions("%s/plugins/Pwngdb/angelheap/angelheap.py" % exgdbpath)

    if "PEDA" in globals():
        cmds = [cmd for cmd in dir(PEDA) if cmd != "SAVED_COMMANDS" and callable(getattr(PEDA, cmd))]
        cmd_to_get_exgdb_functions = "grep -o ' *def.*:' %s/exgdbmethods.py | sed -E 's@ *def (.*)\((.*)\) *:@\\1:\\2@g'" % exgdbpath
        stdout, stderr = Shell(cmd_to_get_exgdb_functions).readlines()
        exgdb_functions = stdout
        exgdb_functions = list(map(lambda x: x.split(":")[0], exgdb_functions))
        for cmd in cmds:
            if cmd.startswith("_"):
                continue
            if hasattr(ExgdbCmd, cmd):
                continue
            if hasattr(gdb.Command, cmd):
                continue
            if cmd in exgdb_functions:
                continue
            cmd_obj = getattr(PEDA, cmd)
            setattr(Exgdb, cmd, cmd_obj)

    if "PEDACmd" in globals():
        cmds = [cmd for cmd in dir(PEDACmd) if callable(getattr(PEDACmd, cmd))]
        cmd_to_get_exgdb_functions = "grep -o ' *def.*:' %s/exgdbcmdmethods.py | sed -E 's@ *def (.*)\((.*)\) *:@\\1:\\2@g'" % exgdbpath
        stdout, stderr = Shell(cmd_to_get_exgdb_functions).readlines()
        exgdb_functions = stdout
        exgdb_functions = list(map(lambda x: x.split(":")[0], exgdb_functions))
        for cmd in cmds:
            if cmd.startswith("_"):
                continue
            if hasattr(ExgdbCmd, cmd):
                continue
            if hasattr(gdb.Command, cmd):
                continue
            if cmd in exgdb_functions:
                continue
            cmd_obj = getattr(PEDACmd, cmd)
            setattr(ExgdbCmd, cmd, cmd_obj)

    if "PwnCmd" in globals():
        cmds = [cmd for cmd in dir(PwnCmd) if callable(getattr(PwnCmd, cmd))]
        for cmd in cmds:
            if cmd.startswith("_"):
                continue
            if hasattr(ExgdbCmd, cmd):
                continue
            if hasattr(gdb.Command, cmd):
                continue
            cmd_obj = getattr(PwnCmd, cmd)
            setattr(ExgdbCmd, cmd, cmd_obj)

    if "AngelHeapCmd" in globals():
        cmds = [cmd for cmd in dir(AngelHeapCmd) if callable(getattr(AngelHeapCmd, cmd))]
        for cmd in cmds:
            if cmd.startswith("_"):
                continue
            if hasattr(ExgdbCmd, cmd):
                continue
            if hasattr(gdb.Command, cmd):
                continue
            cmd_obj = getattr(AngelHeapCmd, cmd)
            setattr(ExgdbCmd, cmd, cmd_obj)

    if "dashboard" in globals():
        import_topFunctions("%s/plugins/gdb-dashboard/.gdbinit" % exgdbpath)
        setattr(ExgdbCmd, "dashboard", dashboard)

    import_from_exportFile()

class ExgdbCmdWrapper(gdb.Command):
    def __init__(self):
        super(ExgdbCmdWrapper,self).__init__("exgdb",gdb.COMMAND_USER)

    def invoke(self,arg,from_tty):
        self.dont_repeat()
        args = e.string_to_argv(arg)
        if len(args) > 0 :
            cmd = args[0]
            if cmd in c.cmds:
                func = getattr(c,cmd)
                if len(args) == 1:
                    func()
                else:
                    func(*args[1:])
            else :
                print("Unknown command")
        else :
            print("Unknown command")
        return

class ExgdbAlias(gdb.Command):
    def __init__(self,alias,command):
        self.command = command
        super(ExgdbAlias,self).__init__(alias,gdb.COMMAND_NONE)

    def invoke(self,args,from_tty):
        self.dont_repeat()
        gdb.execute("%s %s" % (self.command,args))

class RepeatExgdbCmdWrapper(gdb.Command):
    def __init__(self):
        super(RepeatExgdbCmdWrapper,self).__init__("rexgdb",gdb.COMMAND_USER)

    def invoke(self,arg,from_tty):
        #self.dont_repeat()
        args = e.string_to_argv(arg)
        if len(args) > 0 :
            cmd = args[0]
            if cmd in c.repeat_cmds:
                func = getattr(c,cmd)
                if len(args) == 1:
                    func()
                else:
                    func(*args[1:])
            else :
                print("Unknown command")
        else :
            print("Unknown command")
        return

class RepeatExgdbAlias(gdb.Command):
    def __init__(self,alias,command):
        self.command = command
        super(RepeatExgdbAlias,self).__init__(alias,gdb.COMMAND_NONE)

    def invoke(self,args,from_tty):
        #self.dont_repeat()
        gdb.execute("%s %s" % (self.command,args))

import_other_plugins()
gdb.execute("source %s/exgdbmethods.py" % exgdbpath)
gdb.execute("source %s/exgdbcmdmethods.py" % exgdbpath)
gdb.execute("source %s/initialize.py" % exgdbpath)
