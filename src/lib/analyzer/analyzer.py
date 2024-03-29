#!/usr/bin/python3
import logging

import src.lib.osm_data_parser as data_parser
import src.lib.way_queries as way_queries
from src.lib.analyzer.railway_analyzer import RailwayAnalyzer
from src.lib.analyzer.highway_analyzer import HighwayAnalyzer
from src.lib.analyzer.multipolygon_analyzer import MultipolygonAnalyzer
from src.lib.model.previous_current import PreviousCurrentHighway
from src.lib.model.error_hwy import ErrorHighway

railway_analyzer = RailwayAnalyzer()
highway_analyzer = HighwayAnalyzer()
multipolygon_analyzer = MultipolygonAnalyzer()
class Analyzer:
    def get_relation_info(self, loaded_relation_file, relation_id: str = ""):
        """This facilitates the retrieval of the relation's information. Relation ID is optional,
        because if you leave it empty, it automatically assigns the first relation for analyzing.
        """
        relation_info = data_parser.collect_information_about_the_relation(loaded_relation_file, relation_id)
        return relation_info

    def relation_checking(self, loaded_relation_file, relation_id: str = ""):
        """

        :param loaded_relation_file: xml file
        :param relation_id: this will be fed from front-end application or console, if you don't supply value, it
         assumes you want the first relation to be analyzed.
        :return: error_information, correct_ways_count
        """
        logging.info(f"Getting relation info of {relation_id}")
        relation_info = self.get_relation_info(loaded_relation_file, relation_id)
        error_information = []
        logging.info(f"Starting analyzing {relation_id}")
        # so it'll take whatever relation it is except if it's public transport because that can't be analyzed.
        if way_queries.get_relation_type(relation_info) != "public_transport":

            if "route" in relation_info and (
                    relation_info.get("route") == "railway" or relation_info.get("route") == "train"):
                return railway_analyzer.checking(relation_info,relation_id)
            elif "route" in relation_info:
                return highway_analyzer.checking(relation_info,relation_id)
            else:
                return multipolygon_analyzer.checking(relation_info,relation_id)
        else:
            error_information.append(ErrorHighway(PreviousCurrentHighway(), "Not supported"))
            return error_information, 0, 0
