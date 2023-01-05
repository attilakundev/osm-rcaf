#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from osm_data_parser import OSMDataParser
from railway_analyzer import RailwayAnalyzer
from highway_analyzer import HighwayAnalyzer
from multipolygon_analyzer import MultipolygonAnalyzer
import way_queries

railway_analyzer = RailwayAnalyzer()
highway_analyzer = HighwayAnalyzer()
multipolygon_analyzer = MultipolygonAnalyzer()

class Analyzer:
    def get_relation_info(self, loaded_relation):
        data_parser = OSMDataParser()
        relation_info = data_parser.collect_information_about_the_relation(loaded_relation)  # generalized function
        return relation_info

    def relation_checking(self, loaded_relation):
        """

        :param loaded_relation: xml file
        :return: error_information, correct_ways_count
        """
        error_information = []
        relation_info = self.get_relation_info(loaded_relation)
        # so it'll take whatever relation it is
        if way_queries.get_relation_type(relation_info) != "public_transport":
            role_of_first_way = way_queries.get_role(relation_info["ways_to_search"][0])
            if "route" in relation_info and (
                    relation_info.get("route") == "railway" or relation_info.get("route") == "train"):
                return railway_analyzer.railway_checking(relation_info, error_information)
            elif "route" in relation_info:
                return highway_analyzer.highway_checking(relation_info, error_information, role_of_first_way)
            else:
                return multipolygon_analyzer.multipolygon_checking(relation_info, error_information)
        return "OutOfScope"