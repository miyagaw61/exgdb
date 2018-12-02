import os

THISFILE = os.path.abspath(os.path.expanduser(__file__))
EXGDBPATH = os.path.dirname(THISFILE)
INITS = EXGDBPATH + "/inits"
PLUGINPATH = EXGDBPATH + "/plugins"

gdb.execute("source %s/peda_init.py" % INITS)
