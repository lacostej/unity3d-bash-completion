#!/usr/bin/python
import subprocess
import unittest

# inspired from http://stackoverflow.com/questions/9137245/unit-test-for-bash-completion-script
class CompletionTestCase(unittest.TestCase):
    completion_file="unity3d_bash_completion.sh"
    program="Unity"

    def test_complete_all(self):
        self.run_complete("", "-batchmode -quit -buildWindowsPlayer -buildOSXPlayer -importPackage -createProject -projectPath -logFile -assetServerUpdate -exportPackage -executeMethod")

    def test_complete(self):
        self.run_complete("-batchmode -quit -ex", "-exportPackage -executeMethod")

    def run_complete(self, command, expected):
        args=command.split()
        args.insert(0, self.program)

        partial_word=""
        if len(command) == 0:
            args.append(partial_word)
        elif command[-1] != ' ':
            partial_word=args[len(args) - 1] 
        cmd=args
        cmdline=r'{program} {command}'.format(program=self.program, command=command)

        full_cmdline=r'source {compfile}; COMP_LINE="{cmdline}" COMP_WORDS=({cmdline}) COMP_CWORD={cword} COMP_POINT={cmdlen}; $(complete -p {cmd} | sed "s/.*-F \\([^ ]*\\) .*/\\1/") && echo ${{COMPREPLY[*]}}'.format(
                compfile=self.completion_file, cmdline=cmdline, cmdlen=len(cmdline), cmd=cmd[0], cword=cmd.index(partial_word)
                )
        #print full_cmdline
        out = subprocess.Popen(['bash', '-i', '-c', full_cmdline], stdout=subprocess.PIPE)
        stdout, stderr = out.communicate()
        self.assertEqual(stdout, expected + '\n')

if (__name__=='__main__'):
    unittest.main()
