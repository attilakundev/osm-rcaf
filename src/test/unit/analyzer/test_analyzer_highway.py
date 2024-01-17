#!/usr/bin/python3
from src.lib.analyzer.highway_analyzer import HighwayAnalyzer
from src.test.files import analyzer_dicts
from src.test.files import way_queries_dicts
from src.lib import way_queries
from src.lib.model.previous_current import PreviousCurrentHighway
from src.lib.model.error_hwy import ErrorHighway

highway_analyzer = HighwayAnalyzer()


def test_is_role_backward():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_backward_role["ways_to_search"]
    current_nodes_before_reverse = way_queries.get_nodes(ways_to_search[0])
    prev_curr = PreviousCurrentHighway(
        first_node_current=way_queries.get_start_node(ways_to_search[0]),
        last_node_current=way_queries.get_end_node(ways_to_search[0]),
        current_role=way_queries.get_role(ways_to_search[0]),
        current_nodes=current_nodes_before_reverse)
    # Act
    highway_analyzer.is_role_backward(prev_curr)
    # Assert
    assert [prev_curr.first_node_current, prev_curr.last_node_current, prev_curr.current_role] == [
        "-4", "-1",
        "forward"]
    assert prev_curr.current_nodes == ["-4", "-3", "-2", "-1"]
    assert current_nodes_before_reverse == ["-1", "-2", "-3", "-4"]


def test_is_role_not_backward():
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_backward_role["ways_to_search"]
    prev_curr = PreviousCurrentHighway(
        first_node_current=way_queries.get_start_node(ways_to_search[0]),
        last_node_current=way_queries.get_end_node(ways_to_search[0]),
        current_role="forward",
        current_nodes=way_queries.get_nodes(ways_to_search[0]))
    # Act
    highway_analyzer.is_role_backward(prev_curr)
    # Assert
    assert [prev_curr.first_node_current, prev_curr.last_node_current, prev_curr.current_role] == [
        "-1", "-4",
        "forward"]
    assert prev_curr.current_nodes == ["-1", "-2", "-3", "-4"]


def test_is_way_roundabout():
    # Arrange
    error_information = []
    ways_to_search = analyzer_dicts.relation_info_highway_to_test_if_roundabout["ways_to_search"]
    prev_curr = PreviousCurrentHighway(
        current_roundabout=way_queries.is_roundabout(ways_to_search[0]),
        last_node_current=way_queries.get_end_node(ways_to_search[0]),
        current_role=way_queries.get_role(ways_to_search[0]),
        current_nodes=way_queries.get_nodes(ways_to_search[0]),
        current_ref=way_queries.get_way_ref(ways_to_search[0]))
    # Act
    highway_analyzer.is_way_roundabout(prev_curr, error_information)
    assert prev_curr.last_roundabout_nodes == ["-1", "-2"]
    prev_curr.current_nodes = way_queries.get_nodes(ways_to_search[1])
    prev_curr.current_role = way_queries.get_role(ways_to_search[1])
    prev_curr.current_roundabout = way_queries.is_roundabout(ways_to_search[1])
    highway_analyzer.is_way_roundabout(prev_curr, error_information)
    assert prev_curr.last_roundabout_nodes == ["-1", "-2"]
    # Assert
    assert len(error_information) == 0


def test_is_the_way_in_forward_way_series_beginning_way_is_forward():
    # Arrange
    ways_to_search = analyzer_dicts.relation_info_highway_forward[
        "ways_to_search"]
    prev_curr = PreviousCurrentHighway(
        first_node_current=way_queries.get_start_node(ways_to_search[0]),
        last_node_current=way_queries.get_end_node(ways_to_search[0]),
        current_role=way_queries.get_role(ways_to_search[0]),
        first_node_of_first_forward_way_in_the_series="0",
        last_node_of_first_forward_way_in_the_series="0",
        count_of_forward_role_way_series=0)

    is_the_way_in_forward_way_series_1st_way_forward(prev_curr)
    is_the_way_in_forward_way_series_3rd_4th_ways(prev_curr, ways_to_search)


