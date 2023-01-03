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
    current_nodes = way_queries.get_nodes(ways_to_search[0])
    roundabout_ways = []
    error_information = []
    prev_curr = PreviousCurrentHighway()
    nodes = way_queries.get_nodes(ways_to_search[0])
    # Act
    last_roundabout_nodes = []  # init
    last_roundabout_nodes, roundabout_ways, error_information = analyzer.is_way_roundabout(current_roundabout, current_role, current_nodes, roundabout_ways, nodes,
                                                       last_roundabout_nodes, error_information, prev_curr)
    current_nodes = way_queries.get_nodes(ways_to_search[1])
    current_role = way_queries.get_role(ways_to_search[1])
    last_roundabout_nodes_not_roundabout, roundabout_ways, error_information = analyzer.is_way_roundabout(not_roundabout, current_nodes, current_role, roundabout_ways, nodes,
                                                       last_roundabout_nodes, error_information, prev_curr)
    # Assert
    assert last_roundabout_nodes == ["-1", "-2"]
    assert last_roundabout_nodes_not_roundabout == ["-1", "-2"]
    assert len(error_information) == 0

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

    count_of_forward_roled_way_series = 0  # initially
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
            count_of_forward_roled_way_series] == ['-4', '-5', 1]


def test_is_the_way_in_forward_way_series_two_forward_ways():
    # Arrange
    ways = analyzer_dicts.relation_info_highway_forward[
        "ways_to_search"]
    # 4-5th way(forward and forward):
    role_of_the_4th_way = way_queries.get_role(ways[3])
    role_of_the_5th_way = way_queries.get_role(ways[4])
    first_node_fifth_way = way_queries.get_start_node(ways[4])
    last_node_fifth_way = way_queries.get_end_node(ways[4])

    first_node_of_first_forward_way_in_the_series = -4
    last_node_of_first_forward_way_in_the_series = -5
    count_of_forward_roled_way_series = 1  # the 4th way is forward.

    first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, \
    count_of_forward_roled_way_series = analyzer.is_the_way_in_forward_way_series(
        index_of_current_way=3,
        previous_role=role_of_the_4th_way, current_role=role_of_the_5th_way,
        count_of_forward_roled_way_series=count_of_forward_roled_way_series,
        first_node_current=first_node_fifth_way,
        last_node_current=last_node_fifth_way,
        first_node_of_first_forward_way_in_the_series=first_node_of_first_forward_way_in_the_series,
        last_node_of_first_forward_way_in_the_series=last_node_of_first_forward_way_in_the_series)
    assert count_of_forward_roled_way_series == 2


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
    previous_current = PreviousCurrentHighway()
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
    previous_current = PreviousCurrentHighway()
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
    route_number = way_queries.get_ref_of_the_route(ways)
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    last_forward_way_before_backward_direction = [way_queries.get_way_ref(ways[index_of_current_way - 2]),
                                                  way_queries.get_end_node(ways[index_of_current_way - 2])]
    has_directional_roles = False  # hardcoded because I can't find a better way. let's suppose it doesn't have directional ways
    previous_current = PreviousCurrentHighway()
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


def test_check_roundabout_gaps_only_one_forward_way():
    # Setup
    index_of_current_way = 2
    ways = analyzer_dicts.relation_info_roundabout_only_one_forward_roled["ways_to_search"]
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    error_information = []
    pieces_of_roundabout = 0
    count_of_forward_roled_way_series = 1  # manually set, otherwise there's a method which will be tested for this
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    previous_current = PreviousCurrentHighway()
    current_role = "forward"
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    # Act
    pieces_of_roundabout, error_information = analyzer.determine_roundabout_errors_and_number(index_of_current_way,
                                                                                              previous_roundabout,
                                                                                              current_roundabout,
                                                                                              current_role,
                                                                                              previous_current,
                                                                                              error_information,
                                                                                              pieces_of_roundabout,
                                                                                              count_of_forward_roled_way_series,
                                                                                              last_node_previous,
                                                                                              last_node_current,
                                                                                              first_node_current)
    # Assert
    assert pieces_of_roundabout == 1
    assert len(error_information) == 1
    assert error_information[0].error_type == "Only one forward way before closed roundabout"


