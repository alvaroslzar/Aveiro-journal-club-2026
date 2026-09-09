#!/usr/bin/env bash
set -eu

git rev-parse --show-toplevel >/dev/null

git config --local filter.strip-notebook-output.clean \
  'python3 -m nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR'
git config --local filter.strip-notebook-output.smudge cat

echo "Notebook Git filter configured for this clone."