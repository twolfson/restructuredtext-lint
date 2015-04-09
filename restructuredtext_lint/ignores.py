import contextlib

from docutils.parsers import rst
from docutils.parsers.rst import directives as rst_directives
from docutils.parsers.rst import roles as rst_roles


class _IgnoredDirective(rst.Directive):
    """Stub for unknown directives.

    See: http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/__init__.py#l194

    See: https://github.com/myint/rstcheck/blob/v1.1.1/rstcheck.py#L217
    """
    has_content = True

    def run(self):
        return []


def _ignore_role(name, rawtext, text, lineno, inliner,
                 options=None, content=None):
    """Stub for unknown roles.

    See: http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/roles.py

    See: https://github.com/myint/rstcheck/blob/v1.1.1/rstcheck.py#L228
    """
    return ([], [])


def register_ignores(directives, roles):
    """Register ignoreable sphinx directives & roles.

    :param list directives: directives to ignore
    :param list roles: roles to ignore

    :rtype (list, list): tuple of directives and roles.
    """
    for directive in directives:
        rst_directives.register_directive(directive, _IgnoredDirective)
    for role in roles:
        rst_roles.register_local_role(role, _ignore_role)
    return (directives, roles)


def unregister_ignores(registered_directives, registered_roles):
    """Unregister previously registered sphinx directives & roles.

    :param list registered_directives: directives to unregister
    :param list registered_roles: roles to unregister
    """
    # TODO: this is a hack into the sphinx rst registries, there doesn't
    # appear to be any other way to get at these...
    all_directives = getattr(rst_directives, '_directives', {})
    for directive in registered_directives:
        all_directives.pop(directive, None)
    all_roles = getattr(rst_roles, '_roles', {})
    for role in registered_roles:
        all_roles.pop(role, None)


@contextlib.contextmanager
def register_unregister_ignores(directives, roles):
    """Register then unregister ignoreable sphinx directives & roles.

    :param list directives: directives to ignore
    :param list roles: roles to ignore
    """
    registered_directives, registered_roles = register_ignores(directives,
                                                               roles)
    try:
        yield
    finally:
        unregister_ignores(registered_directives, registered_roles)
