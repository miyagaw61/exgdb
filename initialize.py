def load_to_exgdb():
    """
    Load exgdb commands.

    Args:
    """
    cmds = [cmd for cmd in dir(ExgdbMethods) if callable(getattr(ExgdbMethods, cmd)) and not cmd.startswith("_")]
    for cmd in cmds:
        setattr(Exgdb, cmd, getattr(ExgdbMethods, cmd))

def load_to_exgdbcmd():
    """
    Returns a command line arguments.

    Args:
    """
    cmds = [cmd for cmd in dir(ExgdbCmdMethods) if callable(getattr(ExgdbCmdMethods, cmd)) and not cmd.startswith("_")]
    for cmd in cmds:
        setattr(ExgdbCmd, cmd, getattr(ExgdbCmdMethods, cmd))
    return cmds

def register_gdbcmd():
    """
    Register gdb command.

    Args:
    """
    for cmd in c.cmds:
        if not cmd in ["next", "step", "nexti", "stepi", "n", "s", "ni", "si", "start"]:
            ExgdbAlias(cmd,"exgdb %s" % cmd)
    ExgdbCmdWrapper()

def register_repeat_gdbcmd():
    """
    Register the repeat command. gdb command.

    Args:
    """
    for cmd in c.repeat_cmds:
        RepeatExgdbAlias(cmd,"rexgdb %s" % cmd)
    RepeatExgdbCmdWrapper()

load_to_exgdb()
cmds = load_to_exgdbcmd()

e = Exgdb()
c = ExgdbCmd()
c.cmds = cmds
c.repeat_cmds = ["radvance", "rad"]

register_gdbcmd()
register_repeat_gdbcmd()
