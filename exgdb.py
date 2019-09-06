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
    def __init__(self):
        pass

class ExgdbCmd():
    def __init__(self):
        pass

def import_topFunctions(fname):
    cmd = r"grep -o '^def.*:' " + fname + " | sed -E 's@^def (.*)\((.*)\) *:@\\1:\\2@g'"
    stdout, stderr = Shell(cmd).readlines()
    functions = stdout
    for function in functions:
        (function_name, function_args) = function.split(":")
        if not function_name.startswith("_"):
            code = "lambda self, " + function_args + ": " + function_name + "(" + function_args + ")"
            new_function = eval(code)
            setattr(Exgdb, function_name, new_function)

def import_from_importFile():
    importFile_names = Shell("ls -1 %s/plugins/*/import_to_exgdb.py" % exgdbpath).readlines()[0]
    if len(importFile_names) < 1: return
    for importFile_name in importFile_names:
        if not File(importFile_name).exist(): continue
        plugin_name_chrs = list(importFile_name.replace("%s/plugins/" % exgdbpath, ""))
        plugin_name = ""
        for ch in plugin_name_chrs:
            if ch == "/": break
            plugin_name += ch
        if len(plugin_name) > len(".disabled") and plugin_name[-9:] == ".disabled": continue
        gdb.execute("source %s" % importFile_name)

def import_other_plugin():
    if "PwnCmd" in globals():
        import_topFunctions("%s/plugins/Pwngdb/pwngdb.py" % exgdbpath)
        import_topFunctions("%s/plugins/Pwngdb/angelheap/angelheap.py" % exgdbpath)

    if "PEDA" in globals():
        cmds = [cmd for cmd in dir(PEDA) if cmd != "SAVED_COMMANDS" and callable(getattr(PEDA, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PEDA, cmd)
                setattr(Exgdb, cmd, cmd_obj)

    if "PEDACmd" in globals():
        cmds = [cmd for cmd in dir(PEDACmd) if callable(getattr(PEDACmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PEDACmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

    if "PwnCmd" in globals():
        cmds = [cmd for cmd in dir(PwnCmd) if callable(getattr(PwnCmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(PwnCmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

    if "AngelHeapCmd" in globals():
        cmds = [cmd for cmd in dir(AngelHeapCmd) if callable(getattr(AngelHeapCmd, cmd))]
        for cmd in cmds:
            if not cmd.startswith("_"):
                cmd_obj = getattr(AngelHeapCmd, cmd)
                setattr(ExgdbCmd, cmd, cmd_obj)

    import_from_importFile()

class ExgdbCmdWrapper(gdb.Command):
    """ Exgdb command wrapper """
    def __init__(self):
        super(ExgdbCmdWrapper,self).__init__("exgdb",gdb.COMMAND_USER)

    def invoke(self,args,from_tty):
        self.dont_repeat()
        arg = args.split()
        if len(arg) > 0 :
            cmd = arg[0]
            if cmd in c.commands :
                func = getattr(c,cmd)
                func(*arg[1:])
            else :
                print("Unknown command")
        else :
            print("Unknown command")
        return 

class ExgdbAlias(gdb.Command):
    """ Exgdb Alias """
    def __init__(self,alias,command):
        self.command = command
        super(ExgdbAlias,self).__init__(alias,gdb.COMMAND_NONE)

    def invoke(self,args,from_tty):
        self.dont_repeat()
        gdb.execute("%s %s" % (self.command,args))

import_other_plugin()
gdb.execute("source %s/exgdbmethods.py" % exgdbpath)
gdb.execute("source %s/exgdbcmdmethods.py" % exgdbpath)
gdb.execute("source %s/initialize.py" % exgdbpath)
