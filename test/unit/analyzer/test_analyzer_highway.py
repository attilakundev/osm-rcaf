#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from osm_data_parser import OSMDataParser
from analyzer import Analyzer
import analyzer_dicts
import way_queries_dicts
import way_queries
from previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon
from error_hwy import ErrorHighway, ErrorMultipolygon

analyzer = Analyzer()


def test_is_role_backward():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_backward_role["ways_to_search"]
    first_node_current = way_queries.get_start_node(ways_to_search[0])
    last_node_current = way_queries.get_end_node(ways_to_search[0])
    current_role = way_queries.get_role(ways_to_search[0])
    current_nodes_before_reverse = way_queries.get_nodes(ways_to_search[0])
    # Act
    first, last, current_role, current_nodes = analyzer.is_role_backward(first_node_current, last_node_current,
                                                                         current_role, current_nodes_before_reverse)
    # Assert
    assert [first, last, current_role] == ["-4", "-1", "forward"]
    assert current_nodes == ["-4", "-3", "-2", "-1"]
    assert current_nodes_before_reverse == ["-1", "-2", "-3", "-4"]


def test_is_role_not_backward():
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_backward_role["ways_to_search"]
    first_node_current = way_queries.get_start_node(ways_to_search[0])
    last_node_current = way_queries.get_end_node(ways_to_search[0])
    current_role = "forward"
    current_nodes_before_reverse = way_queries.get_nodes(ways_to_search[0])
    first, last, current_role, current_nodes = analyzer.is_role_backward(first_node_current, last_node_current,
                                                                         current_role, current_nodes_before_reverse)
    assert [first, last, current_role] == ["-1", "-4", "forward"]
    assert current_nodes == ["-1", "-2", "-3", "-4"]


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
    ways = analyzer_dicts.relation_info_highway_forward[
        "ways_to_search"]
    # 1th way: it's forward only
    role_of_the_first_way = way_queries.get_role(ways[0])
    first_node_first_way = way_queries.get_start_node(ways[0])
    last_node_first_way = way_queries.get_end_node(ways[0])

    # 3-4th way(non-forward and forward):
    role_of_the_third_way = way_queries.get_role(ways[2])
    role_of_the_fourth_way = way_queries.get_role(ways[3])
    first_node_fourth_way = way_queries.get_start_node(ways[3])
    last_node_fourth_way = way_queries.get_end_node(ways[3])
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
    ways = analyzer_dicts.relation_info_highway_to_test_if_roundabout["ways_to_search"]
    first_node_of_first_forward_way_in_the_series = '-1'
    last_node_of_first_forward_way_in_the_series = '-1'
    count_of_forward_roled_way_series = 0
    role_of_the_first_way = way_queries.get_role(ways[0])
    role_of_the_second_way = way_queries.get_role(ways[0])
    first_node_first_way = way_queries.get_start_node(ways[1])
    last_node_first_way = way_queries.get_end_node(ways[1])
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


def test_check_if_there_is_gap_at_the_beginning():
    # Arrange
    ways = analyzer_dicts.relation_info_gap_in_first_forward_series["ways_to_search"]
    index_of_current_way = 3  # let's suppose that the way is detached from the merging beginning split at position 3
    count_of_forward_roled_series = 1  # this is a forward way series
    role_of_first_way = way_queries.get_role(ways[0])
    is_mutcd = False
    currently_checked_ref = way_queries.get_way_ref(ways[index_of_current_way])
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    last_forward_way_before_backward_direction = [way_queries.get_way_ref(ways[index_of_current_way - 2]),
                                                  way_queries.get_end_node(ways[index_of_current_way - 2])]
    has_directional_roles = False  # hardcoded because I can't find a better way. let's suppose it doesn't have directional ways
    previous_current = PreviousCurrentHighway(currently_checked_ref=currently_checked_ref,
                                              last_forward_way_before_backward_direction=last_forward_way_before_backward_direction,
                                              first_node_previous=first_node_previous,
                                              first_node_current=first_node_current,
                                              last_node_previous=last_node_previous,
                                              last_node_current=last_node_current,
                                              previous_role=previous_role, current_role=current_role)
    error_information = []
    # Act
    has_directional_roles, error_information = analyzer.check_if_there_is_gap_at_the_beginning(index_of_current_way,
                                                                                               count_of_forward_roled_series,
                                                                                               role_of_first_way,
                                                                                               is_mutcd, previous_role,
                                                                                               current_role,
                                                                                               first_node_previous,
                                                                                               last_node_previous,
                                                                                               first_node_current,
                                                                                               last_node_current,
                                                                                               last_forward_way_before_backward_direction,
                                                                                               has_directional_roles,
                                                                                               error_information,
                                                                                               previous_current)

    assertion = ErrorHighway(previous_current, "Gap at the beginning")
    assert type(error_information[0]) == ErrorHighway
    assert error_information[0].prev_curr == previous_current
    assert error_information[0].error_type == "Gap at the beginning"
    assert has_directional_roles is False


