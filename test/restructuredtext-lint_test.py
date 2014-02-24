import os
from unittest import TestCase

import yaml

import restructuredtext_lint

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
        return restructuredtext_lint.lint(*args)

    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        filepath = __dir__ + '/test_files/valid.rst'
        content = self._load_file(filepath)
        errors = self._lint_file(content)
        self.assertEqual(errors, [])

    def test_raises_on_invalid_rst(self):
        """A invalid reStructuredText file when linted raises errors"""
        # Load and lint invalid file
        filepath = __dir__ + '/test_files/invalid.rst'
        content = self._load_file(filepath)
        actual_errors = self._lint_file(content, filepath)

        # Load in expected errors
        expected_yaml = self._load_file(__dir__ + '/test_files/invalid.yaml')
        expected_errors = yaml.load(expected_yaml)

        # Assert errors against expected errors
        self.assertEqual(len(actual_errors), len(expected_errors))
        for i, error in enumerate(expected_errors):
            self.assertEqual(actual_errors[i].line, expected_errors[i]['line'])
            self.assertEqual(actual_errors[i].level, expected_errors[i]['level'])
            self.assertEqual(actual_errors[i].type, expected_errors[i]['type'])
            self.assertEqual(actual_errors[i].source, filepath)
            self.assertEqual(actual_errors[i].message, expected_errors[i]['message'])


    def test_encoding(self):
        """A document with special characters can be used."""
        filepath = __dir__ + '/test_files/utf8.rst'
        self.assertRaises(UnicodeDecodeError,
                          restructuredtext_lint.lint_file,
                          filepath, encoding=None)
        errors = restructuredtext_lint.lint_file(filepath, encoding='utf-8')
        self.assertEqual(errors, [])