def is_the_way_in_forward_way_series_1st_way_forward(prev_curr):
    # Act
    # First condition: we check it for the beginning
    highway_analyzer.is_the_way_in_forward_way_series(prev_curr)
    assert [prev_curr.first_node_of_first_forward_way_in_the_series,
            prev_curr.last_node_of_first_forward_way_in_the_series,
            prev_curr.count_of_forward_role_way_series] == ['-1', '-2', 1]


def is_the_way_in_forward_way_series_3rd_4th_ways(prev_curr, ways_to_search):
    # 3-4th way(non-forward and forward):
    prev_curr.count_of_forward_role_way_series = 0
    prev_curr.previous_role = way_queries.get_role(ways_to_search[2])
    prev_curr.current_role = way_queries.get_role(ways_to_search[3])
    prev_curr.first_node_current = way_queries.get_start_node(ways_to_search[3])
    prev_curr.last_node_current = way_queries.get_end_node(ways_to_search[3])
    prev_curr.index_of_current_way = 3
    highway_analyzer.is_the_way_in_forward_way_series(prev_curr)
    assert [prev_curr.first_node_of_first_forward_way_in_the_series,
            prev_curr.last_node_of_first_forward_way_in_the_series,
            prev_curr.count_of_forward_role_way_series] == ['-4', '-5', 1]


def test_is_the_way_in_forward_way_series_two_forward_ways():
    # Arrange
    ways = analyzer_dicts.relation_info_highway_forward[
        "ways_to_search"]
    # 4-5th way(forward and forward):
    prev_curr = PreviousCurrentHighway(first_node_current=way_queries.get_start_node(ways[4]),
                                       last_node_current=way_queries.get_end_node(ways[4]),
                                       previous_role=way_queries.get_role(ways[3]),
                                       current_role=way_queries.get_role(ways[4]),
                                       first_node_of_first_forward_way_in_the_series="-4",
                                       last_node_of_first_forward_way_in_the_series="-5",
                                       count_of_forward_role_way_series=1)
    # Act
    highway_analyzer.is_the_way_in_forward_way_series(prev_curr)
    # Assert
    assert prev_curr.count_of_forward_role_way_series == 2


def test_is_the_way_in_forward_way_series_not_forward():
    # chose an arbritrary existing array which has no forward ways.
    ways = analyzer_dicts.relation_info_highway_to_test_if_roundabout["ways_to_search"]
    prev_curr = PreviousCurrentHighway(first_node_current=way_queries.get_start_node(ways[1]),
                                       last_node_current=way_queries.get_end_node(ways[1]),
                                       previous_role=way_queries.get_role(ways[0]),
                                       current_role=way_queries.get_role(ways[1]),
                                       first_node_of_first_forward_way_in_the_series='-1',
                                       last_node_of_first_forward_way_in_the_series='-1',
                                       count_of_forward_role_way_series=0,
                                       index_of_current_way=3)
    highway_analyzer.is_the_way_in_forward_way_series(prev_curr)
    assert [prev_curr.first_node_of_first_forward_way_in_the_series,
            prev_curr.last_node_of_first_forward_way_in_the_series,
            prev_curr.count_of_forward_role_way_series] == ['-1', '-1', 0]


def test_check_if_there_is_gap_at_the_beginning():
    # Arrange
    ways = analyzer_dicts.relation_info_gap_in_first_forward_series["ways_to_search"]
    index_of_current_way = 3
    error_information = []
    last_forward_way_ref_nodes_before_backward = [
        way_queries.get_way_ref(ways[index_of_current_way - 2]),
        way_queries.get_end_node(ways[index_of_current_way - 2])]
    prev_curr = \
        PreviousCurrentHighway(first_node_previous=way_queries.
                               get_start_node(ways[index_of_current_way - 1]),
                               last_node_previous=way_queries.
                               get_end_node(ways[index_of_current_way - 1]),
                               first_node_current=way_queries.
                               get_start_node(ways[index_of_current_way]),
                               last_node_current=way_queries.
                               get_end_node(ways[index_of_current_way]),
                               previous_role=way_queries.get_role(ways[index_of_current_way - 1]),
                               current_role=way_queries.get_role(ways[index_of_current_way]),
                               first_node_of_first_forward_way_in_the_series='-1',
                               last_node_of_first_forward_way_in_the_series='-1',
                               count_of_forward_role_way_series=1,
                               index_of_current_way=index_of_current_way,
                               role_of_first_way=way_queries.get_role(ways[0]),
                               currently_checked_ref=way_queries.
                               get_way_ref(ways[index_of_current_way]),
                               last_forward_way_ref_nodes_before_backward=
                               last_forward_way_ref_nodes_before_backward)

    # Act
    highway_analyzer.check_if_there_is_gap_at_the_beginning(prev_curr, error_information)
    # Assert
    assert type(error_information[0]) == ErrorHighway
    assert error_information[0].error_type == "Gap at the beginning"
    assert prev_curr.has_directional_roles is False