def test_check_roundabout_gaps_when_previous_last_is_current_last():
    index_of_current_way = 2
    ways = analyzer_dicts.relation_info_roundabout_previous_last_is_current_last["ways_to_search"]
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    error_information = []
    pieces_of_roundabout = 0
    count_of_forward_roled_way_series = 2  # manually set, otherwise there's a method which will be tested for this
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    previous_current = PreviousCurrentHighway()
    current_role = "forward"
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    # Act
    pieces_of_roundabout, error_information = analyzer.determine_roundabout_errors_and_number(index_of_current_way,
                                                                                              previous_roundabout,
                                                                                              current_roundabout,
                                                                                              current_role,
                                                                                              previous_current,
                                                                                              error_information,
                                                                                              pieces_of_roundabout,
                                                                                              count_of_forward_roled_way_series,
                                                                                              last_node_previous,
                                                                                              last_node_current,
                                                                                              first_node_current)
    # Assert
    assert pieces_of_roundabout == 1
    assert len(error_information) == 1
    assert error_information[0].error_type == "Roundabout gap"


def test_check_roundabout_gaps_no_gaps_but_two_pieces_of_roundabout():
    index_of_current_way = 1
    ways = analyzer_dicts.relation_info_roundabout_two_roundabout_pieces["ways_to_search"]
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    error_information = []
    pieces_of_roundabout = 1
    count_of_forward_roled_way_series = -1  # we actually don't need this, since we only check it at the beginning
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    previous_current = PreviousCurrentHighway()
    current_role = "forward"
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    # Act
    pieces_of_roundabout, error_information = analyzer.determine_roundabout_errors_and_number(index_of_current_way,
                                                                                              previous_roundabout,
                                                                                              current_roundabout,
                                                                                              current_role,
                                                                                              previous_current,
                                                                                              error_information,
                                                                                              pieces_of_roundabout,
                                                                                              count_of_forward_roled_way_series,
                                                                                              last_node_previous,
                                                                                              last_node_current,
                                                                                              first_node_current)
    assert pieces_of_roundabout == 2
    assert len(error_information) == 0
    # now comes the case when we reach the end of roundabout:
    index_of_current_way = 2
    previous_roundabout = current_roundabout
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    current_role = "forward"
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    # Act
    pieces_of_roundabout, error_information = analyzer.determine_roundabout_errors_and_number(index_of_current_way,
                                                                                              previous_roundabout,
                                                                                              current_roundabout,
                                                                                              current_role,
                                                                                              previous_current,
                                                                                              error_information,
                                                                                              pieces_of_roundabout,
                                                                                              count_of_forward_roled_way_series,
                                                                                              last_node_previous,
                                                                                              last_node_current,
                                                                                              first_node_current)
    assert pieces_of_roundabout == 0
    assert len(error_information) == 0


def test_check_roundabout_gaps_continuous_no_roundabout_series():
    index_of_current_way = 1
    ways = analyzer_dicts.relation_info_continuous_series["ways_to_search"]
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    error_information = []
    pieces_of_roundabout = 0
    count_of_forward_roled_way_series = -1  # we actually don't need this, since we only check it at the beginning
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    previous_current = PreviousCurrentHighway()
    current_role = "forward"
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    # Act
    pieces_of_roundabout, error_information = analyzer.determine_roundabout_errors_and_number(index_of_current_way,
                                                                                              previous_roundabout,
                                                                                              current_roundabout,
                                                                                              current_role,
                                                                                              previous_current,
                                                                                              error_information,
                                                                                              pieces_of_roundabout,
                                                                                              count_of_forward_roled_way_series,
                                                                                              last_node_previous,
                                                                                              last_node_current,
                                                                                              first_node_current)
    # Assert
    assert pieces_of_roundabout == 0
    assert len(error_information) == 0


