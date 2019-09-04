import os
import sys
import re
import gdb
RE_BLUE = re.compile(r";34m")

EXGDBFILE = os.path.abspath(os.path.expanduser(__file__))
sys.path.insert(0, os.path.dirname(EXGDBFILE) + "/lib/")

from enert import *
import utils
import exutils

class Exgdb():
    def __init__(self):
        pass

class ExgdbCmd():
    def __init__(self):
        pass

def import_other_plugin():
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
gdb.execute("source ./exgdbmethods.py")
gdb.execute("source ./exgdbcmdmethods.py")
gdb.execute("source ./initialize.py")
