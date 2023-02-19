#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from railway_fixer import RailwayFixer
from highway_fixer import HighwayFixer
from multipolygon_fixer import MultipolygonFixer
from fixer_base import FixerBase

railway_fixer = RailwayFixer()
highway_fixer = HighwayFixer()
multipolygon_fixer = MultipolygonFixer()

class RelationFixer(FixerBase):
    def fixing(self, relation_info: dict,  first_way: str = "", is_from_api: bool = True):
        """

        :param is_from_api:
        :param relation_info: relation info from the analyzer
        :param relation_id: this will be fed from front-end application or console, if you don't supply value, it
         assumes you want the first relation to be fixed.
        :param first_way: the first way from which the relation gets assembled. If no value is supplied, the first member is taken as first.
        :return: corrected_relation: dict
        """

        if relation_info["type"] != "public_transport":
            if relation_info["type"] == "route" and (relation_info["route"] == "railway" or relation_info["route"] == "train"):
                return {"Error": "Not implemented yet."}
            elif relation_info["type"] == "route" and relation_info["route"] == "road":
                return highway_fixer.fixing(relation_info,first_way,is_from_api)
            else: # Multipolygon fixing
                return {"Error": "Not implemented yet."}
        else:
            return {"Error": "This relation type is not supported."}