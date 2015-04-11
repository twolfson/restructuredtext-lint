# Load in our dependencies
# DEV: Use `absolute_import` to remove confusion about where `sphinx` comes from
from __future__ import absolute_import
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.roles import register_local_role

# Define placeholder for memoization
memo_map = {}


# Start our Sphinx helpers
def get_builtin_domains():
    """Helper to retrieve domains from Sphinx"""
    # Attempt to load memoized BUILTIN_DOMAINS
    if memo_map.get('_BUILTIN_DOMAINS') is not None:
        return memo_map['_BUILTIN_DOMAINS']

    # Otherwise, import Sphinx's builtin domains
    #   https://github.com/sphinx-doc/sphinx/tree/1.3/sphinx/domains
    # DEV: We lazy load this to avoid loading Sphinx directives prematurely
    from sphinx.domains import BUILTIN_DOMAINS
    memo_map['_BUILTIN_DOMAINS'] = BUILTIN_DOMAINS
    return memo_map['_BUILTIN_DOMAINS']


def register_domain(domain):
    """Register a specific builtin domain to `docutils

    :param str key: Name of builtin domain (e.g. `c`, `cpp`, `py`)
        https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/domains/__init__.py#L285-L292
    """
    # https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/domains/python.py#L582-L622
    domain_name = domain.name
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/directives/__init__.py#l134  # noqa
    for directive_name, directive in domain.directives.items():
        name = '{domain}:{directive}'.format(domain=domain_name, directive=directive_name)
        register_directive(name, directive)
    # http://repo.or.cz/w/docutils.git/blob/1976ba91eff979abc3e13e5d8cb68324833af6a0:/docutils/parsers/rst/roles.py#l146  # noqa
    # https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/application.py#L590-L592
    for role_name, role in domain.roles.items():
        name = '{domain}:{role}'.format(domain=domain_name, role=role_name)
        register_local_role(name, role)


def register_builtin_domains():
    """Register all Sphinx builtin domains to `docutils`"""
    builtin_domains = get_builtin_domains()
    for key in builtin_domains:
        register_domain(builtin_domains[key])
