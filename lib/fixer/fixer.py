#!/usr/bin/python3
import sys
from abc import ABC
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from railway_fixer import RailwayFixer
from highway_fixer import HighwayFixer
from multipolygon_fixer import MultipolygonFixer
from fixer_base import FixerBase


class RelationFixer(FixerBase, ABC):
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
                return HighwayFixer().fixing(relation_info,first_way,is_from_api)
            else: # Multipolygon fixing
                return {"Error": "Not implemented yet."}
        else:
            return {"Error": "This relation type is not supported."}
    def correct_way_roles_tags(self, relation_info, corrected_ways_to_search):
        if relation_info["type"] != "public_transport":
            if relation_info["type"] == "route" and (
                    relation_info["route"] == "railway" or relation_info["route"] == "train"):
                return {"Error": "Not implemented yet."}
            elif relation_info["type"] == "route" and relation_info["route"] == "road":
                return HighwayFixer().correct_way_roles_tags(corrected_ways_to_search)
            else:  # Multipolygon fixing
                return {"Error": "Not implemented yet."}
        else:
            return {"Error": "This relation type is not supported."}
