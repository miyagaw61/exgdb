def load_to_exgdb():
    cmds = [cmd for cmd in dir(ExgdbMethods) if callable(getattr(ExgdbMethods, cmd))]
    for cmd in cmds:
        if cmd.startswith("_"):
            continue
        if hasattr(ExgdbCmd, cmd):
            continue
        if hasattr(gdb.Command, cmd):
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
#
#exgdb_context = ExgdbContext()

if "dashboard" in globals():
    def return_emptystr():
        return ""

    #Dashboard.clear_screen = return_emptystr
    #gdb.events.stop.disconnect(dashboard.on_stop)
    #gdb.events.cont.disconnect(dashboard.on_continue)
    #gdb.events.exited.disconnect(dashboard.on_exit)
    #c.contextmode("reg,code,src,stack,bt,thr")

    #e.define_user_command("hook-stop", "exgdb context\n" "session autosave")

    utils.clearscreen = return_emptystr
    c.contextmode("reg,stack")
    #c.contextmode("none")
