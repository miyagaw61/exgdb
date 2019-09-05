import os
import sys

exgdbpath = os.environ.get("EXGDBPATH")
if exgdbpath == None:
    print("Please export $EXGDBPATH")
    exit()
pluginpath = exgdbpath + "/plugins"

expeda_is_enabled = os.path.exists("%s/expeda" % pluginpath)
peda_is_enabled = os.path.exists("%s/peda" % pluginpath)
pwngdb_is_enabled = os.path.exists("%s/Pwngdb" % pluginpath)
#yourplugin_is_enabled = os.path.exists("%s/yourplugin" % pluginpath)

if expeda_is_enabled:
    sys.path.insert(0, "%s/expeda/lib/" % pluginpath)
    gdb.execute("source %s/expeda/peda.py" % pluginpath)
elif peda_is_enabled:
    gdb.execute("source %s/peda/peda.py" % pluginpath)
if pwngdb_is_enabled:
    sys.path.insert(0, "%s/Pwngdb/angelheap" % pluginpath)
    gdb.execute("source %s/Pwngdb/pwngdb.py" % pluginpath)
    gdb.execute("source %s/Pwngdb/angelheap/gdbinit.py" % pluginpath)
    gdb.execute("source %s/Pwngdb/angelheap/command_wrapper.py" % pluginpath)
    gdb.execute("source %s/Pwngdb/angelheap/angelheap.py" % pluginpath)
#if yourplugin_is_enabled:
#    gdb.execute("source %s/yourplugin/gdbinit.py" % pluginpath)

gdb.execute("source %s/exgdb.py" % exgdbpath)
