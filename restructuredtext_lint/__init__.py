import argparse
import json
import sys

import docutils
from docutils.nodes import Element
from docutils.parsers.rst import Parser

def lint(content, filepath=None, **kwargs):
    """Lint reStructuredText and return errors

    :param string content: reStructuredText to be linted
    :param string filepath: Optional path to file, this will be returned as the source
    :rtype list: List of errors. Each error will contain a line, source (filepath),
        message (error message), and full message (error message + source lines)
    """
    # Generate a new parser
    parser = Parser()
    settings = docutils.frontend.OptionParser(
                    components=(docutils.parsers.rst.Parser,)
                    ).get_default_values()
    document = docutils.utils.new_document(filepath, settings=settings)

    # Disable stdout
    # TODO: Find a more proper way to do this
    # TODO: We might exit the program is a certain error level is reached
    document.reporter.stream = None

    # Collect errors via an observer
    errors = []
    def error_collector(data):
        # Mutate the data since it was just generated
        data.type = data['type']
        data.level = data['level']
        data.message = Element.astext(data.children[0])
        data.full_message = Element.astext(data)

        # Save the error
        errors.append(data)
    document.reporter.attach_observer(error_collector)

    # Parse the content and return our collected errors
    parser.parse(content, document)
    return errors

def cli():
    # Set up options and parse arguments
    parser = argparse.ArgumentParser(description='Lint a reStructuredText file')
    parser.add_argument('filepath', type=str, help='File to lint')
    args = parser.parse_args()

    # Lint the file
    with open(args.filepath) as f:
        # Read and lin the file
        content = f.read()
        errors = lint(content, args.filepath)

        # If there were no errors, exit gracefully
        if not errors:
            print 'File was clean.'
            sys.exit(0)

        # Otherwise, output the errors as JSON
        error_dicts = [{
            'line': error.line,
            'source': error.source,
            'level': error.level,
            'type': error.type,
            'message': error.message,
            'full_message': error.full_message,
        } for error in errors]
        print json.dumps(error_dicts)

        sys.exit(1)
