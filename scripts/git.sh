#!/bin/bash

MSG="autopush"
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -e|--extension)
    MSG="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    MSG="$1" # save it in an array for later
    shift # past argument
    ;;
esac
done

# ***** PUSHING *****

echo $(git status)
echo ">>>[Adding files ...]"
git add .
echo ">>>[Commit message: '${MSG}}']"
git commit -m "$MSG"
echo ">>>[Pushing ...]"
git push

