from __future__ import absolute_import

SPHINX_AVAILABLE = True
try:
    # Import all known sphinx domains
    # See: https://github.com/sphinx-doc/sphinx/tree/1.3/sphinx/domains
    from sphinx import domains
except ImportError:
    SPHINX_AVAILABLE = False

# Default and/or base roles/directives to ignore.
#
# See: http://sphinx-doc.org/markup/para.html
# And: http://sphinx-doc.org/markup/toctree.html#directive-toctree
# And: https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/directives/other.py
_base_sphinx_roles = ('ctype',)
_base_sphinx_directives = ('autosummary', 'centered', 'currentmodule',
                           'deprecated', 'hlist', 'include', 'index',
                           'literalinclude', 'no-code-block', 'seealso',
                           'toctree', 'todo', 'versionadded', 'versionchanged')


def fetch_roles_directives():
    """Extract all possible directives & roles that sphinx is aware of.

    Raises a ``RuntimeError`` if sphinx is not importable.

    :rtype dict: dict with 'directives' and 'roles' keys with list values.
    """
    if not SPHINX_AVAILABLE:
        raise RuntimeError('`restructuredtext-lint` tried to `import sphinx`'
                           ' at the initial load time but was unable'
                           ' to. Please verify `sphinx` is installed'
                           ' properly.')

    sphinx_directives = list(_base_sphinx_directives)
    sphinx_roles = list(_base_sphinx_roles)

    # Get all the domains directives and roles and insert them.
    for name, domain_class in domains.BUILTIN_DOMAINS.items():

        domain_directives = getattr(domain_class, 'directives', [])
        domain_roles = getattr(domain_class, 'roles', [])

        # Ensure that we also use the name prefixed version as well
        # for example :py:func: and :func: are equivalent and we need to make
        # sure we register both kinds.
        sphinx_directives.extend(domain_directives)
        if name != 'std':
            sphinx_directives.extend('{domain}:{item}'.format(domain=domain_class.name,
                                                              item=item)
                                 for item in domain_directives)

        sphinx_roles.extend(domain_roles)
        if name != 'std':
            sphinx_roles.extend('{domain}:{item}'.format(domain=domain_class.name,
                                                         item=item)
                            for item in domain_roles)

    return {
        'directives': sphinx_directives,
        'roles': sphinx_roles,
    }
