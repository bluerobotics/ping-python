#!/usr/bin/env bash

source ci/ci-functions.sh

echob "generating message api..."
test pip install jinja2
test generate/generate-python.py --output-dir=brping

echob "installing package..."
test python setup.py install

echob "testing message api..."
test python brping/pingmessage.py

echob "update gh pages..."
test pip install pyOpenSSL
test ci/deploy-gh-pages.sh

echob "deploying..."
test ci/deploy.sh
