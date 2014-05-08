import io
import docutils
from docutils.core import Publisher
from docutils.nodes import Element
from docutils.parsers.rst import Parser

def lint(content, filepath=None):
    """Lint reStructuredText and return errors

    :param string content: reStructuredText to be linted
    :param string filepath: Optional path to file, this will be returned as the source
    :rtype list: List of errors. Each error will contain a line, source (filepath),
        message (error message), and full message (error message + source lines)
    """
    # Generate a new parser (copying `rst2html.py` flow)
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/tools/rst2html.py
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l348
    pub = Publisher(None, None, None, settings=None)
    pub.set_components('standalone', 'restructuredtext', 'pseudoxml')

    # Read content
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l216
    if pub.settings is None:
        pub.process_command_line()
    pub.set_io()
    pub.document = pub.reader.read(pub.source, pub.parser,
                                 pub.settings)
    print pub.document
    pub.apply_transforms()

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
        data.line = data['line']
        data.source = data['source']
        data.level = data['level']
        data.type = data['type']
        data.message = Element.astext(data.children[0])
        data.full_message = Element.astext(data)

        # Save the error
        errors.append(data)
    document.reporter.attach_observer(error_collector)
    print errors

    # Parse the content and return our collected errors
    parser.parse(content, document)
    return errors

def lint_file(filepath, encoding=None):
    """Lint a specific file"""
    f = io.open(filepath, encoding=encoding)
    content = f.read()
    f.close()
    return lint(content, filepath)
