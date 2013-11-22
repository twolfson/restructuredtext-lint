from unittest import TestCase
from restructuredtext_lint import restructuredtext_lint

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
        pass

    def _lint_file(self):
        """Lint the file and preserve any errors"""
        pass

    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        self.assertTrue(bool(restructuredtext_lint.run))

    def test_raises_on_invalid_rst(self):
        """A invalid reStructuredText file when linted raises errors"""
        self.assertTrue(bool(restructuredtext_lint.run))
