mgpeda
===========

extension plugins for the gdb-peda&Pwngdb.  
gdb-peda,Pwngdbの拡張プラグインです。
**元々のpedaのソースコードは改造していないため、環境を壊すことはありません。**  
**mgpedaを使いたくなくなったら~/.gdbinitからsource ~/peda/mgpeda/mgpeda.pyとsource ~/Pwngdb/angelheap/mgpeda/gdbinit.pyを削除するだけで大丈夫です。**  

How to install
--------------

apt-get -y install gdb  
cd $HOME/Downloads  
git clone https://github.com/miyagaw61/mgpeda.git  
cd mgpeda  
./mgpeda_install.sh  

※最後の"cp -a mggdbinit $HOME/.gdbinit [y/n]"という質問にyと答えると、現在の.gdbinitが上書きされてしまいます。nと答えた場合は自分で追記してください。（一応$HOME/.gdbinit.bakという名前でバックアップはとるようになっています）
※うまくいかない場合は~/.gdbinitの最後のendを削除してendを一つにするとうまくいく場合もあるようです。

Function list
-------------

* ix  
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

* ix  
アドレスの中身を調査する  
(telescopeコマンドの改良版。  
一つのアドレスのみを調べたい場合に、"telescope [address] 1"の"1"の入力を省略可能。)  
![ix](http://i.imgur.com/QdUut21.png)
```
Usage: ix [addr] [count]
```

* allstack  
スタックをespからebpまで全て出力  
![allstack](http://i.imgur.com/rMhRO9c.png)
```
Usage: allstack
```

* pc  
現在のeipが指している位置からcount個の命令コードを出力
![pc](http://i.imgur.com/12HCezL.png)
```
Usage: pc [count]
```

* code  
addr番地からcount個の命令コードを出力
![code](http://i.imgur.com/h4GPE1O.png)
```
Usage: code [addr] [count]
```

* dtel
double型版telescope
```
Usage: dtel [addr] [count]
```

* xgrep  
cmdコマンドの出力をregexp正規表現でgrepして抽出する。  
grepというaliasがかけられている。  
※このコマンドを使用するためには別途 https://github.com/miyagaw61/mgtools を導入する必要あり  
![xgrep](http://i.imgur.com/jy2xbEq.png)
```
Usage: xgrep [cmd] [regexp]
```

* jj  
次のjmp系/call命令が来るまでniで進み続ける
![jj1](http://i.imgur.com/k51hUKf.png)
![jj2](http://i.imgur.com/wKimY6o.png)
```
Usage: jj
```

* jji  
次のjmp系/call命令が来るまでsiで潜り続ける
```
Usage: jji
```

* cc  
次のcall命令が来るまでniで進み続ける
```
Usage: cc
```

* cci  
次のcall命令が来るまでsiで潜り続ける
```
Usage: cci
```

* uu  
引数に与えた文字が含まれる命令が来るまでniで進み続ける
```
Usage: uu [str]
```

* uui  
引数に与えた文字が含まれる命令が来るまでsiで潜り続ける
```
Usage: uui [str]
```
* uc  引数に与えた文字が含まれるcall命令が来るまでnextcallで進み続ける
```
Usage: uc [str]
```

* ii  
現在のeipが指している命令コードに用いられているアドレス/レジスタの内部を出力  
![ii](http://i.imgur.com/IePbIFI.png)
```
Usage: ii
```

* ph  
現在のヒープの状況をパースしてリスト表示する。  
表示されているアドレスの配色が緑色の場合はUsedチャンク、青色の場合はFreedチャンクを表す。  
NMはnon_mainarena, IMはis_mmap, PIはprev_inuseのビット値を表す。
![ph](http://i.imgur.com/pP9N1MF.png)
```
Usage: ph
```

* ci  
引数に与えたアドレスを先頭アドレスとするチャンクのチャンク情報, もしくは上からｎ番目のチャンクのチャンク情報を表示する。
![ci](http://i.imgur.com/Wfj7WAq.png)
```
Usage: ci [addr/n]
```

* cix  
ciの拡張版で、Dataも表示する。
![cix](http://i.imgur.com/pO4443S.png)
```
Usage: ci [addr/n]
```

* allci  
すべてのチャンクのci結果を上から順に表示していく。
![allci](http://i.imgur.com/XVVRbGA.png)
```
Usage: allci
```

* allcix  
すべてのチャンクのcix結果を上から順に表示していく。  
ただし、先頭のChunk infoテキストとUnlinkable情報を省くことによって、  
ヒープ領域を一語ずつ全て、ヒープ情報付きで表示することができる。  
![allcix](http://i.imgur.com/V0qAzrO.png)
```
Usage: allcix
```

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
* grep : xgrep


