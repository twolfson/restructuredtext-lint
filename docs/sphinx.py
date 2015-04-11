# Load in our dependencies
import restructuredtext_lint
from docutils.parsers.rst.directives import register_directive
from sphinx.directives.code import Highlight

errors = restructuredtext_lint.lint_file('docs/sphinx.rst')
print errors[0].message

