# Load in our dependencies
from __future__ import absolute_import
import argparse
import json
import os
import sys

from collections import OrderedDict

from docutils.utils import Reporter

from restructuredtext_lint.lint import lint_file

# Generate our levels mapping for humans, using ordered dict for --help string
# http://repo.or.cz/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/utils/__init__.py#l65
LEVEL_MAP = OrderedDict([
    ('debug', Reporter.DEBUG_LEVEL),  # 0
    ('info', Reporter.INFO_LEVEL),  # 1
    ('warning', Reporter.WARNING_LEVEL),  # 2
    ('error', Reporter.ERROR_LEVEL),  # 3
    ('severe', Reporter.SEVERE_LEVEL),  # 4
])


# Load in VERSION from standalone file
with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as version_file:
    VERSION = version_file.read().strip()


def _main(filepaths, format='text', stream=sys.stdout, encoding=None, level=2):
    error_dicts = []
    error_occurred = False

    for filepath in filepaths:
        # Read and lint the file
        unfiltered_file_errors = lint_file(filepath, encoding=encoding)
        file_errors = [err for err in unfiltered_file_errors if err.level >= level]

        if not file_errors:
            if format == 'text':
                stream.write('INFO File {filepath} is clean.\n'.format(filepath=filepath))
        else:
            error_occurred = True
            if format == 'text':
                for err in file_errors:
                    # e.g. WARNING readme.rst:12 Title underline too short.
                    stream.write('{err.type} {err.source}:{err.line} {err.message}\n'.format(err=err))
            elif format == 'json':
                error_dicts.extend({
                    'line': err.line,
                    'source': err.source,
                    'level': err.level,
                    'type': err.type,
                    'message': err.message,
                    'full_message': err.full_message,
                } for err in file_errors)

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
    parser.add_argument('--level', default='warning', type=str, choices=LEVEL_MAP,
                        help='Minimum docutils linting error level to report and consider as failing '
                        '(lower case string, default is warning)')
    args = parser.parse_args()

    # Want the level strings to appear in the --help text via choices, so convert now:
    args.level = LEVEL_MAP[args.level]

    # Run the main argument
    _main(**args.__dict__)


if __name__ == '__main__':
    main()
