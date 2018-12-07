#!/bin/sh

if test ! -e ./install.sh ;then
    echo "Please < cd /path/to/exgdb ; ./install.sh >"
    exit 0
fi
apt -y update
apt -y install gdb
now=$(pwd)
#apt-get -y install libc6-dbg
#apt-get -y install libc6-dbg:i386
if test ! -e $HOME/peda/ ;then
	#git clone https://github.com/scwuaptx/peda.git $HOME/peda  
    git clone https://github.com/longld/peda $HOME/peda
fi
if test ! -e $HOME/Pwngdb/ ;then
	git clone https://github.com/scwuaptx/Pwngdb.git $HOME/Pwngdb
fi
line=$(cat $HOME/peda/peda.py | grep -n "def xprint" | sed -E "s/(.*):.*:/\1/g")
if test ! -e $HOME/peda/exgdb/ ;then
	mkdir $HOME/peda/exgdb/
fi
#cp -a "$(pwd)"/exgdb64.txt $HOME/peda/exgdb/
cp -a "$(pwd)"/exgdb_code.py $HOME/peda/exgdb/
#cp -a "$(pwd)"/exgdb32.txt $HOME/peda/exgdb/
cp -a "$(pwd)"/exgdb.alias.txt $HOME/peda/exgdb/
head -n $((${line} - 1)) $HOME/peda/peda.py | tail -n $((${line} - 1)) > $HOME/peda/exgdb/peda.before.txt
head -n $(cat $HOME/peda/peda.py | wc -l) $HOME/peda/peda.py | tail -n $(($(cat $HOME/peda/peda.py | wc -l) - ${line} + 1)) > $HOME/peda/exgdb/peda.after.txt
cp -a $HOME/peda/exgdb/peda.before.txt $HOME/peda/exgdb/exgdb.py
#if test "$(uname -a | grep 'x86_64')" ;then
	#cat $HOME/peda/exgdb/exgdb64.txt >> $HOME/peda/exgdb/exgdb.py
cat $HOME/peda/exgdb/exgdb_code.py >> $HOME/peda/exgdb/exgdb.py
#else
#	cat $HOME/peda/exgdb/exgdb32.txt >> $HOME/peda/exgdb/exgdb.py
#fi
cat $HOME/peda/exgdb/peda.after.txt >> $HOME/peda/exgdb/exgdb.py
cat $HOME/peda/exgdb/exgdb.alias.txt >> $HOME/peda/exgdb/exgdb.py

cat $HOME/peda/exgdb/exgdb.py | perl -pe "s@if not self._is_running\(\)@if\(1==2\)@g" > $HOME/peda/exgdb/exgdb.tmp
cat $HOME/peda/exgdb/exgdb.tmp | perl -pe "s@if not pid@if\(1==2\)@g" > $HOME/peda/exgdb/exgdb.py
cat $HOME/peda/exgdb/exgdb.py | perl -pe "s@if self._is_running\(\):@if\(1==1\):@g" > $HOME/peda/exgdb/exgdb.tmp
 
### getpid=$(cat getpid.txt)
### cat $HOME/peda/exgdb/exgdb.tmp | perl -pe "s@if not pid@"$getpid"@g" > $HOME/peda/exgdb/exgdb.tmp2
### cat $HOME/peda/exgdb/exgdb.tmp2 | perl -pe "s@TMPSPACE@ @g" > $HOME/peda/exgdb/exgdb.tmp
### cat $HOME/peda/exgdb/exgdb.tmp | perl -pe "s@TMP2SPACE@        @g" > $HOME/peda/exgdb/exgdb.tmp2
### cat $HOME/peda/exgdb/exgdb.tmp2 | perl -pe "s@TMP3SPACE@            @g" > $HOME/peda/exgdb/exgdb.py
mv $HOME/peda/exgdb/exgdb.tmp $HOME/peda/exgdb/exgdb.py

if test ! -e $HOME/Pwngdb/angelheap/exgdb/ ;then
	mkdir $HOME/Pwngdb/angelheap/exgdb/
