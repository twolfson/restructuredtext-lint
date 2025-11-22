#!/usr/bin/env bash
# Exit on first error and echo commands
set -e
set -x

# Run our linter and tests
if test "$SKIP_LINT" != "TRUE"; then
  flake8 --max-line-length=120 restructuredtext_lint
fi
nose3-py3 --nocapture $*
