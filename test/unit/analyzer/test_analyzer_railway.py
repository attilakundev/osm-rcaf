#!/usr/bin/python3

from src.lib.analyzer.analyzer import Analyzer
from src.lib.analyzer.railway_analyzer import RailwayAnalyzer
from src.lib.model.previous_current import PreviousCurrentHighway
from src.test.files import analyzer_dicts
from src.lib import way_queries

railway_analyzer = RailwayAnalyzer()
analyzer = Analyzer()


def test_check_rails_if_the_ways_are_connected():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_railway_result_appended["ways_to_search"]
    prev_curr = PreviousCurrentHighway(first_node_previous=way_queries.get_start_node(ways_to_search[0]),
                                       last_node_previous=way_queries.get_end_node(ways_to_search[0]),
                                       first_node_current=way_queries.get_start_node(ways_to_search[1]),
                                       last_node_current=way_queries.get_end_node(ways_to_search[1]))
    is_error = railway_analyzer.check_rails_if_the_ways_are_not_connected(prev_curr)
    assert is_error is False


def test_check_rails_if_the_ways_are_not_connected():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_railway_result_appended["ways_to_search"]
    prev_curr = PreviousCurrentHighway(first_node_previous=way_queries.get_start_node(ways_to_search[1]),
                                       last_node_previous=way_queries.get_end_node(ways_to_search[1]),
                                       first_node_current=way_queries.get_start_node(ways_to_search[2]),
                                       last_node_current=way_queries.get_end_node(ways_to_search[2]))
    is_error = railway_analyzer.check_rails_if_the_ways_are_not_connected(prev_curr)
    assert is_error is True


def test_railway_checking():
    # Arrange - it's the relation_info_appended relation_info_result_appended
    error_information, correct_ways_count = railway_analyzer.checking(
        analyzer_dicts.relation_info_railway_result_appended)
    assert len(error_information) == 1
    assert correct_ways_count == 2


def test_system_test_for_railways():
    error_information, correct_ways_count = analyzer.relation_checking(
        analyzer_dicts.result_dict_multi_ways_rail)
    assert len(error_information) == 1
    assert correct_ways_count == 2
