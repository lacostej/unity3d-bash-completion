#!/usr/bin/python
import subprocess
import unittest

# inspired from http://stackoverflow.com/questions/9137245/unit-test-for-bash-completion-script
class Completion():
    def prepare(self, program, command):
        self.program=program
        self.COMP_LINE="%s %s" % (program, command)
        self.COMP_WORDS=self.COMP_LINE.rstrip()

        args=command.split()
        self.COMP_CWORD=len(args)
        self.COMP_POINT=len(self.COMP_LINE)

        if (self.COMP_LINE[-1] == ' '):
            self.COMP_WORDS += " "
            self.COMP_CWORD += 1

    def run(self, completion_file, program, command):
        self.prepare(program, command)
        full_cmdline=r'source {compfile}; COMP_LINE="{COMP_LINE}" COMP_WORDS=({COMP_WORDS}) COMP_CWORD={COMP_CWORD} COMP_POINT={COMP_POINT}; $(complete -p {program} | sed "s/.*-F \\([^ ]*\\) .*/\\1/") && echo ${{COMPREPLY[*]}}'.format(
                compfile=completion_file, COMP_LINE=self.COMP_LINE, COMP_WORDS=self.COMP_WORDS, COMP_POINT=self.COMP_POINT, program=self.program, COMP_CWORD=self.COMP_CWORD
                )
        out = subprocess.Popen(['bash', '-i', '-c', full_cmdline], stdout=subprocess.PIPE)
        return out.communicate()

class CompletionTestCase(unittest.TestCase):
    def test_completion_internal(self):
        self.assertEqualCompletion("fake", "",     "fake ",     "fake ",     1, 5)
        self.assertEqualCompletion("fake", " ",    "fake  ",    "fake ",     1, 6)
        self.assertEqualCompletion("fake", "a",    "fake a",    "fake a",    1, 6)
        self.assertEqualCompletion("fake", "aa",   "fake aa",   "fake aa",   1, 7)
        self.assertEqualCompletion("fake", "a ",   "fake a ",   "fake a ",   2, 7)
        self.assertEqualCompletion("fake", "a   ", "fake a   ", "fake a ",   2, 9)
        self.assertEqualCompletion("fake", "a a",  "fake a a",  "fake a a",  2, 8)
        self.assertEqualCompletion("fake", "a a ", "fake a a ", "fake a a ", 3, 9)

    def assertEqualCompletion(self, program, cline, line, words, cword, point):
        c = Completion()
        c.prepare(program, cline)
        self.assertEqual(c.program, program)
        self.assertEqual(c.COMP_LINE, line)
        self.assertEqual(c.COMP_WORDS, words)
        self.assertEqual(c.COMP_CWORD, cword)
        self.assertEqual(c.COMP_POINT, point)

class Unity3dTestCase(unittest.TestCase):
    completion_file="unity3d_bash_completion.sh"
    program="Unity"

    def test_complete_all(self):
        self.run_complete("", "-batchmode -quit -buildWindowsPlayer -buildOSXPlayer -importPackage -createProject -projectPath -logFile -assetServerUpdate -exportPackage -executeMethod")

    def test_complete_ex(self):
        self.run_complete("-batchmode -quit -ex", "-exportPackage -executeMethod")

    def test_complete_executeMethod_1(self):
        self.run_complete("-batchmode -quit -executeMethod ", "MyEditorScript MyEditorScript2")

    def test_complete_executeMethod_2(self):
        self.run_complete("-batchmode -quit -executeMethod MyEditorScript", "MyEditorScript MyEditorScript2")

    def test_complete_executeMethod_methods(self):
        self.run_complete("-batchmode -quit -executeMethod MyEditorScript.", "MyEditorScript.PerformFlashBuild MyEditorScript.PerformMacOSXBuild MyEditorScript.PerformWin32Build")

    def test_complete_executeMethod_missing_project_path(self):
        self.run_complete("-projectPath ", "")

    def test_complete_executeMethod_projectPath(self):
        self.run_complete("-quit -projectPath proj1 -executeMethod My", "MyEditorScript2")

    def test_complete_executeMethod_projectPath_with_slashes(self):
        self.run_complete("-projectPath proj1/ -executeMethod My", "MyEditorScript2")

    def run_complete(self, command, expected):
        stdout,stderr = Completion().run(self.completion_file, self.program, command)

        self.assertEqual(stdout, expected + '\n')

if (__name__=='__main__'):
    unittest.main()
