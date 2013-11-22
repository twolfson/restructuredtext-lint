import os
from unittest import TestCase

from restructuredtext_lint import restructuredtext_lint

__dir__ = os.path.dirname(os.path.abspath(__file__))

"""
# Test outlines
A valid rst file
    when linted
        does not return errors

An invalid rst file
    when linted
        returns errors

# TODO: We should build out a bin script to lint files
# TODO: This should evolve into part of sublime-linter
# TODO: Implement this or record it as an open issue
An invalid rst file
    when linted with the `fail_first` parameter
        raises on the first error
"""

class TestRestructuredtextLint(TestCase):
    def _load_file(self, filepath):
        """Load a file into memory"""
        f = open(filepath)
        self.file = f.read()
        f.close()

    def _lint_file(self):
        """Lint the file and preserve any errors"""
        pass

    # TODO: Consider implementing these as flat file tests once we know what the output looks like
    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        self._load_file(__dir__ + '/test_files/valid.rst')
        print self.file
        self.assertTrue(bool(restructuredtext_lint.run))

    def test_raises_on_invalid_rst(self):
        """A invalid reStructuredText file when linted raises errors"""
        self._load_file(__dir__ + '/test_files/invalid.rst')
        print self.file
        self.assertTrue(bool(restructuredtext_lint.run))
