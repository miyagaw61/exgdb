miyagawpeda
===========

miyagawpeda is extension plugin of gdb-peda by @miyagaw61.  
miyagawpedaは、@miyagaw61によって作成されたgdb-pedaの拡張プラグインです。

how to install
--------------

apt-get -y install gdb
git clone https://github.com/miyagaw61/miyagawpeda.git  
cd miyagawpeda  
./miyagawpeda_install.sh  

how to use
----------

* infox  
アドレスの中身を調査する  
<pre>
Usage: infox [addr]
</pre>

* fullstack  
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
一語という意味のwordでもaliasがかけられている。
<pre>
Usage: dword [addr] [count]
</pre>

* qword  
addr番地からcount個のQWORD型データ(8byte)を出力
<pre>
Usage: qword [addr] [count]
</pre>

* cc  
次のcall命令が来るまでsiで潜り続ける
<pre>
Usage: cc
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