def test_check_if_there_is_gap_at_the_beginning_usa():
    index_of_current_way = 3
    ways = analyzer_dicts.relation_info_gap_in_first_forward_series["ways_to_search"]
    error_information = []
    last_forward_way_ref_nodes_before_backward = [
        way_queries.get_way_ref(ways[index_of_current_way - 2]),
        way_queries.get_end_node(ways[index_of_current_way - 2])]
    prev_curr = PreviousCurrentHighway(
        first_node_previous=way_queries.get_start_node(ways[index_of_current_way - 1]),
        last_node_previous=way_queries.get_end_node(ways[index_of_current_way - 1]),
        first_node_current=way_queries.get_start_node(ways[index_of_current_way]),
        last_node_current=way_queries.get_end_node(ways[index_of_current_way]),
        previous_role="north",
        role_of_first_way="north",
        current_role=way_queries.get_role(ways[index_of_current_way]),
        first_node_of_first_forward_way_in_the_series='-1',
        last_node_of_first_forward_way_in_the_series='-1',
        count_of_forward_role_way_series=1,
        index_of_current_way=index_of_current_way,
        is_mutcd_country=True,
        has_directional_roles=False,
        currently_checked_ref=way_queries.get_way_ref(ways[index_of_current_way]),
        last_forward_way_ref_nodes_before_backward=last_forward_way_ref_nodes_before_backward)

    # Act
    highway_analyzer.check_if_there_is_gap_at_the_beginning(prev_curr, error_information)

    assert type(error_information[0]) == ErrorHighway
    assert error_information[0].prev_curr == prev_curr
    assert error_information[0].error_type == "Gap at the beginning"
    assert prev_curr.has_directional_roles is True


def test_check_if_there_is_no_gap_at_the_beginning():
    index_of_current_way = 3
    ways = analyzer_dicts.relation_info_no_gap_in_first_forward_series["ways_to_search"]
    error_information = []
    last_forward_way_ref_nodes_before_backward = [
        way_queries.get_way_ref(ways[index_of_current_way - 2]),
        way_queries.get_end_node(ways[index_of_current_way - 2])]
    prev_curr = PreviousCurrentHighway(count_of_forward_role_way_series=1,
                                       first_node_previous=way_queries.get_start_node(
                                           ways[index_of_current_way - 1]),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[index_of_current_way - 1]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[index_of_current_way]),
                                       previous_role=way_queries.get_role(
                                           ways[index_of_current_way - 1]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       current_role=way_queries.get_role(
                                           ways[index_of_current_way]),
                                       index_of_current_way=index_of_current_way,
                                       is_mutcd_country=False,
                                       currently_checked_ref=way_queries.get_way_ref(
                                           ways[index_of_current_way]),
                                       last_forward_way_ref_nodes_before_backward=
                                       last_forward_way_ref_nodes_before_backward)
    # Act
    highway_analyzer.check_if_there_is_gap_at_the_beginning(prev_curr, error_information)
    assert len(error_information) == 0
    assert prev_curr.has_directional_roles is False


def test_check_if_mutcd_country_and_directional():
    is_mutcd_usa = way_queries.determine_if_country_has_MUTCD_or_similar(
        way_queries_dicts.relation2)
    is_mutcd_hungary = way_queries.determine_if_country_has_MUTCD_or_similar(
        way_queries_dicts.relation)
    prev_curr = PreviousCurrentHighway(is_mutcd_country=is_mutcd_usa,
                                       role_of_first_way="south",
                                       previous_role="south",
                                       current_role="south")
    mutcd_country_having_directional_roles(prev_curr)
    __are_hungarian_roads_directional__(is_mutcd_hungary, prev_curr)
    mutcd_country_having_no_directional_roles(prev_curr)


