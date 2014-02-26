import io
import docutils
from docutils.nodes import Element
from docutils.parsers.rst import Parser

def lint(content, filepath=None):
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

def lint_file(filepath, encoding=None):
    """Lint a specific file"""
    f = io.open(filepath, encoding=encoding)
    content = f.read()
    f.close()
    return lint(content, filepath)
