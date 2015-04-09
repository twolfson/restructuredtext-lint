from __future__ import absolute_import

import contextlib

try:
    import sphinx  # noqa

    from sphinx.domains import c as c_domain
    from sphinx.domains import cpp as cpp_domain
    from sphinx.domains import javascript as javascript_domain
    from sphinx.domains import python as python_domain
    from sphinx.domains import std as std_domain

    SPHINX_AVAILABLE = True
except ImportError:
    SPHINX_AVAILABLE = False

from docutils.parsers import rst
from docutils.parsers.rst import directives as rst_directives
from docutils.parsers.rst import roles as rst_roles

# Default and/or base roles/directives to ignore.
_base_sp_roles = tuple(['ctype'])
_base_sp_directives = tuple(['autosummary',
                             'centered', 'currentmodule', 'deprecated',
                             'hlist', 'include', 'index',
                             'literalinclude', 'no-code-block',
                             'seealso', 'toctree', 'todo',
                             'versionadded', 'versionchanged'])


class _IgnoredDirective(rst.Directive):
    """Stub for unknown directives.

    See: https://github.com/myint/rstcheck/blob/master/rstcheck.py#L305
    """
    has_content = True

    def run(self):
        return []


def _ignore_role(name, rawtext, text, lineno, inliner,
                 options=None, content=None):
    """Stub for unknown roles.

    See: https://github.com/myint/rstcheck/blob/master/rstcheck.py#L316
    """
    return ([], [])


def _fetch_roles_directives(no_skip_directives=None, no_skip_roles=None):
    # Extract all possible directives & roles that sphinx is aware of for
    # all known sphinx domains, and then remove the ones we do not want to
    # skip (and return them).
    sp_directives = list(_base_sp_directives)
    sp_directives.extend(std_domain.StandardDomain.directives)
    sp_roles = list(_base_sp_roles)
    sp_roles.extend(std_domain.StandardDomain.roles)

    for (domain, class_name) in [(c_domain, 'CDomain'),
                                 (cpp_domain, 'CPPDomain'),
                                 (javascript_domain, 'JavaScriptDomain'),
                                 (python_domain, 'PythonDomain')]:

        # Get all the domains directives and roles and insert them.
        domain_class = getattr(domain, class_name)
        domain_directives = getattr(domain_class, 'directives', [])
        domain_roles = getattr(domain_class, 'roles', [])

        sp_directives.extend(domain_directives)

        # Ensure that we also use the name prefixed version as well
        # for example :py:func: and :func: are equivalent and we need to make
        # sure we register both kinds.
        sp_directives.extend('%s:%s' % (domain_class.name, item)
                             for item in domain_directives)

        sp_roles.extend(domain_roles)
        sp_roles.extend('%s:%s' % (domain_class.name, item)
                        for item in domain_roles)

    # Filter out the ones we desire to avoid skipping (if any)...
    if not no_skip_directives:
        no_skip_directives = []
    if not no_skip_roles:
        no_skip_roles = []
    ok_directives = []
    for directive in sp_directives:
        if directive not in no_skip_directives:
            ok_directives.append(directive)
    ok_roles = []
    for role in sp_roles:
        if role not in no_skip_roles:
            ok_roles.append(role)
    return (ok_directives, ok_roles)


def register_ignores(no_skip_directives=None, no_skip_roles=None):
    """Register ignoreable sphinx directives.

    Does nothing if sphinx is not importable.

    :param list/set no_skip_directives: directives to not skip
    :param list/set no_skip_roles: roles to not skip
    """
    if not SPHINX_AVAILABLE:
        return ([], [])
    ok_directives, ok_roles = _fetch_roles_directives(
        no_skip_directives=no_skip_directives,
        no_skip_roles=no_skip_roles)
    for directive in ok_directives:
        rst_directives.register_directive(directive, _IgnoredDirective)
    for role in ok_roles:
        rst_roles.register_local_role(role, _ignore_role)
    return (ok_directives, ok_roles)


def unregister_ignores(registered_directives, registered_roles):
    """Unregister previously registered sphinx directives.

    Does nothing if sphinx is not importable.

    :param list/set registered_directives: directives to unregister
    :param list/set registered_roles: roles to unregister
    """
    if not SPHINX_AVAILABLE:
        return
    # TODO: this is a hack into the sphinx rst registries, there doesn't
    # appear to be any other way to get at these...
    all_directives = getattr(rst_directives, '_directives', {})
    for directive in registered_directives:
        all_directives.pop(directive, None)
    all_roles = getattr(rst_roles, '_roles', {})
    for role in registered_roles:
        all_roles.pop(role, None)


@contextlib.contextmanager
def register_unregister_ignores(no_skip_directives=None, no_skip_roles=None):
    """Register then unregister ignoreable sphinx directives.

    Does nothing if sphinx is not importable.

    :param list/set no_skip_directives: directives to not skip
    :param list/set no_skip_roles: roles to not skip
    """
    registered_directives, registered_roles = register_ignores(
        no_skip_directives=no_skip_directives,
        no_skip_roles=no_skip_roles)
    try:
        yield
    finally:
        unregister_ignores(registered_directives, registered_roles)
