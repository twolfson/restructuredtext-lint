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

# TODO: Implement this as a class (options) with a sugar function that lints a string against a set of options
An invalid rst file
    when linted with the `fail_first` parameter
        raises on the first error
"""

class TestRestructuredtextLint(TestCase):
    def _load_file(self, filepath):
        """Load a file into memory"""
        f = open(filepath)
        file = f.read()
        f.close()
        return file

    def _lint_file(self, *args, **kwargs):
        """Lint the file and preserve any errors"""
        return restructuredtext_lint.run(*args)

    # TODO: Move to flat file tests
    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        filepath = __dir__ + '/test_files/valid.rst'
        content = self._load_file(filepath)
        errors = self._lint_file(content)
        self.assertEqual(errors, [])

    def test_raises_on_invalid_rst(self):
        """A invalid reStructuredText file when linted raises errors"""
        filepath = __dir__ + '/test_files/invalid.rst'
        content = self._load_file(filepath)
        errors = self._lint_file(content, filepath)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].line, 2)
        self.assertEqual(errors[0].source, filepath)
        self.assertEqual(errors[0].message, 'Title underline too short.')