def mutcd_country_having_directional_roles(prev_curr):
    highway_analyzer.check_if_mutcd_country_and_directional(prev_curr)
    assert prev_curr.has_directional_roles is True


def mutcd_country_having_no_directional_roles(prev_curr):
    prev_curr.has_directional_roles = True
    prev_curr.previous_role = prev_curr.current_role = prev_curr.role_of_first_way = "forward"
    highway_analyzer.check_if_mutcd_country_and_directional(prev_curr)
    assert prev_curr.has_directional_roles is True


def __are_hungarian_roads_directional__(is_mutcd_hungary, prev_curr):
    prev_curr.has_directional_roles = False
    prev_curr.is_mutcd_country = is_mutcd_hungary
    highway_analyzer.check_if_mutcd_country_and_directional(prev_curr)
    assert prev_curr.has_directional_roles is False


def test_check_roundabout_gaps_only_one_forward_way():
    # Setup
    index_of_current_way = 2
    error_information = []
    ways = analyzer_dicts.relation_info_roundabout_only_one_forward_role["ways_to_search"]
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way]),
                                       count_of_forward_role_way_series=1,
                                       last_node_previous=way_queries.get_end_node(
                                           ways[index_of_current_way - 1]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[index_of_current_way]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       current_role="forward")
    # Act
    prev_curr, error_information = highway_analyzer.check_roundabout_errors(
        prev_curr, error_information,ways,index_of_current_way)
    # Assert
    assert len(error_information) == 1
    assert error_information[0].error_type == "Only one forward way before closed roundabout"


def test_check_roundabout_gaps_when_previous_last_is_current_last():
    index_of_current_way = 2
    error_information = []
    ways = analyzer_dicts.relation_info_roundabout_previous_last_is_current_last["ways_to_search"]
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way]),
                                       count_of_forward_role_way_series=2,
                                       last_node_previous=way_queries.get_end_node(
                                           ways[index_of_current_way - 1]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[index_of_current_way]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       current_role="forward")

    # Act
    prev_curr, error_information = highway_analyzer.check_roundabout_errors(
        prev_curr, error_information,ways,index_of_current_way)
    # Assert
    assert len(error_information) == 1
    assert error_information[0].error_type == "Roundabout gap"


def test_check_roundabout_no_gaps():
    index_of_current_way = 1
    error_information = []
    ways = analyzer_dicts.relation_info_roundabout_two_roundabout_pieces["ways_to_search"]
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way]),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[index_of_current_way - 1]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[index_of_current_way]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       current_role="forward")
    # Act
    error_information, prev_curr = check_roundabout_no_gaps_at_the_beginning(error_information,
                                                                             prev_curr,ways,index_of_current_way)
    check_roundabout_no_gaps_at_the_end_of_roundabout(error_information, prev_curr, ways)


def check_roundabout_no_gaps_at_the_beginning(error_information, prev_curr,ways_to_search, index):
    prev_curr, error_information = highway_analyzer.check_roundabout_errors(
        prev_curr, error_information,ways_to_search,index)
    assert len(error_information) == 0
    return error_information, prev_curr


def check_roundabout_no_gaps_at_the_end_of_roundabout(error_information, prev_curr, ways):
    index_of_current_way = 2
    prev_curr.previous_roundabout = way_queries.is_roundabout(ways[index_of_current_way - 1])
    prev_curr.current_roundabout = way_queries.is_roundabout(ways[index_of_current_way])
    prev_curr.last_node_previous = way_queries.get_end_node(ways[index_of_current_way - 1])
    prev_curr.last_node_current = way_queries.get_end_node(ways[index_of_current_way])
    prev_curr.current_role = "forward"
    prev_curr.first_node_current = way_queries.get_start_node(ways[index_of_current_way])
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_roundabout_errors(prev_curr, error_information,ways,index_of_current_way)
    assert prev_curr.pieces_of_roundabout == 0
    assert len(error_information) == 0