def test_check_role_issues_in_continuous_way_normal_way():
    # Arrange
    relation = analyzer_dicts.relation_info_continuous_series
    ways = relation["ways_to_search"]
    index_of_current_way = 1
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    has_directional_roles = False
    last_forward_way_before_backward_direction = error_information = []
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    previous_current = PreviousCurrentHighway()
    # Act
    has_directional_roles, error_information = analyzer.check_role_issues_in_continuous_way(index_of_current_way,
                                                                                            previous_role,
                                                                                            current_role,
                                                                                            previous_oneway,
                                                                                            current_oneway,
                                                                                            is_mutcd_country,
                                                                                            role_of_first_way,
                                                                                            has_directional_roles,
                                                                                            last_forward_way_before_backward_direction,
                                                                                            previous_nodes,
                                                                                            error_information,
                                                                                            previous_current)
    assert has_directional_roles is False
    assert current_role == ""
    assert current_oneway is False
    assert len(error_information) == 0


def test_check_role_issues_in_continuous_way_forward_in_a_non_forward_series():
    # Arrange
    relation = analyzer_dicts.relation_info_NNFN_pattern
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    has_directional_roles = False
    last_forward_way_before_backward_direction = error_information = []
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    previous_current = PreviousCurrentHighway()
    # Act
    has_directional_roles, error_information = analyzer.check_role_issues_in_continuous_way(index_of_current_way,
                                                                                            previous_role,
                                                                                            current_role,
                                                                                            previous_oneway,
                                                                                            current_oneway,
                                                                                            is_mutcd_country,
                                                                                            role_of_first_way,
                                                                                            has_directional_roles,
                                                                                            last_forward_way_before_backward_direction,
                                                                                            previous_nodes,
                                                                                            error_information,
                                                                                            previous_current)
    assert has_directional_roles is False
    assert current_role == ""
    assert previous_role == "forward"
    assert len(error_information) == 1
    assert error_information[0].error_type == "Forward and non-oneway without ability to move backward"


def test_check_role_issues_in_forward_way_no_gap_oneway_series():
    # Arrange
    relation_new = analyzer_dicts.relation_info_no_gap_in_first_forward_series
    ways = relation_new["ways_to_search"]
    index_of_current_way = 3
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation_new)
    role_of_first_way = way_queries.get_role(ways[0])
    has_directional_roles = False
    last_forward_way_before_backward_direction = error_information = []
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    previous_current = PreviousCurrentHighway()
    # Act
    has_directional_roles, error_information = analyzer.check_role_issues_in_continuous_way(index_of_current_way,
                                                                                            previous_role,
                                                                                            current_role,
                                                                                            previous_oneway,
                                                                                            current_oneway,
                                                                                            is_mutcd_country,
                                                                                            role_of_first_way,
                                                                                            has_directional_roles,
                                                                                            last_forward_way_before_backward_direction,
                                                                                            previous_nodes,
                                                                                            error_information,
                                                                                            previous_current)
    assert has_directional_roles is False
    assert current_role == ""
    assert previous_role == "forward"
    assert way_queries.get_role(ways[index_of_current_way - 2]) == "forward"
    assert len(error_information) == 0


def test_check_role_issues_in_forward_way_no_gap_oneway_series_no_oneway():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series_no_oneway
    ways = relation["ways_to_search"]
    index_of_current_way = 2
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    has_directional_roles = False
    last_forward_way_before_backward_direction = error_information = []
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    previous_current = PreviousCurrentHighway()
    # Act
    has_directional_roles, error_information = analyzer.check_role_issues_in_continuous_way(index_of_current_way,
                                                                                            previous_role,
                                                                                            current_role,
                                                                                            previous_oneway,
                                                                                            current_oneway,
                                                                                            is_mutcd_country,
                                                                                            role_of_first_way,
                                                                                            has_directional_roles,
                                                                                            last_forward_way_before_backward_direction,
                                                                                            previous_nodes,
                                                                                            error_information,
                                                                                            previous_current)
    assert current_role == "forward"
    assert previous_role == "forward"
    assert current_oneway is False
    assert len(error_information) == 0


