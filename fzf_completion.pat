--- /home/miyagaw61/.fzf.bak/shell/completion.bash	2017-08-04 14:02:29.648215000 +0900
+++ /home/miyagaw61/.fzf/shell/completion.bash	2017-08-06 18:04:47.590505567 +0900
@@ -135,7 +135,12 @@ __fzf_generic_path_completion() {
   fzf="$(__fzfcmd_complete)"
   cmd="${COMP_WORDS[0]//[^A-Za-z0-9_=]/_}"
   COMPREPLY=()
-  trigger=${FZF_COMPLETION_TRIGGER-'**'}
+  #trigger=${FZF_COMPLETION_TRIGGER-'**'}
+  #trigger=${FZF_COMPLETION_TRIGGER-'hoge'}
+  #trigger=${FZF_COMPLETION_TRIGGER-'*'}
+  #trigger=${FZF_COMPLETION_TRIGGER-''}
+  #trigger=${FZF_COMPLETION_TRIGGER-'.'}
+  trigger=${FZF_COMPLETION_TRIGGER-','}
   cur="${COMP_WORDS[COMP_CWORD]}"
   if [[ "$cur" == *"$trigger" ]]; then
     base=${cur:0:${#cur}-${#trigger}}
@@ -151,7 +156,7 @@ __fzf_generic_path_completion() {
         matches=$(eval "$1 $(printf %q "$dir")" | FZF_DEFAULT_OPTS="--height ${FZF_TMUX_HEIGHT:-40%} --reverse $FZF_DEFAULT_OPTS $FZF_COMPLETION_OPTS" $fzf $2 -q "$leftover" | while read -r item; do
           printf "%q$3 " "$item"
         done)
-        matches=${matches% }
+        [ $4 = 1 ] && matches=${matches% }
         if [ -n "$matches" ]; then
           COMPREPLY=( "$matches" )
         else
@@ -167,6 +172,7 @@ __fzf_generic_path_completion() {
     shift
     shift
     shift
+    shift
     _fzf_handle_dynamic_completion "$cmd" "$@"
   fi
 }
@@ -179,6 +185,7 @@ _fzf_complete() {
 
   cmd="${COMP_WORDS[0]//[^A-Za-z0-9_=]/_}"
   trigger=${FZF_COMPLETION_TRIGGER-'**'}
+  trigger=${FZF_COMPLETION_TRIGGER-''}
   cur="${COMP_WORDS[COMP_CWORD]}"
   if [[ "$cur" == *"$trigger" ]]; then
     cur=${cur:0:${#cur}-${#trigger}}
@@ -198,7 +205,7 @@ _fzf_complete() {
 }
 
 _fzf_path_completion() {
-  __fzf_generic_path_completion _fzf_compgen_path "-m" "" "$@"
+  __fzf_generic_path_completion _fzf_compgen_path "-m" "" 0 "$@"
 }
 
 # Deprecated. No file only completion.
@@ -207,7 +214,7 @@ _fzf_file_completion() {
 }
 
 _fzf_dir_completion() {
-  __fzf_generic_path_completion _fzf_compgen_dir "" "/" "$@"
+  __fzf_generic_path_completion _fzf_compgen_dir "" "/" 1 "$@"
 }
 
 _fzf_complete_kill() {
@@ -299,7 +306,7 @@ _fzf_defc() {
 
 # Anything
 for cmd in $a_cmds; do
-  _fzf_defc "$cmd" _fzf_path_completion "-o default -o bashdefault"
+  _fzf_defc "$cmd" _fzf_path_completion "-o nospace -o default -o bashdefault"
 done
 
 # Directory