def test_check_roundabout_gaps_continuous_no_roundabout_series():
    index_of_current_way = 1
    error_information = []
    ways = analyzer_dicts.relation_info_continuous_series["ways_to_search"]
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[index_of_current_way]),
                                       pieces_of_roundabout=0,
                                       last_node_previous=way_queries.get_end_node(
                                           ways[index_of_current_way - 1]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[index_of_current_way]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       current_role="forward")
    # Act
    prev_curr, error_information = highway_analyzer.check_roundabout_errors(
        prev_curr, error_information,ways,index_of_current_way)
    # Assert
    assert prev_curr.pieces_of_roundabout == 0
    assert len(error_information) == 0


def test_check_role_issues_in_continuous_way_normal_way():
    # Arrange
    relation = analyzer_dicts.relation_info_continuous_series
    ways = relation["ways_to_search"]
    index_of_current_way = 1
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_highway=way_queries.get_highway(
                                           ways[index_of_current_way - 1]),
                                       previous_role=way_queries.get_role(
                                           ways[index_of_current_way - 1]),
                                       current_role=way_queries.get_role(
                                           ways[index_of_current_way]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[index_of_current_way - 1]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[index_of_current_way - 1]),
                                       count_of_forward_role_way_series=2)

    # Act
    prev_curr, error_information = highway_analyzer. \
        check_role_issues_in_continuous_way(prev_curr,
                                            error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_role == ""
    assert prev_curr.current_oneway is False
    assert len(error_information) == 0


def test_check_role_issues_in_continuous_way_forward_in_a_non_forward_series():
    # Arrange
    relation = analyzer_dicts.relation_info_NNFN_pattern
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_highway=way_queries.get_highway(
                                           ways[index_of_current_way - 1]),
                                       previous_role=way_queries.get_role(
                                           ways[index_of_current_way - 1]),
                                       current_role=way_queries.get_role(
                                           ways[index_of_current_way]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[index_of_current_way - 1]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[index_of_current_way - 1]),
                                       count_of_forward_role_way_series=2)
    # Act
    prev_curr, error_information = highway_analyzer. \
        check_role_issues_in_continuous_way(prev_curr,
                                            error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_role == ""
    assert prev_curr.previous_role == "forward"
    assert prev_curr.previous_highway == "motorway"
    assert len(error_information) == 1
    assert error_information[
               0].error_type == "Forward and non-oneway without ability to move backward"


def test_check_role_issues_in_forward_way_no_gap_oneway_series():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_highway=way_queries.get_highway(
                                           ways[index_of_current_way - 1]),
                                       previous_role=way_queries.get_role(
                                           ways[index_of_current_way - 1]),
                                       current_role=way_queries.get_role(
                                           ways[index_of_current_way]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[index_of_current_way - 1]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[index_of_current_way - 1]),
                                       count_of_forward_role_way_series=2)
    # Act
    prev_curr, error_information = highway_analyzer. \
        check_role_issues_in_continuous_way(prev_curr,
                                            error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_role == ""
    assert prev_curr.previous_role == "forward"
    assert way_queries.get_role(ways[index_of_current_way - 2]) == "forward"
    assert len(error_information) == 0


def test_check_role_issues_in_forward_way_no_gap_oneway_series_no_oneway():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series_no_oneway
    ways = relation["ways_to_search"]
    index_of_current_way = 2
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_highway=way_queries.get_highway(
                                           ways[index_of_current_way - 1]),
                                       previous_role=way_queries.get_role(
                                           ways[index_of_current_way - 1]),
                                       current_role=way_queries.get_role(
                                           ways[index_of_current_way]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[index_of_current_way - 1]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[index_of_current_way - 1]),
                                       count_of_forward_role_way_series=2)
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_role_issues_in_continuous_way(prev_curr,
                                                             error_information)
    assert prev_curr.current_role == "forward"
    assert prev_curr.previous_role == "forward"
    assert prev_curr.current_oneway is False
    assert len(error_information) == 0


