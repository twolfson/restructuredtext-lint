# Load in our dependencies
from __future__ import absolute_import
from restructuredtext_lint.lint import lint, lint_file

# Export lint functions
lint = lint
lint_file = lint_file

__version__ = '0.14.4'
