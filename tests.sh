#!/usr/bin/env bash
export FILES=$(find src/test/ -type f -name "*.py" | grep -v "init")
python3.11 -m pytest $FILES --cov=. --cov-config=.coveragerc --cov-report html