def test_check_role_issues_in_wrong_role_setup():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series_no_oneway
    ways = relation["ways_to_search"]
    index_of_current_way = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=index_of_current_way,
                                       previous_highway=way_queries.get_highway(
                                           ways[index_of_current_way - 1]),
                                       previous_role=way_queries.get_role(
                                           ways[index_of_current_way - 1]),
                                       current_role=way_queries.get_role(
                                           ways[index_of_current_way]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[index_of_current_way - 1]),
                                       current_oneway=way_queries.is_oneway(
                                           ways[index_of_current_way]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[index_of_current_way]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[index_of_current_way - 1]),
                                       count_of_forward_role_way_series=2)
    # Act
    prev_curr, error_information = highway_analyzer. \
        check_role_issues_in_continuous_way(prev_curr,
                                            error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_role == ""
    assert prev_curr.previous_role == "forward"
    assert prev_curr.current_oneway is True
    assert len(error_information) == 1
    assert error_information[0].error_type == "Wrong role setup"


def test_check_the_situation_with_2_by_2_highways_check_if_its_correct():
    # Arrange
    relation = analyzer_dicts.relation_info_no_gap_in_two_by_two_splitting_highway
    ways = relation["ways_to_search"]
    curr_way_index = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[curr_way_index - 1]),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       first_node_of_first_forward_way_in_the_series=way_queries.
                                       get_start_node(ways[1]),
                                       last_node_of_first_forward_way_in_the_series=way_queries.
                                       get_end_node(ways[1]),
                                       count_of_forward_role_way_series=1,
                                       network=way_queries.get_network(relation),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]))
    # Act
    prev_curr, error_information = highway_analyzer.check_the_situation_with_2_by_2_highways(
        prev_curr,
        error_information)
    assert len(prev_curr.last_forward_way_ref_nodes_before_backward) == 0
    assert prev_curr.motorway_split_way is False
    assert prev_curr.has_directional_roles is False
    assert len(error_information) == 0


def test_check_the_situation_with_2_by_2_motorways_when_one_side_ends_one_side_starts():
    # Arrange
    relation = analyzer_dicts.relation_info_motorway
    ways = relation["ways_to_search"]
    curr_way_index = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[curr_way_index - 1]),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       first_node_of_first_forward_way_in_the_series=way_queries.
                                       get_start_node(ways[1]),
                                       last_node_of_first_forward_way_in_the_series=way_queries.
                                       get_end_node(ways[1]),
                                       count_of_forward_role_way_series=1,
                                       network=way_queries.get_network(relation),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       route_number=way_queries.get_ref_of_the_route(relation))
    # Act
    prev_curr, error_information = highway_analyzer.check_the_situation_with_2_by_2_highways(
        prev_curr,
        error_information)
    assert prev_curr.last_forward_way_ref_nodes_before_backward == [
        way_queries.get_way_ref(ways[2]),
        prev_curr.previous_nodes]
    assert prev_curr.current_highway == "motorway"
    assert prev_curr.network.startswith("HU")
    assert prev_curr.route_number.startswith("M")
    assert prev_curr.motorway_split_way is True
    assert prev_curr.has_directional_roles is False
    assert len(error_information) == 0


def test_check_the_situation_with_2_by_2_ways_when_it_starts_from_a_complete_roundabout_no_gap():
    # Arrange
    relation = analyzer_dicts.relation_info_one_piece_roundabout_to_split_ways
    ways = relation["ways_to_search"]
    curr_way_index = 4
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[curr_way_index - 1]),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       first_node_of_first_forward_way_in_the_series=way_queries.
                                       get_start_node(ways[1]),
                                       last_node_of_first_forward_way_in_the_series=way_queries.
                                       get_end_node(ways[1]),
                                       count_of_forward_role_way_series=1,
                                       network=way_queries.get_network(relation),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       last_roundabout_nodes=way_queries.get_nodes(ways[1]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]))
    # Act
    prev_curr, error_information = highway_analyzer.check_the_situation_with_2_by_2_highways(
        prev_curr,
        error_information)
    assert prev_curr.last_forward_way_ref_nodes_before_backward == [
        way_queries.get_way_ref(ways[curr_way_index - 1]),
        prev_curr.previous_nodes]
    assert prev_curr.motorway_split_way is False
    assert prev_curr.has_directional_roles is False
    assert len(error_information) == 0


