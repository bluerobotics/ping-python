#!/usr/bin/env bash

# source helper functions
source ci/ci-functions.sh

# TODO make test() work with | pipe
cat ci/deploy-whitelist | xargs git add -f
# commit generated files if necessary, it's ok if commit fails
git commit -m "temporary commit"
# move to deployment branch
test git checkout deployment
test rm -rf *
# get the list of files that should be version controlled in deployment branch
test git checkout HEAD@{1} ci/deploy-whitelist
# add those files
cat ci/deploy-whitelist | xargs git checkout HEAD@{1}
test git --no-pager diff --staged
# unstage the whitelist
test git rm -f ci/deploy-whitelist
