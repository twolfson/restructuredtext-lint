import os
from unittest import TestCase

import yaml

import restructuredtext_lint
from restructuredtext_lint.sphinx import get_empty_directives_roles

__dir__ = os.path.dirname(os.path.abspath(__file__))

"""
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

    def test_encoding_utf8(self):
        """A document with utf-8 characters is valid."""
        filepath = __dir__ + '/test_files/utf8.rst'
        errors = restructuredtext_lint.lint_file(filepath, encoding='utf-8')
        self.assertEqual(errors, [])

    def test_second_heading_short_line_number(self):
        """A document with a short second heading raises errors that include a line number

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/5
        """
        filepath = __dir__ + '/test_files/second_short_heading.rst'
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertEqual(errors[0].line, 6)
        self.assertEqual(errors[0].source, filepath)

    def test_invalid_target(self):
        """A document with an invalid target name raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/6
        """
        filepath = __dir__ + '/test_files/invalid_target.rst'
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Unknown target name', errors[0].message)

    def test_invalid_line_mismatch(self):
        """A document with an overline/underline mismatch raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/7
        """
        filepath = __dir__ + '/test_files/invalid_line_mismatch.rst'
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Title overline & underline mismatch', errors[0].message)

    def test_invalid_link(self):
        """A document with a bad link raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/12
        """
        filepath = __dir__ + '/test_files/invalid_link.rst'
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Anonymous hyperlink mismatch: 1 references but 0 targets.', errors[0].message)
        self.assertIn('Hyperlink target "hello" is not referenced.', errors[1].message)

    def test_sphinx(self):
        """A document with Sphinx directives/roles ignores them when requested to

        https://github.com/twolfson/restructuredtext-lint/issues/11
        """
        filepath = __dir__ + '/test_files/sphinx.rst'
        get_empty_directives_roles()
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertEqual(errors, [])