def test_check_role_issues_in_wrong_role_setup():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series_no_oneway
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    current_role = way_queries.get_role(ways[index_of_current_way])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    has_directional_roles = False
    last_forward_way_before_backward_direction = error_information = []
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    previous_current = PreviousCurrentHighway()
    # Act
    has_directional_roles, error_information = analyzer.check_role_issues_in_continuous_way(index_of_current_way,
                                                                                            previous_role,
                                                                                            current_role,
                                                                                            previous_oneway,
                                                                                            current_oneway,
                                                                                            is_mutcd_country,
                                                                                            role_of_first_way,
                                                                                            has_directional_roles,
                                                                                            last_forward_way_before_backward_direction,
                                                                                            last_node_previous,
                                                                                            error_information,
                                                                                            previous_current)
    assert has_directional_roles is False
    assert current_role == ""
    assert previous_role == "forward"
    assert current_oneway is True
    assert len(error_information) == 1
    assert error_information[0].error_type == "Wrong role setup"


def test_check_the_situation_with_2_by_2_highways_check_if_its_correct():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_two_by_two_splitting_highway
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    has_directional_roles = False
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = way_queries.get_start_node(ways[1])
    last_node_of_first_forward_way_in_the_series = way_queries.get_end_node(ways[1])
    role_of_first_way = way_queries.get_role(ways[0])
    count_of_forward_roled_way_series = 1  # this is tested in another method
    last_forward_way_before_backward_direction = []
    current_highway = ""  # in this case, it's not that important. next test will have that
    route_number = ""  # similarly to the previous one, since this is the relation's "route number" eg. M35
    network = way_queries.get_network(relation)
    motorway_split_way = False
    error_information = []
    prev_curr = PreviousCurrentHighway()
    previous_ref = way_queries.get_way_ref(ways[index_of_current_way - 1])
    last_roundabout = []  # not important now
    current_nodes = []  # it's not important now
    # Act
    last_forward_way_before_backward_direction_from_method, motorway_split_way, has_directional_roles, error_information = analyzer.check_the_situation_with_2_by_2_highways(
        is_mutcd_country, has_directional_roles, first_node_current, last_node_current,
        first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
        role_of_first_way, count_of_forward_roled_way_series, last_forward_way_before_backward_direction,
        current_highway, route_number, network, motorway_split_way, error_information,
        prev_curr, previous_ref, last_roundabout, current_nodes, previous_nodes)
    assert last_forward_way_before_backward_direction_from_method == last_forward_way_before_backward_direction
    assert motorway_split_way is False
    assert has_directional_roles is False
    assert len(error_information) == 0


def test_check_the_situation_with_2_by_2_motorways_when_one_side_ends_one_side_starts():
    # Arrange
    relation = analyzer_dicts.relation_info_motorway
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    has_directional_roles = False
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = way_queries.get_start_node(ways[1])
    last_node_of_first_forward_way_in_the_series = way_queries.get_end_node(ways[1])
    role_of_first_way = way_queries.get_role(ways[0])
    count_of_forward_roled_way_series = 1  # this is tested in another method
    last_forward_way_before_backward_direction = []
    current_highway = way_queries.get_highway(ways[index_of_current_way])
    route_number = way_queries.get_ref_of_the_route(relation)
    network = way_queries.get_network(relation)
    motorway_split_way = False
    error_information = []
    prev_curr = PreviousCurrentHighway()
    previous_ref = way_queries.get_way_ref(ways[index_of_current_way - 1])
    last_roundabout = []  # not important now
    current_nodes = []  # it's not important now
    # Act
    last_forward_way_before_backward_direction_from_method, motorway_split_way, has_directional_roles, error_information = analyzer.check_the_situation_with_2_by_2_highways(
        is_mutcd_country, has_directional_roles, first_node_current, last_node_current,
        first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
        role_of_first_way, count_of_forward_roled_way_series, last_forward_way_before_backward_direction,
        current_highway, route_number, network, motorway_split_way, error_information,
        prev_curr, previous_ref, last_roundabout, current_nodes, previous_nodes)
    assert last_forward_way_before_backward_direction_from_method == [way_queries.get_way_ref(ways[2]),
                                                                      previous_nodes]
    assert current_highway == "motorway"
    assert network.startswith("HU")
    assert route_number.startswith("M")
    assert motorway_split_way is True
    assert has_directional_roles is False
    assert len(error_information) == 0


