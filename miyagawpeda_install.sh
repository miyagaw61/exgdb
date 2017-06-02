#!/bin/sh
if test ! -e $HOME/peda/ ;then
	git clone https://github.com/longld/peda.git $HOME/peda  
fi
line=$(cat $HOME/peda/peda.py | grep -n "def xprint" | sed -E "s/(.*):.*:/\1/g")
if test ! -e $HOME/peda/miyagawpeda/ ;then
	mkdir $HOME/peda/miyagawpeda/
fi
cp -a "$(pwd)"/miyagawpeda64.txt $HOME/peda/miyagawpeda/
cp -a "$(pwd)"/miyagawpeda32.txt $HOME/peda/miyagawpeda/
cp -a "$(pwd)"/miyagawpeda.alias.txt $HOME/peda/miyagawpeda/
head -n $((${line} - 1)) $HOME/peda/peda.py | tail -n $((${line} - 1)) > $HOME/peda/miyagawpeda/peda.before.txt
head -n $(cat $HOME/peda/peda.py | wc -l) $HOME/peda/peda.py | tail -n $(($(cat $HOME/peda/peda.py | wc -l) - ${line} + 1)) > $HOME/peda/miyagawpeda/peda.after.txt
cp -a $HOME/peda/miyagawpeda/peda.before.txt $HOME/peda/miyagawpeda/miyagawpeda.py
if test "$(uname -a | grep 'x86_64')" ;then
	cat $HOME/peda/miyagawpeda/miyagawpeda64.txt >> $HOME/peda/miyagawpeda/miyagawpeda.py
else
	cat $HOME/peda/miyagawpeda/miyagawpeda32.txt >> $HOME/peda/miyagawpeda/miyagawpeda.py
fi
cat $HOME/peda/miyagawpeda/peda.after.txt >> $HOME/peda/miyagawpeda/miyagawpeda.py
cat $HOME/peda/miyagawpeda/miyagawpeda.alias.txt >> $HOME/peda/miyagawpeda/miyagawpeda.py
cp "$(pwd)"/miyagawgdbinit $HOME/.gdbinit