def test_check_the_situation_with_2_by_2_ways_when_it_starts_from_a_complete_roundabout_gap():
    # Arrange
    relation = analyzer_dicts.relation_info_one_piece_roundabout_to_split_ways_gap
    ways = relation["ways_to_search"]
    curr_way_index = 4
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_oneway=way_queries.is_oneway(
                                           ways[curr_way_index - 1]),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(
                                           relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       first_node_of_first_forward_way_in_the_series=way_queries.
                                       get_start_node(ways[1]),
                                       last_node_of_first_forward_way_in_the_series=way_queries.
                                       get_end_node(ways[1]),
                                       count_of_forward_role_way_series=1,
                                       network=way_queries.get_network(relation),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       last_roundabout_nodes=way_queries.get_nodes(ways[1]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]))
    # Act
    prev_curr, error_information = highway_analyzer.check_the_situation_with_2_by_2_highways(
        prev_curr,
        error_information)
    assert prev_curr.last_forward_way_ref_nodes_before_backward == [
        way_queries.get_way_ref(ways[curr_way_index - 1]),
        prev_curr.previous_nodes]
    assert prev_curr.motorway_split_way is False
    assert prev_curr.has_directional_roles is False
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in forward series"


def test_check_if_motorway_not_split():
    # Assert
    relation = analyzer_dicts.relation_info_motorway_not_split
    ways = relation["ways_to_search"]
    index_of_current_way = len(ways) - 1
    length_of_ways_to_search = len(ways)
    error_information = []
    prev_curr = PreviousCurrentHighway(
        index_of_current_way=index_of_current_way,
        current_highway=way_queries.get_highway(
            ways[index_of_current_way]),
        route_number=way_queries.get_ref_of_the_route(relation),
        network=way_queries.get_network(relation),
        current_role=way_queries.get_role(ways[index_of_current_way])
    )
    # Act
    highway_analyzer.check_if_motorway_not_split(prev_curr, length_of_ways_to_search,
                                                 error_information)
    assert prev_curr.motorway_split_way is False
    assert prev_curr.current_highway == "motorway"
    assert len(error_information) == 1
    assert error_information[0].error_type == "Motorway not split"


def test_check_if_way_connects_continuously():
    # Just throw in the parameters one of the tests - in the case of 2x2 highways.
    relation = analyzer_dicts.relation_info_one_piece_roundabout_to_split_ways_gap
    ways = relation["ways_to_search"]
    curr_way_index = 4
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(relation),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[curr_way_index - 1]),
                                       first_node_previous=way_queries.get_start_node(
                                           ways[curr_way_index - 1]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       first_node_of_first_forward_way_in_the_series=way_queries.
                                       get_start_node(ways[1]),
                                       last_node_of_first_forward_way_in_the_series=way_queries.
                                       get_end_node(ways[1]),
                                       count_of_forward_role_way_series=1,
                                       network=way_queries.get_network(relation),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       last_roundabout_nodes=way_queries.get_nodes(ways[1]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]))
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_if_way_connects_continuously(ways, prev_curr, error_information)

    assert prev_curr.motorway_split_way is False
    assert prev_curr.has_directional_roles is False
    assert prev_curr.previous_role == "forward"
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in forward series"
    assert prev_curr.last_forward_way_ref_nodes_before_backward == [
        way_queries.get_way_ref(ways[curr_way_index - 1]),
        prev_curr.previous_nodes]


# Continue with other tests from the same method!

