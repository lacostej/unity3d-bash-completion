#!/usr/bin/python
import unittest
from lib.completion import BashCompletionTest

class Unity3dTestCase(BashCompletionTest):

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
        completion_file="unity3d_bash_completion.sh"
        program="Unity"
        super(Unity3dTestCase, self).run_complete(completion_file, program, command, expected)

if (__name__=='__main__'):
    unittest.main()
