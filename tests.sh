#!/usr/bin/env bash
cd ..
export FILES=$(find src/test/ -type f -name "*.py" | grep -v "init")
python3.11 -m pytest $FILES --cov=. --cov-config=src/.coveragerc --cov-report html