def test_check_if_way_connects_continuously_checking_role_issues_wrong_role():
    relation = analyzer_dicts.relation_info_no_gap_in_first_forward_series_no_oneway
    ways = relation["ways_to_search"]
    curr_way_index = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(relation),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[curr_way_index - 1]),
                                       first_node_previous=way_queries.get_start_node(
                                           ways[curr_way_index - 1]),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]),
                                       count_of_forward_role_way_series=0,
                                       network=way_queries.get_network(relation),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index])
                                       )
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_if_way_connects_continuously(ways, prev_curr, error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_role == ""
    assert prev_curr.previous_role == "forward"
    assert prev_curr.current_oneway is True
    assert curr_way_index > 0
    assert curr_way_index > 0 and (way_queries.check_connectivity(prev_curr.first_node_previous,
                                                                  prev_curr.first_node_current,
                                                                  prev_curr.last_node_previous,
                                                                  prev_curr.last_node_current))
    assert len(error_information) == 1
    assert error_information[0].error_type == "Wrong role setup"


def test_check_if_way_connects_continuously_relation_info_one_piece_roundabout_gap():
    relation = analyzer_dicts.relation_info_one_piece_roundabout_gap
    ways = relation["ways_to_search"]
    curr_way_index = 2
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[curr_way_index - 1]),
                                       first_node_previous=way_queries.get_start_node(
                                           ways[curr_way_index - 1]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]),
                                       count_of_forward_role_way_series=0,
                                       network=way_queries.get_network(relation),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[curr_way_index - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[curr_way_index])
                                       )
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_if_way_connects_continuously(ways, prev_curr, error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_roundabout is False
    assert prev_curr.previous_roundabout is True
    assert curr_way_index > 0
    assert len(error_information) == 1
    assert error_information[0].error_type == "Roundabout gap"


def test_check_if_way_connects_continuously_relation_info_gap():
    relation = analyzer_dicts.relation_info_one_piece_roundabout_gap
    ways = relation["ways_to_search"]
    curr_way_index = 3
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[curr_way_index - 1]),
                                       first_node_previous=way_queries.get_start_node(
                                           ways[curr_way_index - 1]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]),
                                       count_of_forward_role_way_series=0,
                                       network=way_queries.get_network(relation),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[curr_way_index - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[curr_way_index])
                                       )
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_if_way_connects_continuously(ways, prev_curr, error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_roundabout is False
    assert prev_curr.previous_roundabout is False
    assert curr_way_index > 0
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap"


def test_check_if_way_connects_continuously_relation_info_no_gap():
    relation = analyzer_dicts.relation_info_one_piece_roundabout_gap
    ways = relation["ways_to_search"]
    curr_way_index = 4
    error_information = []
    prev_curr = PreviousCurrentHighway(index_of_current_way=curr_way_index,
                                       role_of_first_way=way_queries.get_role(ways[0]),
                                       previous_highway=way_queries.get_highway(
                                           ways[curr_way_index - 1]),
                                       previous_role=way_queries.get_role(ways[curr_way_index - 1]),
                                       previous_ref=way_queries.get_way_ref(
                                           ways[curr_way_index - 1]),
                                       previous_nodes=way_queries.get_nodes(
                                           ways[curr_way_index - 1]),
                                       last_node_previous=way_queries.get_end_node(
                                           ways[curr_way_index - 1]),
                                       first_node_previous=way_queries.get_start_node(
                                           ways[curr_way_index - 1]),
                                       current_highway=way_queries.get_highway(
                                           ways[curr_way_index]),
                                       is_mutcd_country=way_queries.
                                       determine_if_country_has_MUTCD_or_similar(relation),
                                       first_node_current=way_queries.get_start_node(
                                           ways[curr_way_index]),
                                       last_node_current=way_queries.get_end_node(
                                           ways[curr_way_index]),
                                       current_nodes=way_queries.get_nodes(ways[curr_way_index]),
                                       count_of_forward_role_way_series=0,
                                       network=way_queries.get_network(relation),
                                       route_number=way_queries.get_ref_of_the_route(relation),
                                       current_oneway=way_queries.is_oneway(ways[curr_way_index]),
                                       current_role=way_queries.get_role(ways[curr_way_index]),
                                       previous_roundabout=way_queries.is_roundabout(
                                           ways[curr_way_index - 1]),
                                       current_roundabout=way_queries.is_roundabout(
                                           ways[curr_way_index])
                                       )
    # Act
    prev_curr, error_information = \
        highway_analyzer.check_if_way_connects_continuously(ways, prev_curr, error_information)
    assert prev_curr.has_directional_roles is False
    assert prev_curr.current_roundabout is False
    assert prev_curr.previous_roundabout is False
    assert curr_way_index > 0
    assert len(error_information) == 0