def test_check_the_situation_with_2_by_2_ways_when_it_starts_from_a_complete_roundabout_no_gap():
    # Arrange
    relation = analyzer_dicts.relation_info_one_piece_roundabout_to_split_ways
    ways = relation["ways_to_search"]
    index_of_current_way = 4
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    has_directional_roles = False
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = way_queries.get_start_node(ways[1])
    last_node_of_first_forward_way_in_the_series = way_queries.get_end_node(ways[1])
    role_of_first_way = way_queries.get_role(ways[0])
    count_of_forward_roled_way_series = 1  # this is tested in another method
    last_forward_way_before_backward_direction = []
    current_highway = way_queries.get_highway(ways[index_of_current_way])
    route_number = way_queries.get_ref_of_the_route(relation)
    network = way_queries.get_network(relation)
    motorway_split_way = False
    error_information = []
    prev_curr = PreviousCurrentHighway()
    previous_ref = way_queries.get_way_ref(ways[index_of_current_way - 1])
    last_roundabout_nodes = way_queries.get_nodes(ways[1])
    current_nodes = way_queries.get_nodes(ways[index_of_current_way])
    # Act
    last_forward_way_before_backward_direction_from_method, motorway_split_way, has_directional_roles, error_information = analyzer.check_the_situation_with_2_by_2_highways(
        is_mutcd_country, has_directional_roles, first_node_current, last_node_current,
        first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
        role_of_first_way, count_of_forward_roled_way_series, last_forward_way_before_backward_direction,
        current_highway, route_number, network, motorway_split_way, error_information,
        prev_curr, previous_ref, last_roundabout_nodes, current_nodes, previous_nodes)
    assert last_forward_way_before_backward_direction_from_method == [
        way_queries.get_way_ref(ways[index_of_current_way - 1]),
        previous_nodes]
    assert motorway_split_way is False
    assert has_directional_roles is False
    assert len(error_information) == 0


def test_check_the_situation_with_2_by_2_ways_when_it_starts_from_a_complete_roundabout_gap():
    # Arrange
    relation = analyzer_dicts.relation_info_one_piece_roundabout_to_split_ways_gap
    ways = relation["ways_to_search"]
    index_of_current_way = 4
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    has_directional_roles = False
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = way_queries.get_start_node(ways[1])
    last_node_of_first_forward_way_in_the_series = way_queries.get_end_node(ways[1])
    role_of_first_way = way_queries.get_role(ways[0])
    count_of_forward_roled_way_series = 1  # this is tested in another method
    last_forward_way_before_backward_direction = []
    current_highway = way_queries.get_highway(ways[index_of_current_way])
    route_number = way_queries.get_ref_of_the_route(relation)
    network = way_queries.get_network(relation)
    motorway_split_way = False
    error_information = []
    prev_curr = PreviousCurrentHighway()
    previous_ref = way_queries.get_way_ref(ways[index_of_current_way - 1])
    last_roundabout_nodes = way_queries.get_nodes(ways[1])
    current_nodes = way_queries.get_nodes(ways[index_of_current_way])
    # Act
    last_forward_way_before_backward_direction_from_method, motorway_split_way, has_directional_roles, error_information = analyzer.check_the_situation_with_2_by_2_highways(
        is_mutcd_country, has_directional_roles, first_node_current, last_node_current,
        first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
        role_of_first_way, count_of_forward_roled_way_series, last_forward_way_before_backward_direction,
        current_highway, route_number, network, motorway_split_way, error_information,
        prev_curr, previous_ref, last_roundabout_nodes, current_nodes, previous_nodes)
    assert last_forward_way_before_backward_direction_from_method == [
        way_queries.get_way_ref(ways[index_of_current_way - 1]),
        previous_nodes]
    assert motorway_split_way is False
    assert has_directional_roles is False
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in forward series"


