#!/usr/bin/env bash

# Deploy repository documentation

source ci/ci-functions.sh

doc_path="doc"

echob "generating message api..."
test pip install jinja2
test generate/generate-python.py --output-dir=brping

echob "Build doxygen documentation."
test cd $doc_path
test doxygen Doxyfile

echo "- Check files"
ls -A "html/"
