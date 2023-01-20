#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import way_queries


class RailwayFixer:
    def correction_of_railway_route(self,relation_info,relation_id,first_way):
        pass
