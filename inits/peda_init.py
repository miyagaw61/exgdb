is_expeda = os.path.exists("%s/expeda" % PLUGINPATH)
is_peda = os.path.exists("%s/peda" % PLUGINPATH)
is_pwngdb = os.path.exists("%s/Pwngdb" % PLUGINPATH)

if is_expeda:
    gdb.execute("source %s/expeda/peda.py" % PLUGINPATH)
    if not is_pwngdb:
        gdb.execute("source %s/exgdb_init.py" % INITS)
elif is_peda:
    gdb.execute("source %s/peda/peda.py" % PLUGINPATH)
    if not is_pwngdb:
        gdb.execute("source %s/exgdb_init.py" % INITS)
if is_pwngdb:
    gdb.execute("source %s/pwngdb_init_1.py" % INITS)
else:
    gdb.execute("source %s/exgdb_init.py" % INITS)
