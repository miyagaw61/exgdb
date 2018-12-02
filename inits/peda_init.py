if os.path.exists("%s/expeda" % PLUGINPATH):
    gdb.execute("source %s/expeda/peda.py" % PLUGINPATH)
elif os.path.exists("%s/peda" % PLUGINPATH):
    gdb.execute("source %s/peda/peda.py" % PLUGINPATH)
if os.path.exists("%s/Pwngdb" % PLUGINPATH):
    gdb.execute("source %s/pwngdb_init_1.py" % INITS)
