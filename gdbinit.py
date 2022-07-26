import os
import sys

exgdbpath = os.environ.get("EXGDBPATH")
if exgdbpath == None:
    print("Please export $EXGDBPATH")
    exit()
pluginpath = exgdbpath + "/plugins"

exgdb_is_enabled = os.path.exists("%s/exgdb.py" % exgdbpath)
peda_is_enabled = os.path.exists("%s/peda" % pluginpath)
pwngdb_is_enabled = os.path.exists("%s/Pwngdb" % pluginpath)
dashboard_is_enabled = os.path.exists("%s/gdb-dashboard" % pluginpath)

if peda_is_enabled:
    __file__ = "%s/peda/peda.py" % pluginpath
    gdb.execute("source %s/peda/peda.py" % pluginpath)
if pwngdb_is_enabled:
    sys.path.insert(0, "%s/Pwngdb/angelheap" % pluginpath)
    gdb.execute("source %s/Pwngdb/pwngdb.py" % pluginpath)
    gdb.execute("source %s/Pwngdb/angelheap/gdbinit.py" % pluginpath)
    gdb.execute("source %s/Pwngdb/angelheap/command_wrapper.py" % pluginpath)
    gdb.execute("source %s/Pwngdb/angelheap/angelheap.py" % pluginpath)
if dashboard_is_enabled:
    gdb.execute("source %s/gdb-dashboard/.gdbinit" % pluginpath)

if exgdb_is_enabled:
    gdb.execute("source %s/exgdb.py" % exgdbpath)

if exgdb_is_enabled and peda_is_enabled and dashboard_is_enabled:
    gdb.execute("contextmode")
