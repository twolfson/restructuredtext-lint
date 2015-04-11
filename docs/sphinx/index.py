# Load in our dependencies
from docutils.parsers.rst.directives import register_directive
from sphinx.directives.code import Highlight
import restructuredtext_lint

# Load our new directive
register_directive('highlight', Highlight)

# Lint our README
errors = restructuredtext_lint.lint_file('docs/sphinx/README.rst')
print errors[0].message # Error in "highlight" directive: no content permitted.
