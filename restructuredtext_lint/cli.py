# Load in our dependencies
from __future__ import absolute_import
import argparse
import json
import os
import sys

from restructuredtext_lint.lint import lint_file

# Load in VERSION from standalone file
with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as version_file:
    VERSION = version_file.read().strip()


def _main(filepaths, format='text', stream=sys.stdout, encoding=None, level=0, fail=0):
    error_dicts = []
    error_occurred = False

    for filepath in filepaths:
        # Read and lint the file
        file_errors = lint_file(filepath, encoding=encoding)

        if not file_errors:
            if format == 'text':
                stream.write('INFO File {filepath} is clean.\n'.format(filepath=filepath))
        else:
            for error in file_errors:
                if error.level >= fail:
                    error_occurred = True
            if format == 'text':
                for error in file_errors:
                    if error.level >= level:
                        # e.g. WARNING readme.rst:12 Title underline too short.
                        stream.write('{err.type} {err.source}:{err.line} {err.message}\n'.format(err=error))
            elif format == 'json':
                error_dicts.extend({
                    'line': error.line,
                    'source': error.source,
                    'level': error.level,
                    'type': error.type,
                    'message': error.message,
                    'full_message': error.full_message,
                } for error in file_errors if error.level >= level)

    if format == 'json':
        stream.write(json.dumps(error_dicts))

    if error_occurred:
        sys.exit(2)  # Using 2 for linting failure, 1 for internal error
    else:
        sys.exit(0)  # Success!


def main():
    # Set up options and parse arguments
    parser = argparse.ArgumentParser(description='Lint reStructuredText files. Returns 0 if all files pass linting, '
                                     '1 for an internal error, and 2 if linting failed.')
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('filepaths', metavar='filepath', nargs='+', type=str, help='File to lint')
    parser.add_argument('--format', default='text', type=str, help='Format of the output (e.g. text, json)')
    parser.add_argument('--encoding', type=str, help='Encoding of the input file (e.g. utf-8)')
    parser.add_argument('--level', default=1, type=int, choices=(1, 2, 3, 4),
                        help='Minimum docutils linting error level to report '
                        '(integer, 1=info [default], 2=warning, 3=error, 4=severe)')
    parser.add_argument('--fail', default=2, type=int, choices=(1, 2, 3, 4),
                        help='Minimum docutils linting error level to consider as failing '
                        '(integer, 1=info, 2=warning [default], 3=error, 4=severe)')
    args = parser.parse_args()

    # Run the main argument
    _main(**args.__dict__)


if __name__ == '__main__':
    main()
