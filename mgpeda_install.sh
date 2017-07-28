#!/bin/sh

if test ! -e ./mgpeda_install.sh ;then
    echo "Please < cd /hoge/mgpeda ; ./mgpeda_install.sh >"
    exit 0
fi
if test ! -e $HOME/peda/ ;then
	git clone https://github.com/longld/peda.git $HOME/peda  
fi
if test ! -e $HOME/Pwngdb/ ;then
	git clone https://github.com/scwuaptx/Pwngdb.git $HOME/Pwngdb
fi
line=$(cat $HOME/peda/peda.py | grep -n "def xprint" | sed -E "s/(.*):.*:/\1/g")
if test ! -e $HOME/peda/mgpeda/ ;then
	mkdir $HOME/peda/mgpeda/
fi
#cp -a "$(pwd)"/mgpeda64.txt $HOME/peda/mgpeda/
cp -a "$(pwd)"/mgpeda_code.py $HOME/peda/mgpeda/
#cp -a "$(pwd)"/mgpeda32.txt $HOME/peda/mgpeda/
cp -a "$(pwd)"/mgpeda.alias.txt $HOME/peda/mgpeda/
head -n $((${line} - 1)) $HOME/peda/peda.py | tail -n $((${line} - 1)) > $HOME/peda/mgpeda/peda.before.txt
head -n $(cat $HOME/peda/peda.py | wc -l) $HOME/peda/peda.py | tail -n $(($(cat $HOME/peda/peda.py | wc -l) - ${line} + 1)) > $HOME/peda/mgpeda/peda.after.txt
cp -a $HOME/peda/mgpeda/peda.before.txt $HOME/peda/mgpeda/mgpeda.py
#if test "$(uname -a | grep 'x86_64')" ;then
	#cat $HOME/peda/mgpeda/mgpeda64.txt >> $HOME/peda/mgpeda/mgpeda.py
cat $HOME/peda/mgpeda/mgpeda_code.py >> $HOME/peda/mgpeda/mgpeda.py
#else
#	cat $HOME/peda/mgpeda/mgpeda32.txt >> $HOME/peda/mgpeda/mgpeda.py
#fi
cat $HOME/peda/mgpeda/peda.after.txt >> $HOME/peda/mgpeda/mgpeda.py
cat $HOME/peda/mgpeda/mgpeda.alias.txt >> $HOME/peda/mgpeda/mgpeda.py

cat $HOME/peda/mgpeda/mgpeda.py | perl -pe "s@if not self._is_running\(\)@if\(1==2\)@g" > $HOME/peda/mgpeda/mgpeda.tmp
cat $HOME/peda/mgpeda/mgpeda.tmp | perl -pe "s@if not pid@if\(1==2\)@g" > $HOME/peda/mgpeda/mgpeda.py
cat $HOME/peda/mgpeda/mgpeda.py | perl -pe "s@if self._is_running\(\):@if\(1==1\):@g" > $HOME/peda/mgpeda/mgpeda.tmp
 
### getpid=$(cat getpid.txt)
### cat $HOME/peda/mgpeda/mgpeda.tmp | perl -pe "s@if not pid@"$getpid"@g" > $HOME/peda/mgpeda/mgpeda.tmp2
### cat $HOME/peda/mgpeda/mgpeda.tmp2 | perl -pe "s@TMPSPACE@ @g" > $HOME/peda/mgpeda/mgpeda.tmp
### cat $HOME/peda/mgpeda/mgpeda.tmp | perl -pe "s@TMP2SPACE@        @g" > $HOME/peda/mgpeda/mgpeda.tmp2
### cat $HOME/peda/mgpeda/mgpeda.tmp2 | perl -pe "s@TMP3SPACE@            @g" > $HOME/peda/mgpeda/mgpeda.py
mv $HOME/peda/mgpeda/mgpeda.tmp $HOME/peda/mgpeda/mgpeda.py

if test ! -e $HOME/Pwngdb/angelheap/mgpeda/ ;then
	mkdir $HOME/Pwngdb/angelheap/mgpeda/
fi
cat $HOME/Pwngdb/angelheap/angelheap.py | head -4 > $HOME/Pwngdb/angelheap/mgpeda/angelheap.py
cat "$(pwd)"/seraphheap_before.py >> $HOME/Pwngdb/angelheap/mgpeda/angelheap.py
cat $HOME/Pwngdb/angelheap/angelheap.py | grep -A$(cat $HOME/Pwngdb/angelheap/angelheap.py | wc -l) "import gdb" >> $HOME/Pwngdb/angelheap/mgpeda/angelheap.py
cat "$(pwd)"/seraphheap_after.py >> $HOME/Pwngdb/angelheap/mgpeda/angelheap.py
line=$(cat $HOME/Pwngdb/angelheap/command_wrapper.py | grep -n "class AngelHeapCmdWrapper" | sed -E "s/(.*):.*:/\1/g")
echo "import sys" > $HOME/Pwngdb/angelheap/mgpeda/command_wrapper.py
echo 'sys.path.append("/home/miyagaw61/Pwngdb")' >> $HOME/Pwngdb/angelheap/mgpeda/command_wrapper.py
echo "import pwngdb" >> $HOME/Pwngdb/angelheap/mgpeda/command_wrapper.py

head -n $((${line} - 1)) $HOME/Pwngdb/angelheap/command_wrapper.py | tail -n $((${line} - 1)) >> $HOME/Pwngdb/angelheap/mgpeda/command_wrapper.py
head -n $(cat $HOME/Pwngdb/angelheap/command_wrapper.py | wc -l) $HOME/Pwngdb/angelheap/command_wrapper.py | tail -n $(($(cat $HOME/Pwngdb/angelheap/command_wrapper.py | wc -l) - ${line} + 1)) >> $HOME/Pwngdb/angelheap/mgpeda/command_wrapper_after.py
cat "$(pwd)"/command_wrapper.py >> $HOME/Pwngdb/angelheap/mgpeda/command_wrapper.py
cat $HOME/Pwngdb/angelheap/mgpeda/command_wrapper_after.py >> $HOME/Pwngdb/angelheap/mgpeda/command_wrapper.py
rm $HOME/Pwngdb/angelheap/mgpeda/command_wrapper_after.py
cp -a $HOME/Pwngdb/angelheap/gdbinit.py $HOME/Pwngdb/angelheap/mgpeda/
cp  -a $HOME/Pwngdb/pwngdb.py $HOME/Pwngdb/angelheap/mgpeda
echo -n "cp -a mggdbinit $HOME/.gdbinit [y/n] : "
read ans
case $ans in
	Y | YES | y | yes)
		cp -a $HOME/.gdbinit $HOME/.gdbinit.bak
		cp -a "$(pwd)"/mggdbinit $HOME/.gdbinit ;;
	N | NO | n | no)
		echo "You have to write mggdbinit -> $HOME/.gdbinit" ;;
	*)
		echo "You have to write mggdbinit -> $HOME/.gdbinit" ;;
esac

