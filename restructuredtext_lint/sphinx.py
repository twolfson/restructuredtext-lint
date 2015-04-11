# Load in our dependencies
# DEV: Use `absolute_import` to remove confusion about where `sphinx` comes from
from __future__ import absolute_import

BUILTIN_DOMAINS = None
try:
    # Import all known sphinx domains
    #   https://github.com/sphinx-doc/sphinx/tree/1.3/sphinx/domains
    from sphinx.domains import BUILTIN_DOMAINS
except ImportError:
    pass


# Define our constants
#   Default/base roles and directives for Sphinx
#   http://sphinx-doc.org/markup/para.html
#   http://sphinx-doc.org/markup/toctree.html#directive-toctree
#   https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/directives/other.py

# TODO: Is this really neecessary? We should be able to leverage BUILTIN_DOMAINS

BASE_SPHINX_ROLES = ('ctype',)
BASE_SPHINX_DIRECTIVES = ('autosummary', 'centered', 'currentmodule',
                          'deprecated', 'hlist', 'include', 'index',
                          'literalinclude', 'no-code-block', 'seealso',
                          'toctree', 'todo', 'versionadded', 'versionchanged')


def get_builtin_domains():
    """Helper to retrieve domains from Sphinx"""
    if BUILTIN_DOMAINS is None:
        raise RuntimeError('`restructuredtext-lint` tried to import `BUILTIN_DOMAINS` from `sphinx.domains` '
                           '(`from sphinx.domains import BUILTIN_DOMAINS`) at the initial load time but was unable to.'
                           'Please verify `sphinx` is installed properly.')
    return BUILTIN_DOMAINS


def register_builtin_domain(key):
    """Register a specific builtin domain to `docutils

    :param str key: Name of builtin domain (e.g. `c`, `cpp`, `py`)
        https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/domains/__init__.py#L285-L292
    """
    pass
    # # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/directives/__init__.py#l134  # noqa
    # if directives:
    #     for directive in directives:
    #         # register_directive(name, directive)
    #         rst_directives.register_directive(directive['name'], directive['directive'])
    # # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/roles.py#l146
    # if roles:
    #     for role in roles:
    #         # register_local_role(name, role_fn)
    #         rst_roles.register_local_role(role['name'], role['role_fn'])


def register_builtin_domains():
    """Register all Sphinx builtin domains to `docutils`"""
    pass
