#!/usr/bin/env bash
# Exit on first error
set -e

# Install our dependencies
npm install foundry@~4.3.2 foundry-release-git@~2.0.2 foundry-release-pypi@~3.0.0

# Remove all `.pyc` files
shopt -s globstar
rm **/*.pyc || true
shopt -u globstar

# Run foundry release with an adjusted PATH
PATH="$PATH:$PWD/node_modules/.bin/"
foundry release $*
