#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import way_queries
from fixer_base import FixerBase


class RailwayFixer(FixerBase):

    def fixing(self, relation_info: dict, first_way: str = "", is_from_api: bool = True):
        pass
