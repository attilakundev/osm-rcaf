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

railway_fixer = RailwayFixer()
highway_fixer = HighwayFixer()
multipolygon_fixer = MultipolygonFixer()

class Fixer:
    def correct_relation(self, relation_info: dict, relation_id: str = "", first_way: str = ""):
        """

        :param relation_info: relation info from the analyzer
        :param relation_id: this will be fed from front-end application or console, if you don't supply value, it
         assumes you want the first relation to be fixed.
        :param first_way: the first way from which the relation gets assembled. If no value is supplied, the first member is taken as first.
        :return: corrected_xml_file: xml file
        """

        if relation_info["type"] != "public_transport":
            if relation_info["type"] == "route" and (relation_info["route"] == "railway" or relation_info["route"] == "train"):
                railway_fixer.correction_of_railway_route(relation_info,relation_id,first_way)
            elif relation_info["type"] == "route" and relation_info["route"] == "road":
                pass
            else:
                pass
        else:
            return {"Error": "This relation type is not supported."}