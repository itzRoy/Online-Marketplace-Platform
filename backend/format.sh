#!/bin/sh -e

export PYTHONPATH=$(pwd):$PYTHONPATH

set -x
isort .
black . --line-length 78
flake8 --exclude __init__.py --max-line-length  99