def test_check_if_motorway_not_split():
    # Assert
    relation = analyzer_dicts.relation_info_motorway_not_split
    ways = relation["ways_to_search"]
    motorway_split_way = False
    index_of_current_way = len(ways) - 1
    length_of_ways_to_search = len(ways)
    current_highway = way_queries.get_highway(ways[index_of_current_way])
    route_number = way_queries.get_ref_of_the_route(relation)
    network = way_queries.get_network(relation)
    current_role = way_queries.get_role(ways[index_of_current_way])
    error_information = []
    previous_current = PreviousCurrentHighway()
    # Act
    error_information = analyzer.check_if_motorway_not_split(motorway_split_way, index_of_current_way,
                                                             length_of_ways_to_search, current_highway, route_number,
                                                             network, current_role, error_information, previous_current)
    assert motorway_split_way is False
    assert index_of_current_way == length_of_ways_to_search - 1
    assert current_highway == "motorway"
    assert len(error_information) == 1
    assert error_information[0].error_type == "Motorway not split"


def test_check_if_way_connects_continuously():
    # Just throw in the parameters one of the tests - in the case of 2x2 highways.
    relation = analyzer_dicts.relation_info_one_piece_roundabout_to_split_ways_gap
    ways = relation["ways_to_search"]
    index_of_current_way = 4
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    has_directional_roles = False
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = way_queries.get_start_node(ways[1])
    last_node_of_first_forward_way_in_the_series = way_queries.get_end_node(ways[1])
    role_of_first_way = way_queries.get_role(ways[0])
    count_of_forward_roled_way_series = 1  # this is tested in another method
    last_forward_way_before_backward_direction = []
    current_highway = way_queries.get_highway(ways[index_of_current_way])
    route_number = way_queries.get_ref_of_the_route(relation)
    network = way_queries.get_network(relation)
    motorway_split_way = False
    error_information = []
    prev_curr = PreviousCurrentHighway()
    previous_ref = way_queries.get_way_ref(ways[index_of_current_way - 1])
    last_roundabout_nodes = way_queries.get_nodes(ways[1])
    current_nodes = way_queries.get_nodes(ways[index_of_current_way])
    previous_nodes = way_queries.get_nodes(ways[index_of_current_way - 1])
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    first_node_previous = current_role = previous_oneway = current_oneway = previous_roundabout = current_roundabout = ""  # not needed now
    # Act
    last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, \
    error_information = analyzer.check_if_way_connects_continuously(ways, previous_nodes, current_nodes,
                                                                    index_of_current_way, first_node_previous,
                                                                    last_node_previous, first_node_current,
                                                                    last_node_current, previous_role, current_role,
                                                                    previous_oneway,
                                                                    previous_roundabout, current_roundabout,
                                                                    current_oneway, is_mutcd_country,
                                                                    role_of_first_way,
                                                                    has_directional_roles,
                                                                    error_information, prev_curr,
                                                                    first_node_of_first_forward_way_in_the_series,
                                                                    last_node_of_first_forward_way_in_the_series,
                                                                    motorway_split_way,
                                                                    count_of_forward_roled_way_series,
                                                                    last_forward_way_before_backward_direction,
                                                                    current_highway, route_number, network,
                                                                    previous_ref, last_roundabout_nodes)

    assert motorway_split_way is False
    assert has_directional_roles is False
    assert previous_role == "forward"
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in forward series"
    assert last_forward_way_before_backward_direction == [
        way_queries.get_way_ref(ways[index_of_current_way - 1]),
        previous_nodes]


