import io
from docutils import utils
from docutils.core import Publisher
from docutils.nodes import Element

from restructuredtext_lint import ignores


def _lint(content, filepath=None):
    # Generate a new parser (copying `rst2html.py` flow)
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/tools/rst2html.py
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l348
    pub = Publisher(None, None, None, settings=None)
    pub.set_components('standalone', 'restructuredtext', 'pseudoxml')

    # Configure publisher
    # DEV: We cannot use `process_command_line` since it processes `sys.argv` which is for `rst-lint`, not `docutils`
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l201
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l143
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l118
    settings = pub.get_settings(halt_level=5)
    pub.set_io()

    # Prepare a document to parse on
    # DEV: We avoid the `read` method because when `source` is `None`, it attempts to read from `stdin`.
    #      However, we already know our content.
    # DEV: We create our document without `parse` because we need to attach observer's before parsing
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/readers/__init__.py#l66
    reader = pub.reader
    document = utils.new_document(filepath, settings)

    # Disable stdout
    # TODO: Find a more proper way to do this
    # TODO: We might exit the program if a certain error level is reached
    document.reporter.stream = None

    # Collect errors via an observer
    errors = []

    def error_collector(data):
        # Mutate the data since it was just generated
        data.line = data.get('line')
        data.source = data['source']
        data.level = data['level']
        data.type = data['type']
        data.message = Element.astext(data.children[0])
        data.full_message = Element.astext(data)

        # Save the error
        errors.append(data)
    document.reporter.attach_observer(error_collector)

    # Parse the content (and collect errors)
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/readers/__init__.py#l75
    reader.parser.parse(content, document)

    # Apply transforms (and more collect errors)
    # DEV: We cannot use `apply_transforms` since it has `attach_observer` baked in. We want only our listener.
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/core.py#l195
    # http://repo.or.cz/w/docutils.git/blob/422cede485668203abc01c76ca317578ff634b30:/docutils/docutils/transforms/__init__.py#l159
    document.transformer.populate_from_components(
        (pub.source, pub.reader, pub.reader.parser, pub.writer, pub.destination)
    )
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


def lint(content, filepath=None, custom_directives=None, custom_roles=None):
    """Lint reStructuredText and return errors

    :param string content: reStructuredText to be linted
    :param string filepath: Optional path to file, this will be returned as the source
    :param list custom_directives: custom directives to ignore
    :param list custom_roles: custom roles to ignore
    :rtype list: List of errors. Each error will contain a line, source (filepath),
        message (error message), and full message (error message + source lines)
    """
    with ignores.register_unregister_ignores(directives=custom_directives,
                                             roles=custom_roles):
        return _lint(content, filepath=filepath)


def lint_file(filepath, encoding=None, **kwargs):
    """Lint a specific file"""
    f = io.open(filepath, encoding=encoding)
    content = f.read()
    f.close()
    return lint(content, filepath=filepath, **kwargs)
