
_fake ()
{
        echo "-> |${COMP_CWORD}| |${COMP_POINT}| |${COMP_LINE}| |${COMP_WORDS[*]}|"
        COMPREPLY=${COMP_WORDS[*]}
}

complete -o bashdefault -o default -F _fake fake
