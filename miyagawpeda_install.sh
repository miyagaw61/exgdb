#!/bin/sh
if test ! -e ~/peda/ ;then
	git clone https://github.com/longld/peda.git ~/peda  
fi
line=$(cat ~/peda/peda.py | grep -n "def xprint" | sed -E "s/(.*):.*:/\1/g")
mkdir ~/peda/miyagawpeda/
head -n $((${line} - 1)) ~/peda/peda.py | tail -n $((${line} - 1)) > ~/peda/miyagawpeda/peda.before.txt
head -n $(cat ~/peda/peda.py | wc -l) ~/peda/peda.py | tail -n $(($(cat ~/peda/peda.py | wc -l) - ${line} + 1)) > ~/peda/miyagawpeda/peda.after.txt
cp -a ~/peda/miyagawpeda/peda.before.txt ~/peda/miyagawpeda/miyagawpeda.py
if test "$(uname -a | grep 'x86_64')" ;then
	cat miyagawpeda64.txt >> ~/peda/miyagawpeda/miyagawpeda.py
else
	cat miyagawpeda32.txt >> ~/peda/miyagawpeda/miyagawpeda.py
fi
cat ~/peda/miyagawpeda/peda.after.txt >> ~/peda/miyagawpeda/miyagawpeda.py
cat miyagawpeda.alias.txt >> ~/peda/miyagawpeda/miyagawpeda.py
cp miyagawgdbinit ~/.gdbinit
