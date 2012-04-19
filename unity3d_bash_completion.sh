# Bash completion script for Unity3d
#
# To use, add the following to your .bashrc:
#
#    . $(UNITY_HOME)/Library/Contributions/unity3d_bash_completion.sh
#
# Alternatively, if you have installed the bash-completion package with brew,
# you can create a symlink to this file in one of the following directories:
#
#    $(brew --prefix)/etc/bash_completion.d
#    $(brew --prefix)/share/bash-completion/completions
#
# and bash-completion will source it automatically.
#

__unity3d_complete_executeMethod ()
{
	local cur="${COMP_WORDS[COMP_CWORD]}"
	local editors=$(\ls  Assets/Editor/*.cs | xargs -L1 basename | sed 's/\.cs//g' | xargs echo)
	local options=$editors
	local file

	if [ -z $cur ]; then
		if [ ${#cs[@]} -eq 1 ]; then
			file=${cs[0]}
		fi
	else
		class=`echo $cur | cut -d '.' -f 1`
		method=`echo $cur | cut -d '.' -f 2`
		if [[ "$cur" != "$class" ]]; then
			file=$class
			options=`sed  -n 's/.*static void * \(.*\) *().*/\1/p' Assets/Editor/${class}.cs | grep "^$method" | sed "s/^/$class./g" | sort | xargs echo`
		fi

	fi
	COMPREPLY=($(compgen -W "$options" -- "$cur"))
}

_unity3d ()
{
	local cmd

	cmd="${COMP_WORDS[$COMP_CWORD]}"
	if [ -z "$cmd" ]; then
		cmd="${COMP_WORDS[$COMP_CWORD-1]}"
	fi
	case "$cmd" in
		-*)
		;;
		*)
		cmd="${COMP_WORDS[$COMP_CWORD-1]}"
 		;;
	esac
	# subcommands have their own completion functions
	case "$cmd" in
	-buildWindowsPlayer|-buildOSXPlayer|-importPackage|-projectPath|-logFile)
		#path completion is handled automatically by the shell
		;;
	-executeMethod)	
		__unity3d_complete_executeMethod ;;
	*)	
		__unity3dcomp "
			-batchmode -quit -buildWindowsPlayer -buildOSXPlayer -importPackage -createProject -projectPath
			-logFile -assetServerUpdate -exportPackage -executeMethod -batchmode
			"
		;;
	esac
}

complete -o bashdefault -o default -F _unity3d Unity
