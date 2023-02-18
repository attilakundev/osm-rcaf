#!/usr/bin/python3
import pytest
import sys
from pathlib import Path
import requests
import xml

import xmltodict

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/analyzer")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from analyzer import Analyzer
from railway_analyzer import RailwayAnalyzer
import analyzer_dicts
import way_queries

railway_analyzer = RailwayAnalyzer()
analyzer = Analyzer()


def test_check_rails_if_the_ways_are_connected():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_railway_result_appended["ways_to_search"]
    first_node_previous = way_queries.get_start_node(ways_to_search[0])
    last_node_previous = way_queries.get_end_node(ways_to_search[0])
    first_node_current = way_queries.get_start_node(ways_to_search[1])
    last_node_current = way_queries.get_end_node(ways_to_search[1])
    is_error = railway_analyzer.check_rails_if_the_ways_are_not_connected(first_node_previous=first_node_previous,
                                                                          last_node_previous=last_node_previous,
                                                                          first_node_current=first_node_current,
                                                                          last_node_current=last_node_current)
    assert is_error is False


def test_check_rails_if_the_ways_are_not_connected():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_railway_result_appended["ways_to_search"]
    first_node_previous = way_queries.get_start_node(ways_to_search[1])
    last_node_previous = way_queries.get_end_node(ways_to_search[1])
    first_node_current = way_queries.get_start_node(ways_to_search[2])
    last_node_current = way_queries.get_end_node(ways_to_search[2])
    is_error = railway_analyzer.check_rails_if_the_ways_are_not_connected(first_node_previous=first_node_previous,
                                                                          last_node_previous=last_node_previous,
                                                                          first_node_current=first_node_current,
                                                                          last_node_current=last_node_current)
    assert is_error is True


def test_railway_checking():
    # Arrange - it's the relation_info_appended relation_info_result_appended
    error_information = []
    error_information, correct_ways_count = railway_analyzer.checking(
        analyzer_dicts.relation_info_railway_result_appended, error_information)
    assert len(error_information) == 1
    assert correct_ways_count == 2


def test_system_test_for_railways():
    error_information, correct_ways_count = analyzer.relation_checking(
        analyzer_dicts.result_dict_multi_ways_rail)
    assert len(error_information) == 1
    assert correct_ways_count == 2
