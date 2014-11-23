#!/bin/bash

STRING_ADD="doing git add....."
STRING_COMMIT="doing git commit....."
STRING_PUSH="doing git push......"
STRING_COMMIT_MSG="'testing...'"

echo $STRING_ADD
git add .
echo $STRING_COMMIT
git commit -m $STRING_COMMIT_MSG
echo $STRING_PUSH
git push origin gh-pages
