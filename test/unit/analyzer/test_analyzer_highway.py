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
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from osm_data_parser import OSMDataParser
from analyzer import Analyzer
import analyzer_dicts
import way_queries
import previous_current

analyzer = Analyzer()


def test_is_role_backward():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_backward_role["ways_to_search"]
    first_node_current = way_queries.get_start_node(ways_to_search[0])
    last_node_current = way_queries.get_end_node(ways_to_search[0])
    current_role = way_queries.get_role(ways_to_search[0])
    current_role_not_backward = ""
    # Act
    first, last = analyzer.is_role_backward(first_node_current, last_node_current, current_role)
    first_not_backward, last_not_backward = analyzer.is_role_backward(first_node_current, last_node_current,
                                                                      current_role_not_backward)
    # Assert
    assert first, last == ["-2", "-1"]
    assert first_not_backward, last_not_backward == ["-1", "-2"]


def test_is_way_roundabout():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_if_roundabout["ways_to_search"]
    current_roundabout = way_queries.is_roundabout(ways_to_search[0])
    not_roundabout = way_queries.is_roundabout(ways_to_search[1])
    current_role = way_queries.get_role(ways_to_search[0])
    nodes = way_queries.get_nodes(ways_to_search[0])
    # Act
    last_roundabout_nodes = []  # init
    last_roundabout_nodes = analyzer.is_way_roundabout(current_roundabout, current_role, nodes, last_roundabout_nodes)
    last_roundabout_nodes_not_roundabout = analyzer.is_way_roundabout(not_roundabout, current_role, nodes,
                                                                      last_roundabout_nodes)
    # Assert
    assert last_roundabout_nodes == ["-1", "-2"]
    assert last_roundabout_nodes_not_roundabout == ["-1", "-2"]


def test_is_the_way_in_forward_way_series_beginning_way_is_forward():
    # Arrange
    ways_to_search_forward = analyzer_dicts.relation_info_highway_forward[
        "ways_to_search"]
    # 1th way: it's forward only
    role_of_the_first_way = way_queries.get_role(ways_to_search_forward[0])
    first_node_first_way = way_queries.get_start_node(ways_to_search_forward[0])
    last_node_first_way = way_queries.get_end_node(ways_to_search_forward[0])

    # 3-4th way(non-forward and forward):
    role_of_the_third_way = way_queries.get_role(ways_to_search_forward[2])
    role_of_the_fourth_way = way_queries.get_role(ways_to_search_forward[3])
    first_node_fourth_way = way_queries.get_start_node(ways_to_search_forward[3])
    last_node_fourth_way = way_queries.get_end_node(ways_to_search_forward[3])
    first_node_of_first_forward_way_in_the_series = -1
    last_node_of_first_forward_way_in_the_series = -1
    count_of_forward_roled_way_series = 0  # initially
    # Act
    # First condition: we check it for the beginning
    first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, \
    count_of_forward_roled_way_series = analyzer.is_the_way_in_forward_way_series(
        index_of_current_way=0,
        previous_role="", current_role=role_of_the_first_way,
        count_of_forward_roled_way_series=count_of_forward_roled_way_series,
        first_node_current=first_node_first_way,
        last_node_current=last_node_first_way,
        first_node_of_first_forward_way_in_the_series=first_node_of_first_forward_way_in_the_series,
        last_node_of_first_forward_way_in_the_series=last_node_of_first_forward_way_in_the_series)
    assert [first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
            count_of_forward_roled_way_series] == ['-1', '-2', 1]

    first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, \
    count_of_forward_roled_way_series = analyzer.is_the_way_in_forward_way_series(
        index_of_current_way=3,
        previous_role=role_of_the_third_way, current_role=role_of_the_fourth_way,
        count_of_forward_roled_way_series=count_of_forward_roled_way_series,
        first_node_current=first_node_fourth_way,
        last_node_current=last_node_fourth_way,
        first_node_of_first_forward_way_in_the_series=first_node_of_first_forward_way_in_the_series,
        last_node_of_first_forward_way_in_the_series=last_node_of_first_forward_way_in_the_series)
    assert [first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
            count_of_forward_roled_way_series] == ['-4', '-5', 2]


def test_is_the_way_in_forward_way_series_not_forward():
    # chose an arbritrary existing array which has no forward ways.
    ways_to_search_non_forward = analyzer_dicts.relation_info_highway_to_test_if_roundabout["ways_to_search"]
    first_node_of_first_forward_way_in_the_series = '-1'
    last_node_of_first_forward_way_in_the_series = '-1'
    count_of_forward_roled_way_series = 0
    role_of_the_first_way = way_queries.get_role(ways_to_search_non_forward[0])
    role_of_the_second_way = way_queries.get_role(ways_to_search_non_forward[0])
    first_node_first_way = way_queries.get_start_node(ways_to_search_non_forward[1])
    last_node_first_way = way_queries.get_end_node(ways_to_search_non_forward[1])
    first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, \
    count_of_forward_roled_way_series = analyzer.is_the_way_in_forward_way_series(
        index_of_current_way=3,
        previous_role=role_of_the_first_way, current_role=role_of_the_second_way,
        count_of_forward_roled_way_series=count_of_forward_roled_way_series,
        first_node_current=first_node_first_way,
        last_node_current=last_node_first_way,
        first_node_of_first_forward_way_in_the_series=first_node_of_first_forward_way_in_the_series,
        last_node_of_first_forward_way_in_the_series=last_node_of_first_forward_way_in_the_series)
    assert [first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
            count_of_forward_roled_way_series] == ['-1', '-1', 0]