def test_check_if_there_is_gap_at_the_beginning_USA():
    ways = analyzer_dicts.relation_info_gap_in_first_forward_series["ways_to_search"]
    index_of_current_way = 3  # let's suppose that the way is detached from the merging beginning split at position 3
    is_mutcd = "yes"  # Manual on Uniform Traffic Control Devices - adopted in USA, but similar versions are in Canada, NZ and Australia
    count_of_forward_roled_series = 1  # this is a forward way series
    role_of_first_way = "north"
    currently_checked_ref = way_queries.get_way_ref(ways[index_of_current_way])
    previous_role = "north"
    current_role = way_queries.get_role(ways[index_of_current_way])
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    last_forward_way_before_backward_direction = [way_queries.get_way_ref(ways[index_of_current_way - 2]),
                                                  way_queries.get_end_node(ways[index_of_current_way - 2])]
    has_directional_roles = True
    error_information = []
    previous_current = PreviousCurrentHighway(currently_checked_ref=currently_checked_ref,
                                              last_forward_way_before_backward_direction=last_forward_way_before_backward_direction,
                                              first_node_previous=first_node_previous,
                                              first_node_current=first_node_current,
                                              last_node_previous=last_node_previous,
                                              last_node_current=last_node_current,
                                              previous_role=previous_role, current_role=current_role)
    # Act
    has_directional_roles, error_information = analyzer.check_if_there_is_gap_at_the_beginning(index_of_current_way,
                                                                                               count_of_forward_roled_series,
                                                                                               role_of_first_way,
                                                                                               is_mutcd, previous_role,
                                                                                               current_role,
                                                                                               first_node_previous,
                                                                                               last_node_previous,
                                                                                               first_node_current,
                                                                                               last_node_current,
                                                                                               last_forward_way_before_backward_direction,
                                                                                               has_directional_roles,
                                                                                               error_information,
                                                                                               previous_current)

    assertion = ErrorHighway(previous_current, "Gap at the beginning")
    assert type(error_information[0]) == ErrorHighway
    assert error_information[0].prev_curr == previous_current
    assert error_information[0].error_type == "Gap at the beginning"
    assert has_directional_roles is True


def test_check_if_there_is_no_gap_at_the_beginning():
    ways = analyzer_dicts.relation_info_no_gap_in_first_forward_series["ways_to_search"]
    index_of_current_way = 3  # let's suppose that the way is detached from the merging beginning split at position 3
    count_of_forward_roled_series = 1  # this is a forward way series
    role_of_first_way = way_queries.get_role(ways[0])
    is_mutcd = False
    currently_checked_ref = way_queries.get_way_ref(ways[index_of_current_way])
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    last_forward_way_before_backward_direction = [way_queries.get_way_ref(ways[index_of_current_way - 2]),
                                                  way_queries.get_end_node(ways[index_of_current_way - 2])]
    has_directional_roles = False  # hardcoded because I can't find a better way. let's suppose it doesn't have directional ways
    previous_current = PreviousCurrentHighway(currently_checked_ref=currently_checked_ref,
                                              last_forward_way_before_backward_direction=last_forward_way_before_backward_direction,
                                              first_node_previous=first_node_previous,
                                              first_node_current=first_node_current,
                                              last_node_previous=last_node_previous,
                                              last_node_current=last_node_current,
                                              previous_role=previous_role, current_role=current_role)
    error_information = []
    # Act
    has_directional_roles, error_information = analyzer.check_if_there_is_gap_at_the_beginning(index_of_current_way,
                                                                                               count_of_forward_roled_series,
                                                                                               role_of_first_way,
                                                                                               is_mutcd, previous_role,
                                                                                               current_role,
                                                                                               first_node_previous,
                                                                                               last_node_previous,
                                                                                               first_node_current,
                                                                                               last_node_current,
                                                                                               last_forward_way_before_backward_direction,
                                                                                               has_directional_roles,
                                                                                               error_information,
                                                                                               previous_current)

    assert len(error_information) == 0
    assert has_directional_roles is False


def test_check_if_mutcd_country_and_directional():
    has_directional_roles = False
    is_mutcd_usa = way_queries.determine_if_country_has_MUTCD_or_similar(way_queries_dicts.relation2)
    is_mutcd_hungary = way_queries.determine_if_country_has_MUTCD_or_similar(way_queries_dicts.relation)
    role_of_first_way, role_of_second_way = "north", "south"
    role_of_first_way_forward, role_of_second_way_forward = "forward", "forward"
    has_directional_roles_usa = analyzer.check_if_mutcd_country_and_directional(has_directional_roles, is_mutcd_usa,
                                                                                role_of_first_way, role_of_second_way)
    has_directional_roles_hungary = analyzer.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                    is_mutcd_hungary, role_of_first_way,
                                                                                    role_of_second_way)
    has_directional_roles_usa_no_cardinal = analyzer.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                            is_mutcd_usa,
                                                                                            role_of_first_way_forward,
                                                                                            role_of_second_way_forward)
    assert [has_directional_roles_usa, has_directional_roles_usa_no_cardinal, has_directional_roles_hungary] == [True,
                                                                                                                 False,
                                                                                                                 False]
