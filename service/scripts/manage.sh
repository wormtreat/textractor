#!/bin/bash
set -e

if [ "$1" = 'lint' ]
then
    echo "Linting..."
    pylint ./src
elif [ "$1" = 'test' ]
then
    echo "Testing..."
    pytest tests/*
# else
#     exec "$@"
fi
