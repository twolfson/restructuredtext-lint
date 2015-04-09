from __future__ import absolute_import

try:
    import sphinx  # noqa

    # All currently know sphinx domains.
    #
    # See: https://github.com/sphinx-doc/sphinx/tree/1.3/sphinx/domains
    from sphinx.domains import c as c_domain
    from sphinx.domains import cpp as cpp_domain
    from sphinx.domains import javascript as javascript_domain
    from sphinx.domains import python as python_domain
    from sphinx.domains import std as std_domain

    SPHINX_AVAILABLE = True
except ImportError:
    SPHINX_AVAILABLE = False

# Default and/or base roles/directives to ignore.
#
# See: http://sphinx-doc.org/markup/para.html
# And: http://sphinx-doc.org/markup/toctree.html#directive-toctree
# And: https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/directives/other.py
_base_sp_roles = ('ctype',)
_base_sp_directives = ('autosummary', 'centered', 'currentmodule',
                       'deprecated', 'hlist', 'include', 'index',
                       'literalinclude', 'no-code-block', 'seealso',
                       'toctree', 'todo', 'versionadded', 'versionchanged')


def fetch_ignore_roles_directives():
    """Extract all possible directives & roles that sphinx is aware of.

    Raises a ``RuntimeError`` if sphinx is not importable.

    :rtype dict: dict with 'directives' and 'roles' keys with list values.
    """
    if not SPHINX_AVAILABLE:
        raise RuntimeError("Sphinx roles can not be fetched without"
                           " sphinx being importable")
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

    return {
        'directives': sp_directives,
        'roles': sp_roles,
    }
