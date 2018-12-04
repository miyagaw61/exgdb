sys.path.insert(0, "%s/Pwngdb/angelheap" % PLUGINPATH)
gdb.execute("source %s/Pwngdb/pwngdb.py" % PLUGINPATH)
gdb.execute("source %s/pwngdb_init_2.py" % INITS)
