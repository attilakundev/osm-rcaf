#!/usr/bin/python3
import pytest
import sys
from pathlib import Path
import requests
import xml

import xmltodict

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from osm_data_parser import OSMDataParser
from analyzer import Analyzer
import analyzer_dicts
import way_queries
import previous_current

analyzer = Analyzer()


# TESTS FOR RAILWAY CHECKING
def test_check_rails_if_the_ways_are_connected():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_railway_result_appended["ways_to_search"]
    first_node_previous = way_queries.get_start_node(ways_to_search[0])
    last_node_previous = way_queries.get_end_node(ways_to_search[0])
    first_node_current = way_queries.get_start_node(ways_to_search[1])
    last_node_current = way_queries.get_end_node(ways_to_search[1])
    is_error = analyzer.check_rails_if_the_ways_are_not_connected(first_node_previous=first_node_previous,
                                                                             last_node_previous=last_node_previous,
                                                                             first_node_current=first_node_current,
                                                                             last_node_current=last_node_current)
    assert is_error == False


def test_check_rails_if_the_ways_are_not_connected():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_railway_result_appended["ways_to_search"]
    first_node_previous = way_queries.get_start_node(ways_to_search[1])
    last_node_previous = way_queries.get_end_node(ways_to_search[1])
    first_node_current = way_queries.get_start_node(ways_to_search[2])
    last_node_current = way_queries.get_end_node(ways_to_search[2])
    is_error = analyzer.check_rails_if_the_ways_are_not_connected(first_node_previous=first_node_previous,
                                                                         last_node_previous=last_node_previous,
                                                                         first_node_current=first_node_current,
                                                                         last_node_current=last_node_current)
    assert is_error == True


def test_railway_checking():
    # Arrange - it's the relation_info_appended relation_info_result_appended
    error_information, correct_ways_count = analyzer.railway_checking(
        analyzer_dicts.relation_info_railway_result_appended)
    assert len(error_information) == 1
    assert correct_ways_count == 2


def test_system_test_for_railways():
    error_information, correct_ways_count = analyzer.relation_checking(analyzer_dicts.result_dict_multi_ways_rail)
    assert len(error_information) == 1
    assert correct_ways_count == 2

# TESTS FOR HIGHWAY CHECKING

# TESTS FOR MULTIPOLYGON CHECKING