# Continue with other tests from the same method!

def test_check_if_way_connects_continuously_checking_role_issues_wrong_role():
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series_no_oneway
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    count_of_forward_roled_way_series = 0
    previous_nodes = current_nodes = last_forward_way_before_backward_direction = last_roundabout_nodes = []
    previous_roundabout = current_roundabout = motorway_split_way = has_directional_roles = False
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    error_information = []
    previous_current = PreviousCurrentHighway()
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = last_node_of_first_forward_way_in_the_series = \
        current_highway = route_number = network = previous_ref = ""
    current_role = way_queries.get_role(ways[index_of_current_way])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    # Act
    last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, \
    error_information = analyzer.check_if_way_connects_continuously(ways, previous_nodes, current_nodes,
                                                                    index_of_current_way, first_node_previous,
                                                                    last_node_previous, first_node_current,
                                                                    last_node_current, previous_role, current_role,
                                                                    previous_oneway,
                                                                    previous_roundabout, current_roundabout,
                                                                    current_oneway, is_mutcd_country,
                                                                    role_of_first_way,
                                                                    has_directional_roles,
                                                                    error_information, previous_current,
                                                                    first_node_of_first_forward_way_in_the_series,
                                                                    last_node_of_first_forward_way_in_the_series,
                                                                    motorway_split_way,
                                                                    count_of_forward_roled_way_series,
                                                                    last_forward_way_before_backward_direction,
                                                                    current_highway, route_number, network,
                                                                    previous_ref, last_roundabout_nodes)
    assert has_directional_roles is False
    assert current_role == ""
    assert previous_role == "forward"
    assert current_oneway is True
    assert index_of_current_way > 0
    assert index_of_current_way > 0 and (
            first_node_previous == first_node_current or first_node_previous == last_node_current
            or last_node_previous == first_node_current or last_node_previous == last_node_current)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Wrong role setup"


def test_check_if_way_connects_continuously_relation_info_one_piece_roundabout_gap():
    relation = analyzer_dicts.relation_info_one_piece_roundabout_gap
    ways = relation["ways_to_search"]
    index_of_current_way = 2
    count_of_forward_roled_way_series = 0
    previous_nodes = current_nodes = last_forward_way_before_backward_direction = last_roundabout_nodes = []
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    motorway_split_way = has_directional_roles = False
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    error_information = []
    previous_current = PreviousCurrentHighway()
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = last_node_of_first_forward_way_in_the_series = \
        current_highway = route_number = network = previous_ref = ""
    current_role = way_queries.get_role(ways[index_of_current_way])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    # Act
    last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, \
    error_information = analyzer.check_if_way_connects_continuously(ways, previous_nodes, current_nodes,
                                                                    index_of_current_way, first_node_previous,
                                                                    last_node_previous, first_node_current,
                                                                    last_node_current, previous_role, current_role,
                                                                    previous_oneway,
                                                                    previous_roundabout, current_roundabout,
                                                                    current_oneway, is_mutcd_country,
                                                                    role_of_first_way,
                                                                    has_directional_roles,
                                                                    error_information, previous_current,
                                                                    first_node_of_first_forward_way_in_the_series,
                                                                    last_node_of_first_forward_way_in_the_series,
                                                                    motorway_split_way,
                                                                    count_of_forward_roled_way_series,
                                                                    last_forward_way_before_backward_direction,
                                                                    current_highway, route_number, network,
                                                                    previous_ref, last_roundabout_nodes)
    assert has_directional_roles is False
    assert current_roundabout is False
    assert previous_roundabout is True
    assert index_of_current_way > 0
    assert len(error_information) == 1
    assert error_information[0].error_type == "Roundabout gap"


