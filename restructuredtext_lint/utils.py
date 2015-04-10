# Load in our dependencies
import contextlib

from docutils.parsers import rst
from docutils.parsers.rst import directives as rst_directives
from docutils.parsers.rst import roles as rst_roles


# Define our utilities
# http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/__init__.py#l194  # noqa
# https://github.com/myint/rstcheck/blob/v1.1.1/rstcheck.py#L217
class EmptyDirective(rst.Directive):
    """Stub for empty directives."""
    # Allow the directive to have content
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/__init__.py#l304  # noqa
    has_content = True

    # Do nothing when the directive is run
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/__init__.py#l319  # noqa
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/directives/body.py#l33  # noqa
    def run(self):
        return []


# http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/roles.py
# http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/roles.py#l184
# https://github.com/myint/rstcheck/blob/v1.1.1/rstcheck.py#L228
class EmptyRole(object, rst_roles.GenericRole):
    """Stub for empty roles"""
    def node_class(*args, **kwargs):
        return None

    def __init__(self, role_name):
        self.role_name = role_name


def register_directives_roles(directives, roles):
    """Register ignoreable sphinx directives and roles.

    :param list directives: directives to ignore
    :param list roles: roles to ignore

    :rtype (list, list): tuple of directives and roles.
    """
    # TODO: Do we need to generate dictionaries for each directive or can we distill its name from the object?
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/directives/__init__.py#l134  # noqa
    for directive in directives:
        # register_directive(name, directive)
        rst_directives.register_directive(directive['name'], directive['directive'])
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/roles.py#l146
    for role in roles:
        # register_local_role(name, role_fn)
        rst_roles.register_local_role(role['name'], role['role'])


def unregister_directives_roles(directives, roles):
    """Unregister previously registered sphinx directives and roles.

    :param list directives: directives to unregister
    :param list roles: roles to unregister
    """
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/directives/__init__.py#l73  # noqa
    all_directives = getattr(rst_directives, '_directives', {})
    for directive in directives:
        all_directives.pop(directive['name'], None)
    all_roles = getattr(rst_roles, '_roles', {})
    for role in roles:
        all_roles.pop(role['name'], None)


@contextlib.contextmanager
def use_directives_roles(directives=None, roles=None):
    """Register then unregister sphinx directives and roles.

        with using_directives_roles(sphinx_directives, sphinx_roles):
            _lint('file.py')

    :param list directives: directives to ignore
    :param list roles: roles to ignore
    """
    if directives is None:
        directives = []
    if roles is None:
        roles = []
    register_directives_roles(directives, roles)
    try:
        yield
    finally:
        unregister_directives_roles(directives, roles)
