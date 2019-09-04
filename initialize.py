def load_to_exgdb():
    cmds = [cmd for cmd in dir(ExgdbMethods) if callable(getattr(ExgdbMethods, cmd)) and not cmd.startswith("_")]
    for cmd in cmds:
        setattr(Exgdb, cmd, getattr(ExgdbMethods, cmd))

def load_to_exgdbcmd():
    cmds = [cmd for cmd in dir(ExgdbCmdMethods) if callable(getattr(ExgdbCmdMethods, cmd)) and not cmd.startswith("_")]
    for cmd in cmds:
        setattr(ExgdbCmd, cmd, getattr(ExgdbCmdMethods, cmd))
    return cmds

def register_gdbcmd(exgdbcmd, cmds):
    exgdbcmd.commands = cmds
    for cmd in exgdbcmd.commands :
        if not cmd in ["next", "step", "nexti", "stepi", "n", "s", "ni", "si"]:
            ExgdbAlias(cmd,"exgdb %s" % cmd)
    ExgdbCmdWrapper()

load_to_exgdb()
cmds = load_to_exgdbcmd()

e = Exgdb()
c = ExgdbCmd()

register_gdbcmd(c, cmds)
