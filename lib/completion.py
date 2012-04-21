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

class BashCompletionTest(unittest.TestCase):
    def run_complete(self, completion_file, program, command, expected):
        stdout,stderr = Completion().run(completion_file, program, command)
        self.assertEqual(stdout, expected + '\n')

class AdsfTestCase(BashCompletionTest):
    def test_orig(self):
        self.run_complete("other arguments f", "four five")

    def run_complete(self, command, expected):
        completion_file="adsf-completion"
        program="asdf"
        super(AdsfTestCase, self).run_complete(completion_file, program, command, expected)


if (__name__=='__main__'):
    unittest.main()
