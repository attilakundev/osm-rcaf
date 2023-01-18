#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from osm_data_parser import OSMDataParser
from railway_analyzer import RailwayAnalyzer
from highway_analyzer import HighwayAnalyzer
from multipolygon_analyzer import MultipolygonAnalyzer
import way_queries
from previous_current import PreviousCurrentHighway
from error_hwy import ErrorHighway

railway_analyzer = RailwayAnalyzer()
highway_analyzer = HighwayAnalyzer()
multipolygon_analyzer = MultipolygonAnalyzer()


class Analyzer:
    def get_relation_info(self, loaded_relation_file, relation_id: str = ""):
        """This facilitates the retrieval of the relation's information. Relation ID is optional,
        because if you leave it empty, it automatically assigns the first relation for anaylzing.
        """
        data_parser = OSMDataParser()
        relation_info = data_parser.collect_information_about_the_relation(loaded_relation_file, relation_id)
        return relation_info

    def relation_checking(self, loaded_relation_file, relation_id: str = ""):
        """

        :param loaded_relation_file: xml file
        :param relation_id: this will be fed from front-end application or console, if you don't supply value, it
         assumes you want the first relation to be analyzed.
        :return: error_information, correct_ways_count
        """
        error_information = []
        relation_info = self.get_relation_info(loaded_relation_file, relation_id)
        # so it'll take whatever relation it is except if it's public transport because that can't be analyzed.
        if way_queries.get_relation_type(relation_info) != "public_transport":
            role_of_first_way = way_queries.get_role(relation_info["ways_to_search"][0])
            if "route" in relation_info and (
                    relation_info.get("route") == "railway" or relation_info.get("route") == "train"):
                return railway_analyzer.railway_checking(relation_info, error_information)
            elif "route" in relation_info:
                return highway_analyzer.highway_checking(relation_info, error_information, role_of_first_way)
            else:
                return multipolygon_analyzer.multipolygon_checking(relation_info, error_information)
        else:
            error_information.append(ErrorHighway(PreviousCurrentHighway(), "Not supported"))
            return error_information, 0
