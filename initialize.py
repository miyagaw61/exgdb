def load_to_exgdb():
    cmds = [cmd for cmd in dir(ExgdbMethods) if callable(getattr(ExgdbMethods, cmd))]
    for cmd in cmds:
        if cmd.startswith("_"):
            continue
        if hasattr(Exgdb, cmd):
            continue
        setattr(Exgdb, cmd, getattr(ExgdbMethods, cmd))

def load_to_exgdbcmd():
    cmds = [cmd for cmd in dir(ExgdbCmdMethods) if callable(getattr(ExgdbCmdMethods, cmd))]
    for cmd in cmds:
        if cmd.startswith("_"):
            continue
        if hasattr(ExgdbCmd, cmd):
            continue
        if hasattr(gdb.Command, cmd):
            print(cmd)
            continue
        setattr(ExgdbCmd, cmd, getattr(ExgdbCmdMethods, cmd))
    return cmds

def register_gdbcmd():
    for cmd in c.cmds:
        if not cmd in ["next", "step", "nexti", "stepi", "n", "s", "ni", "si", "start"]:
            ExgdbAlias(cmd,"exgdb %s" % cmd)
    ExgdbCmdWrapper()

def register_repeat_gdbcmd():
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

#class ExgdbContext(gdb.Command):
#    def __init__(self):
#        pass
#    def on_stop(self, _):
#        #dashboard.on_stop(_)
#        #c.context_stack()
#        c.context()

if "dashboard" in globals():
    #Dashboard.clear_screen = exutils.return_emptystr
    utils.clearscreen = exutils.return_emptystr
    gdb.events.stop.disconnect(dashboard.on_stop)
    lang = e.get_lang()
    c.contextmode("c", "peda_dashboard")
    c.contextmode("rust", "dashboard")
elif "PEDA" in globals():
    c.contextmode("c", "peda")
    c.contextmode("rust", "peda")

e.define_user_command("hook-stop", "exgdb context\n" "session autosave")
