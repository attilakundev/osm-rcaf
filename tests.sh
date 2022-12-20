#!/usr/bin/env bash
export FILES=`find test/ -type f -name "*.py" | grep -v "init"`
pytest $files