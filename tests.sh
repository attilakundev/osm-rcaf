#!/usr/bin/env bash
export FILES=$(find test/ -type f -name "*.py" | grep -v "init")
pytest $FILES --cov=. --cov-report html