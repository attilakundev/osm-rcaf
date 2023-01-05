#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from previous_current import PreviousCurrentMultipolygon
from error_hwy import ErrorMultipolygon
import way_queries

class MultipolygonAnalyzer:
    def multipolygon_checking(self, relation_info: list, error_information: list):
        return ""
