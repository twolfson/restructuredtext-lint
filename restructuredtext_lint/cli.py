import argparse
import json
import sys

import lint

def _main(filepath, format='text', stream=sys.stdout):
    # Read and lint the file
    errors = lint.lint_file(filepath)

    # If there were no errors, exit gracefully
    if not errors:
        if format == 'json':
            stream.write(json.dumps(errors))
        else:
            stream.write('File was clean.\n')
        sys.exit(0)

    # Otherwise, output the errors and exit angrily
    if format == 'json':
        error_dicts = [{
            'line': error.line,
            'source': error.source,
            'level': error.level,
            'type': error.type,
            'message': error.message,
            'full_message': error.full_message,
        } for error in errors]
        stream.write(json.dumps(error_dicts))
    else:
        for error in errors:
            # WARNING readme.rst:12 Title underline too short.
            stream.write('%s %s:%s %s\n' % (error.type, error.source, error.line, error.message))
    sys.exit(1)

def main():
    # Set up options and parse arguments
    parser = argparse.ArgumentParser(description='Lint a reStructuredText file')
    parser.add_argument('filepath', type=str, help='File to lint')
    # TODO: Add format
    args = parser.parse_args()

    # Run the main argument
    _main(**args.__dict__)
