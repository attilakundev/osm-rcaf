#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")
from fixer_base import FixerBase
import way_queries


class MultipolygonFixer(FixerBase):

    def fixing(self, relation_info: dict, first_way: str = "", is_from_api: bool = True):
        return None, None