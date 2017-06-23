#!/bin/sh
if test ! -e $HOME/peda/ ;then
	git clone https://github.com/longld/peda.git $HOME/peda  
fi
line=$(cat $HOME/peda/peda.py | grep -n "def xprint" | sed -E "s/(.*):.*:/\1/g")
if test ! -e $HOME/peda/mgpeda/ ;then
	mkdir $HOME/peda/mgpeda/
fi
cp -a "$(pwd)"/mgpeda64.txt $HOME/peda/mgpeda/
cp -a "$(pwd)"/mgpeda32.txt $HOME/peda/mgpeda/
cp -a "$(pwd)"/mgpeda.alias.txt $HOME/peda/mgpeda/
head -n $((${line} - 1)) $HOME/peda/peda.py | tail -n $((${line} - 1)) > $HOME/peda/mgpeda/peda.before.txt
head -n $(cat $HOME/peda/peda.py | wc -l) $HOME/peda/peda.py | tail -n $(($(cat $HOME/peda/peda.py | wc -l) - ${line} + 1)) > $HOME/peda/mgpeda/peda.after.txt
cp -a $HOME/peda/mgpeda/peda.before.txt $HOME/peda/mgpeda/mgpeda.py
if test "$(uname -a | grep 'x86_64')" ;then
	cat $HOME/peda/mgpeda/mgpeda64.txt >> $HOME/peda/mgpeda/mgpeda.py
else
	cat $HOME/peda/mgpeda/mgpeda32.txt >> $HOME/peda/mgpeda/mgpeda.py
fi
cat $HOME/peda/mgpeda/peda.after.txt >> $HOME/peda/mgpeda/mgpeda.py
cat $HOME/peda/mgpeda/mgpeda.alias.txt >> $HOME/peda/mgpeda/mgpeda.py
cp "$(pwd)"/mggdbinit $HOME/.gdbinit
