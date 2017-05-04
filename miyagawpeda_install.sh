#!/bin/sh
apt-get install -y git  
git clone https://github.com/longld/peda.git ~/peda  
#git clone https://github.com/miyagaw61/miyagawpeda.git ~/peda/miyagawpeda
line=$(cat ~/peda/peda.py | grep -n "def xprint" | sed -E "s/(.*):.*:/\1/g")
head -n $((${line} - 1)) ~/peda/peda.py | tail -n $((${line} - 1)) > ~/peda/miyagawpeda/peda.before.txt
head -n $(cat ~/peda/peda.py | wc -l) ~/peda/peda.py | tail -n $(($(cat ~/peda/peda.py | wc -l) - ${line} + 1)) > ~/peda/miyagawpeda/peda.after.txt
cp -a ~/peda/miyagawpeda/peda.before.txt ~/peda/miyagawpeda/miyagawpeda.py
if test "$(uname -a | grep 'x86_64')" ;then
	cat ~/peda/miyagawpeda/miyagawpeda64.txt >> ~/peda/miyagawpeda/miyagawpeda.py
else
	cat ~/peda/miyagawpeda/miyagawpeda32.txt >> ~/peda/miyagawpeda/miyagawpeda.py
fi
cat ~/peda/miyagawpeda/miyagawpeda.after.txt >> ~/peda/miyagawpeda/miyagawpeda.py
cat ~/peda/miyagawpeda/miyagawpeda.alias.txt >> ~/peda/miyagawpeda/miyagawpeda.py
#rm -rf ~/peda/miyagawpeda/
cat ~/peda/miyagawpeda/miyagawgdbinit >> ~/.gdbinit
