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

Function list
-------------

* infox  
* allstack  
* pc  
* code  
* dword  
* qword  
* jj  
* jji  
* cc  
* cci  
* uu  
* uui  
* uc  
* ii  
* parseh  
* ci  
* cix  
* allci  
* allcix  

How to use
----------

* infox  
アドレスの中身を調査する  
![infox](http://i.imgur.com/6uTRYLj.png)
<pre>
Usage: infox [addr]
</pre>

* allstack  
スタックをespからebpまで全て出力  
![allstack](http://i.imgur.com/rMhRO9c.png)
<pre>
Usage: fullstack
</pre>

* pc  
現在のeipが指している位置からcount個の命令コードを出力
![pc](http://i.imgur.com/12HCezL.png)
<pre>
Usage: pc [count]
</pre>

* code  
addr番地からcount個の命令コードを出力
![code](http://i.imgur.com/h4GPE1O.png)
<pre>
Usage: code [addr] [count]
</pre>

* dword  
addr番地からcount個のDWORD型データ（4byte)を出力  
![dword](http://i.imgur.com/KRAniQl.png)
<pre>
Usage: dword [addr] [count]
</pre>

* qword  
addr番地からcount個のQWORD型データ(8byte)を出力
![qword](http://i.imgur.com/7m4bb6s.png)
<pre>
Usage: qword [addr] [count]
</pre>

* jj  
次のjmp系/call命令が来るまでniで進み続ける
![jj1](http://i.imgur.com/k51hUKf.png)
![jj2](http://i.imgur.com/wKimY6o.png)
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
![ii](http://i.imgur.com/PJuQdM1.png)
<pre>
Usgae: ii
</pre>

* parseh  
現在のヒープの状況をパースしてリスト表示する。  
表示されているアドレスの配色が緑色の場合はUsedチャンク、青色の場合はFreedチャンクを表す。  
NMはnon_mainarena, IMはis_mmap, PIはprev_inuseのビット値を表す。
![parseh](http://i.imgur.com/ryqUG6x.png)
<pre>
Usgae: parseh
</pre>

* ci  
引数に与えたアドレスを先頭アドレスとするチャンクのチャンク情報, もしくは上からｎ番目のチャンクのチャンク情報を表示する。
![ci](http://i.imgur.com/Wfj7WAq.png)
<pre>
Usgae: ci [addr/n]
</pre>

* cix  
ciの拡張版で、Unlinkable情報,Dataも表示する。
![cix](http://i.imgur.com/pO4443S.png)
<pre>
Usgae: ci [addr/n]
</pre>

* allci  
すべてのチャンクのci結果を上から順に表示していく。
![allci](http://i.imgur.com/XVVRbGA.png)
<pre>
Usgae: allci
</pre>

* allcix  
すべてのチャンクのcix結果を上から順に表示していく。
![allcix](http://i.imgur.com/V0qAzrO.png)
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