def test_check_if_way_connects_continuously_relation_info_gap():
    relation = analyzer_dicts.relation_info_one_piece_roundabout_gap
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    count_of_forward_roled_way_series = 0
    previous_nodes = current_nodes = last_forward_way_before_backward_direction = last_roundabout_nodes = []
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    motorway_split_way = has_directional_roles = False
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    error_information = []
    previous_current = PreviousCurrentHighway()
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = last_node_of_first_forward_way_in_the_series = \
        current_highway = route_number = network = previous_ref = ""
    current_role = way_queries.get_role(ways[index_of_current_way])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    # Act
    last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, \
    error_information = analyzer.check_if_way_connects_continuously(ways, previous_nodes, current_nodes,
                                                                    index_of_current_way, first_node_previous,
                                                                    last_node_previous, first_node_current,
                                                                    last_node_current, previous_role, current_role,
                                                                    previous_oneway,
                                                                    previous_roundabout, current_roundabout,
                                                                    current_oneway, is_mutcd_country,
                                                                    role_of_first_way,
                                                                    has_directional_roles,
                                                                    error_information, previous_current,
                                                                    first_node_of_first_forward_way_in_the_series,
                                                                    last_node_of_first_forward_way_in_the_series,
                                                                    motorway_split_way,
                                                                    count_of_forward_roled_way_series,
                                                                    last_forward_way_before_backward_direction,
                                                                    current_highway, route_number, network,
                                                                    previous_ref, last_roundabout_nodes)
    assert has_directional_roles is False
    assert current_roundabout is False
    assert previous_roundabout is False
    assert index_of_current_way > 0
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap"


def test_check_if_way_connects_continuously_relation_info_no_gap():
    relation = analyzer_dicts.relation_info_one_piece_roundabout_gap
    ways = relation["ways_to_search"]
    index_of_current_way = 4
    count_of_forward_roled_way_series = 0
    previous_nodes = current_nodes = last_forward_way_before_backward_direction = last_roundabout_nodes = []
    previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    motorway_split_way = has_directional_roles = False
    previous_role = way_queries.get_role(ways[index_of_current_way - 1])
    previous_oneway = way_queries.is_oneway(ways[index_of_current_way - 1])
    is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation)
    role_of_first_way = way_queries.get_role(ways[0])
    error_information = []
    previous_current = PreviousCurrentHighway()
    first_node_previous = way_queries.get_start_node(ways[index_of_current_way - 1])
    last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    first_node_of_first_forward_way_in_the_series = last_node_of_first_forward_way_in_the_series = \
        current_highway = route_number = network = previous_ref = ""
    current_role = way_queries.get_role(ways[index_of_current_way])
    current_oneway = way_queries.is_oneway(ways[index_of_current_way])
    # Act
    last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, \
    error_information = analyzer.check_if_way_connects_continuously(ways, previous_nodes, current_nodes,
                                                                    index_of_current_way, first_node_previous,
                                                                    last_node_previous, first_node_current,
                                                                    last_node_current, previous_role, current_role,
                                                                    previous_oneway,
                                                                    previous_roundabout, current_roundabout,
                                                                    current_oneway, is_mutcd_country,
                                                                    role_of_first_way,
                                                                    has_directional_roles,
                                                                    error_information, previous_current,
                                                                    first_node_of_first_forward_way_in_the_series,
                                                                    last_node_of_first_forward_way_in_the_series,
                                                                    motorway_split_way,
                                                                    count_of_forward_roled_way_series,
                                                                    last_forward_way_before_backward_direction,
                                                                    current_highway, route_number, network,
                                                                    previous_ref, last_roundabout_nodes)
    assert has_directional_roles is False
    assert current_roundabout is False
    assert previous_roundabout is False
    assert index_of_current_way > 0
    assert len(error_information) == 0