fi
cat $HOME/Pwngdb/angelheap/angelheap.py | head -4 > $HOME/Pwngdb/angelheap/exgdb/angelheap.py
cat "$(pwd)"/seraphheap_before.py >> $HOME/Pwngdb/angelheap/exgdb/angelheap.py
cat $HOME/Pwngdb/angelheap/angelheap.py | grep -A$(cat $HOME/Pwngdb/angelheap/angelheap.py | wc -l) "import gdb" >> $HOME/Pwngdb/angelheap/exgdb/angelheap.py
cat "$(pwd)"/seraphheap_after.py >> $HOME/Pwngdb/angelheap/exgdb/angelheap.py
line=$(cat $HOME/Pwngdb/angelheap/command_wrapper.py | grep -n "class AngelHeapCmdWrapper" | sed -E "s/(.*):.*:/\1/g")
echo "import sys" > $HOME/Pwngdb/angelheap/exgdb/command_wrapper.py
echo 'sys.path.append("/home/miyagaw61/Pwngdb")' >> $HOME/Pwngdb/angelheap/exgdb/command_wrapper.py
echo "import pwngdb" >> $HOME/Pwngdb/angelheap/exgdb/command_wrapper.py

head -n $((${line} - 1)) $HOME/Pwngdb/angelheap/command_wrapper.py | tail -n $((${line} - 1)) >> $HOME/Pwngdb/angelheap/exgdb/command_wrapper.py
head -n $(cat $HOME/Pwngdb/angelheap/command_wrapper.py | wc -l) $HOME/Pwngdb/angelheap/command_wrapper.py | tail -n $(($(cat $HOME/Pwngdb/angelheap/command_wrapper.py | wc -l) - ${line} + 1)) >> $HOME/Pwngdb/angelheap/exgdb/command_wrapper_after.py
cat "$(pwd)"/command_wrapper_for_exgdb.py >> $HOME/Pwngdb/angelheap/exgdb/command_wrapper.py
cat $HOME/Pwngdb/angelheap/exgdb/command_wrapper_after.py >> $HOME/Pwngdb/angelheap/exgdb/command_wrapper.py
rm $HOME/Pwngdb/angelheap/exgdb/command_wrapper_after.py
cp -a $HOME/Pwngdb/angelheap/gdbinit.py $HOME/Pwngdb/angelheap/exgdb/
cp  -a $HOME/Pwngdb/pwngdb.py $HOME/Pwngdb/angelheap/exgdb
echo "peda.execute(\"set prompt \\\001%s\\\002\" % red(\"\\\002gdb-peda\$ \\\001\",\"light\")) # custom prompt" >> ~/peda/exgdb/exgdb.py
sed -i -e "s/─/=/g" $HOME/peda/lib/utils.py
sed -i -e "s@Copyright (C) 2012 Long Le Dinh <longld at vnsecurity.net>@Copyright (C) 2012 Long Le Dinh <longld at vnsecurity.net> and \n#       Copyright (C) 2017 Taisei Miyagawa <miyagaw61 at https://miyagaw61/github.io>\n#       detail: exgdb/LICENSE@g" $HOME/peda/exgdb/exgdb.py
if test ! -e $HOME/peda/exgdb/lib ;then
    mkdir $HOME/peda/exgdb/lib
fi
git clone https://github.com/miyagaw61/enert $HOME/peda/exgdb/lib/tmp
cd $HOME/peda/exgdb/lib/tmp
python setup.py install
python2 setup.py install
python3 setup.py install
cd $now
mv $HOME/peda/exgdb/lib/tmp/enert $HOME/peda/exgdb/lib/enert
rm -rf $HOME/peda/exgdb/lib/tmp
git clone https://github.com/Qix-/better-exceptions $HOME/peda/exgdb/lib/tmp
mv $HOME/peda/exgdb/lib/tmp/better_exceptions $HOME/peda/exgdb/lib/better_exceptions
rm -rf $HOME/peda/exgdb/lib/tmp
git clone https://github.com/chrippa/backports.shutil_get_terminal_size $HOME/peda/exgdb/lib/tmp
mv $HOME/peda/exgdb/lib/tmp/backports $HOME/peda/exgdb/lib/backports
rm -rf $HOME/peda/exgdb/lib/tmp
sed -i -e "s@\"/lib/\")@\"/lib/\")\nfrom enert import \*@g" $HOME/peda/exgdb/exgdb.py
echo -n "cp -a ./exgdbinit $HOME/.gdbinit [y/n] : "
read ans
case $ans in
	Y | YES | y | yes)
        if test -e $HOME/.gdbinit ;then
            cp -a $HOME/.gdbinit $HOME/.gdbinit.bak
        fi
		cp -a "$now"/exgdbinit $HOME/.gdbinit ;;
	N | NO | n | no)
		echo "You have to write exgdbinit -> $HOME/.gdbinit" ;;
	*)
		echo "You have to write exgdbinit -> $HOME/.gdbinit" ;;
esac

