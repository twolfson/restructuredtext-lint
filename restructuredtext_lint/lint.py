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

    # Configure publisher
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l201
    settings = pub.get_settings()
    pub.set_io()

    # Parse content
    # DEV: We avoid the `read` method because when `source` is `None`, it attempts to read from `stdin`. However, we already know our content.
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/readers/__init__.py#l66
    reader = pub.reader
    reader.source = pub.source
    if not reader.parser:
        reader.parser = pub.parser
    reader.settings = settings
    reader.input = content
    reader.parse()
    document = reader.document

    # Apply transforms/collect errors
    document.transformer.populate_from_components(
            (pub.source, pub.reader, pub.reader.parser, pub.writer,
             pub.destination))

    # Disable stdout
    # TODO: Find a more proper way to do this
    # TODO: We might exit the program if a certain error level is reached
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

    # Parse the content and return our collected errors
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/transforms/__init__.py#l159
    # DEV: We cannot use `apply_transforms` since it has `attach_observer` baked in. We want only our listener.
    transformer = document.transformer
    while transformer.transforms:
        if not transformer.sorted:
            # Unsorted initially, and whenever a transform is added.
            transformer.transforms.sort()
            transformer.transforms.reverse()
            transformer.sorted = 1
        priority, transform_class, pending, kwargs = transformer.transforms.pop()
        transform = transform_class(transformer.document, startnode=pending)
        transform.apply(**kwargs)
        transformer.applied.append((priority, transform_class, pending, kwargs))
    return errors

def lint_file(filepath, encoding=None):
    """Lint a specific file"""
    f = io.open(filepath, encoding=encoding)
    content = f.read()
    f.close()
    return lint(content, filepath)
