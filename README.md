mgpeda
===========

mgpeda is extension plugins for the gdb-peda by @miyagaw61.  
mgpedaは、@miyagaw61によって作成されたgdb-pedaの拡張プラグインです。

How to install
--------------

apt-get -y install gdb  
cd $HOME  
git clone https://github.com/miyagaw61/mgtools.git  
cd mgtools  
./mpinstall  

How to use
----------

* infox  
アドレスの中身を調査する  
<pre>
Usage: infox [addr]
</pre>

* allstack  
スタックをespからebpまで全て出力  
<pre>
Usage: fullstack
</pre>

* pc  
現在のeipが指している位置からcount個の命令コードを出力
<pre>
Usage: pc [count]
</pre>

* code  
addr番地からcount個の命令コードを出力
<pre>
Usage: code [addr] [count]
</pre>

* dword  
addr番地からcount個のDWORD型データ（4byte)を出力  
<pre>
Usage: dword [addr] [count]
</pre>

* qword  
addr番地からcount個のQWORD型データ(8byte)を出力
<pre>
Usage: qword [addr] [count]
</pre>

* jj  
次のjmp系/call命令が来るまでniで進み続ける
<pre>
Usage: jj
</pre>

* jji  
次のjmp系/call命令が来るまでsiで潜り続ける
<pre>
Usage: jji
</pre>

* cc  
次のcall命令が来るまでniで進み続ける
<pre>
Usgae: cc
</pre>

* cci  
次のcall命令が来るまでsiで潜り続ける
<pre>
Usgae: cci
</pre>

* uu  
引数に与えた文字が含まれる命令が来るまでniで進み続ける
<pre>
Usgae: uu [str]
</pre>

* uui  
引数に与えた文字が含まれる命令が来るまでsiで潜り続ける
<pre>
Usgae: uui [str]
</pre>

* uc  
引数に与えた文字が含まれるcall命令が来るまでnextcallで進み続ける
<pre>
Usgae: uc [str]
</pre>

* ii  
現在のeipが指している命令コードに用いられているアドレス/レジスタの内部を出力  
使用するには事前にregmakeコマンドでレジストリデータを保存するディレクトリを作成している必要がある
<pre>
Usgae: ii
</pre>

* regtrace  
レジストリの変化をトレースしながらeipを進める  
結果はカレントディレクトリ/regディレクトリの中に格納されていく  
使用するには事前にregmakeコマンドでレジストリデータを保存するディレクトリを作成している必要がある  
デフォルトでrtにaliasがかけられている
<pre>
Usage: regrtrace
</pre>

* parseh
現在のヒープの状況をパースしてリスト表示する。  
表示されているアドレスの配色が緑色の場合はUsedチャンク、青色の場合はFreedチャンクを表す。  
NMはnon_mainarena, IMはis_mmap, PIはprev_inuseのビット値を表す。
<pre>
Usgae: parseh
</pre>

* ci
引数に与えたアドレスを先頭アドレスとするチャンクのチャンク情報, もしくは上からｎ番目のチャンクのチャンク情報を表示する。
<pre>
Usgae: ci [addr/n]
</pre>

* cix
ciの拡張版で、Unlinkable情報,Dataも表示する。
<pre>
Usgae: ci [addr/n]
</pre>

* allci
すべてのチャンクのci結果を上から順に表示していく。
<pre>
Usgae: allci
</pre>

* allcix
すべてのチャンクのcix結果を上から順に表示していく。
<pre>
Usgae: allci
</pre>

aliases
-------

* br : break *  
* ad : advance *  
* a : advance  
* sm : searchmem  
* as : asmsearch  
* nc : nextcall  
* now : context
* here : context code
* u : stepuntil 
* nr : stepuntil ret  
* nj : stepuntil call,jmp,je,jne,jb,ja  
* nt : stepuntil test,cmp  
* ph : parseh
