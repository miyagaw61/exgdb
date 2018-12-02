# Promote useful stuff to toplevel

try:
    from .toplevel import *
    pwnlib3.args.initialize()
    pwnlib3.log.install_default_handler()
    log = pwnlib3.log.getLogger('pwnlib3.exploit')
    args = pwnlib3.args.args
except:
    print('[+]Try this:\npip install git+https://github.com/miyagaw61/pwnlib3#egg=pwnlib3')
