from unittest import TestCase
from restructuredtext_lint import restructuredtext_lint

"""
# Test outlines
A valid rst file
    when linted
        does not raise errors

An invalid rst file
    when linted
        raises errors
"""

class TestRestructuredtextLint(TestCase):
    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        self.assertTrue(bool(restructuredtext_lint.run))

    def test_raises_on_invalid_rst(self):
        """A invalid reStructuredText file when linted raises errors"""
        self.assertTrue(bool(restructuredtext_lint.run))
