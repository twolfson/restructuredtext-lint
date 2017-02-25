# Load in our dependencies
from __future__ import absolute_import
import os
import subprocess
import sys
from unittest import TestCase

import yaml

import restructuredtext_lint


__dir__ = os.path.dirname(os.path.abspath(__file__))
valid_rst = os.path.join(__dir__, 'test_files', 'valid.rst')
warning_rst = os.path.join(__dir__, 'test_files', 'second_short_heading.rst')
invalid_rst = os.path.join(__dir__, 'test_files', 'invalid.rst')
rst_lint_path = os.path.join(__dir__, os.pardir, 'cli.py')

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
        return restructuredtext_lint.lint(*args, **kwargs)

    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        content = self._load_file(valid_rst)
        errors = self._lint_file(content)
        self.assertEqual(errors, [])

    def test_raises_on_invalid_rst(self):
        """A invalid reStructuredText file when linted raises errors"""
        # Load and lint invalid file
        content = self._load_file(invalid_rst)
        actual_errors = self._lint_file(content, invalid_rst)

        # Load in expected errors
        expected_yaml = self._load_file(os.path.join(__dir__, 'test_files', 'invalid.yaml'))
        expected_errors = yaml.load(expected_yaml)

        # Assert errors against expected errors
        self.assertEqual(len(actual_errors), len(expected_errors))
        for i, error in enumerate(expected_errors):
            self.assertEqual(actual_errors[i].line, expected_errors[i]['line'])
            self.assertEqual(actual_errors[i].level, expected_errors[i]['level'])
            self.assertEqual(actual_errors[i].type, expected_errors[i]['type'])
            self.assertEqual(actual_errors[i].source, invalid_rst)
            self.assertEqual(actual_errors[i].message, expected_errors[i]['message'])

    def test_encoding_utf8(self):
        """A document with utf-8 characters is valid."""
        filepath = os.path.join(__dir__, 'test_files', 'utf8.rst')
        errors = restructuredtext_lint.lint_file(filepath, encoding='utf-8')
        self.assertEqual(errors, [])

    def test_second_heading_short_line_number(self):
        """A document with a short second heading raises errors that include a line number

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/5
        """
        filepath = os.path.join(__dir__, 'test_files', 'second_short_heading.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertEqual(errors[0].line, 6)
        self.assertEqual(errors[0].source, filepath)

    def test_invalid_target(self):
        """A document with an invalid target name raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/6
        """
        filepath = os.path.join(__dir__, 'test_files', 'invalid_target.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Unknown target name', errors[0].message)

    def test_invalid_line_mismatch(self):
        """A document with an overline/underline mismatch raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/7
        """
        filepath = os.path.join(__dir__, 'test_files', 'invalid_line_mismatch.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Title overline & underline mismatch', errors[0].message)

    def test_invalid_link(self):
        """A document with a bad link raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/12
        """
        filepath = os.path.join(__dir__, 'test_files', 'invalid_link.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Anonymous hyperlink mismatch: 1 references but 0 targets.', errors[0].message)
        self.assertIn('Hyperlink target "hello" is not referenced.', errors[1].message)


class TestRestructuredtextLintCLI(TestCase):
    """ Tests for 'rst-lint' CLI comand """

    def test_rst_lint_filepaths_not_given(self):
        """The `rst-lint` command is available and prints error if no filepath was given."""
        with self.assertRaises(subprocess.CalledProcessError) as e:
            # python ../cli.py
            subprocess.check_output((sys.executable, rst_lint_path), stderr=subprocess.STDOUT)
        output = str(e.exception.output)
        self.assertIn('too few arguments', output)

    def test_rst_lint_correct_file(self):
        """The `rst-lint` command prints nothing if rst file is correct."""
        # python ../cli.py test_files/valid.rst
        raw_output = subprocess.check_output((sys.executable, rst_lint_path, valid_rst))
        output = str(raw_output)
        self.assertEqual(output, '')

    def test_rst_lint_many_files(self):
        """The `rst-lint` command accepts many rst file paths and prints respective information for each of them."""
        with self.assertRaises(subprocess.CalledProcessError) as e:
            # python ../cli.py test_files/valid.rst invalid.rst
            subprocess.check_output((sys.executable, rst_lint_path, valid_rst, invalid_rst))
        output = str(e.exception.output)
        # 'rst-lint' should exit with error code 2 as linting failed:
        self.assertEqual(e.exception.returncode, 2)
        # There should be no clean output:
        # DEV: This verifies only 1 line of output which is our invalid line
        self.assertEqual(output.count('\n'), 1, output)
        # There should be a least one invalid rst file:
        self.assertIn('WARNING', output)

    def test_level_fail(self):
        """Confirm low --level threshold fails file with warnings only"""
        # This is the expected behaviour we are checking:
        # $ rst-lint --level warning second_short_heading.rst ; echo "Return code $?"
        # WARNING second_short_heading.rst:6 Title underline too short.
        # WARNING second_short_heading.rst:6 Title underline too short.
        # Return code 2
        with self.assertRaises(subprocess.CalledProcessError) as e:
            subprocess.check_output((sys.executable, rst_lint_path, '--level', 'warning', warning_rst),
                                    universal_newlines=True)
        output = str(e.exception.output)
        self.assertEqual(output.count('\n'), 2, output)
        self.assertEqual(output.count('WARNING'), 2, output)
        # The expected 2 warnings should be treated as failing
        self.assertEqual(e.exception.returncode, 2)

    def test_level_high(self):
        """Confirm high --level threshold accepts file with warnings only"""
        # This is the expected behaviour we are checking:
        # $ rst-lint --level error second_short_heading.rst ; echo "Return code $?"
        # Return code 0
        raw_output = subprocess.check_output((sys.executable, rst_lint_path, '--level', 'error', warning_rst),
                                             universal_newlines=True)
        # `check_output` doesn't raise an exception code so it's error code 0
        output = str(raw_output)
        self.assertEqual(output, '')
