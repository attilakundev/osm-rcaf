#!/usr/bin/python3
import sys
import xmltodict
from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/analyzer")
sys.path.append(f"{project_path}/lib/fixer")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from analyzer import Analyzer
from highway_fixer import HighwayFixer
import analyzer_dicts
import way_queries

highway_fixer = HighwayFixer()
analyzer = Analyzer()


def get_relation_info(file_path):
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    return relation_info


def test_search_for_connection_exiting_from_closed_roundabout_if_entry_exit_split_entry_wrong_order():
    # Arrange
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_closed_roundabout_entry_divided_exit_divided_wrong_order_of_entry.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2], ways_to_search[3]]
    already_added_members = ["-6", "-5", "-2"]
    roundabout_nodes = ["-20", "-21", "-22", "-8", "-7", "-6", "-5", "-24", "-23", "-15", "-16", "-17", "-18", "-19",
                        "-20"]
    # Act
    corrected_ways_to_search, already_added_members = highway_fixer.search_for_connection_exiting_from_closed_roundabout(
        roundabout_nodes, corrected_ways_to_search,
        already_added_members, ways_to_search)
    # Assert
    assert corrected_ways_to_search == [ways_to_search[0], ways_to_search[2], ways_to_search[3], ways_to_search[4],
                                        ways_to_search[5]]
    assert already_added_members == ["-6", "-5", "-2", "-1", "-3"]


def test_search_for_connection_exiting_from_closed_roundabout_if_entry_wrong_order_exit_wrong_order_both_split():
    # Arrange
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_divided_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2], ways_to_search[3]]
    already_added_members = ["-6", "-5", "-2"]
    roundabout_nodes = ["-20", "-21", "-22", "-8", "-7", "-6", "-5", "-24", "-23", "-15", "-16", "-17", "-18", "-19",
                        "-20"]
    # Act
    corrected_ways_to_search, already_added_members = highway_fixer.search_for_connection_exiting_from_closed_roundabout(
        roundabout_nodes, corrected_ways_to_search,
        already_added_members, ways_to_search)
    # Assert
    assert already_added_members == ["-6", "-5", "-2", "-1", "-3"]
    assert corrected_ways_to_search == [ways_to_search[0], ways_to_search[2], ways_to_search[3], ways_to_search[5],
                                        ways_to_search[4]]


def test_search_for_connection_exiting_from_closed_roundabout_if_entry_exit_not_split():
    # Arrange
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_not_divided_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    already_added_members = ["-6", "-5", "-2"]
    roundabout_nodes = ["-20", "-21", "-22", "-8", "-7", "-6", "-5", "-24", "-23", "-15", "-16", "-17", "-18", "-19",
                        "-20"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2], ways_to_search[4]]
    # Act
    corrected_ways_to_search, already_added_members = highway_fixer.search_for_connection_exiting_from_closed_roundabout(
        roundabout_nodes, corrected_ways_to_search,
        already_added_members, ways_to_search)
    assert already_added_members == ["-6", "-5", "-2", "-1"]
    assert corrected_ways_to_search == [ways_to_search[0], ways_to_search[2], ways_to_search[4],
                                        ways_to_search[3]]

    # Assert
    pass


def test_search_for_connection_wrong_order_road_connecting_to_a_oneway_road():
    file_path = f"{project_path}/test/files/files_for_fixer/search_for_connection_wrong_order_road.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 1
    first_node_previous = way_queries.get_start_node(ways_to_search[0])
    last_node_previous = way_queries.get_end_node(ways_to_search[0])
    already_added_members = ["-1"]
    corrected_ways_to_search = [ways_to_search[0]]
    number_of_members_of_this_forward_series = 0
    connecting_to_3rd_way_index = highway_fixer.search_for_connection(index, first_node_previous, last_node_previous,
                                                                      ways_to_search, already_added_members,
                                                                      corrected_ways_to_search,
                                                                      number_of_members_of_this_forward_series)
    assert connecting_to_3rd_way_index == 2


def test_search_for_connection_wrong_order_road_connecting_to_a_roundabout():
    file_path = f"{project_path}/test/files/files_for_fixer/search_for_connection_wrong_order_road.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 0
    first_node_previous = way_queries.get_start_node(ways_to_search[2])
    last_node_previous = way_queries.get_end_node(ways_to_search[2])
    already_added_members = ["-1", "-3"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2]]
    number_of_members_of_this_forward_series = 1
    connecting_to_3rd_way_index = highway_fixer.search_for_connection(index, first_node_previous, last_node_previous,
                                                                      ways_to_search, already_added_members,
                                                                      corrected_ways_to_search,
                                                                      number_of_members_of_this_forward_series)
    assert connecting_to_3rd_way_index == 1


def test_search_for_connection_wrong_order_road_connecting_searching_for_the_entry_after_exit():
    # Scenario 1st way connects to 3rd way
    # 3rd way connects to a roundabout piece on 2th place
    # 5th way exists, but the 6th way would be a roundabout piece, that would cause a loop, instead search for a oneway piece
    # 7th way
    file_path = f"{project_path}/test/files/files_for_fixer/search_for_connection_wrong_order_road.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 0
    first_node_previous = way_queries.get_start_node(ways_to_search[3])
    last_node_previous = way_queries.get_end_node(ways_to_search[3])
    already_added_members = ["-1", "-3", "-2", "-4"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2], ways_to_search[1], ways_to_search[3]]
    number_of_members_of_this_forward_series = 1
    connecting_to_3rd_way_index = highway_fixer.search_for_connection(index, first_node_previous, last_node_previous,
                                                                      ways_to_search, already_added_members,
                                                                      corrected_ways_to_search,
                                                                      number_of_members_of_this_forward_series)
    assert connecting_to_3rd_way_index == 5


def test_search_for_connection_wrong_order_road_closed_roundabout_return_forward_way_instead_of_roundabout():
    # So we're dealing with a section with a closed roundabout, with two entry ways
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_divided_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 0
    first_node_previous = way_queries.get_start_node(ways_to_search[2])
    last_node_previous = way_queries.get_end_node(ways_to_search[2])
    already_added_members = ["-1", "-3"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2]]
    number_of_members_of_this_forward_series = 1
    result = highway_fixer.search_for_connection(index, first_node_previous, last_node_previous,
                                                 ways_to_search, already_added_members,
                                                 corrected_ways_to_search,
                                                 number_of_members_of_this_forward_series)
    assert result == 1


def test_search_for_tag():
    tags_only_dict = {
        "tag": {
            '@k': "oneway",
            '@v': "yes"
        }
    }
    tags_list = {
        "tag": [
            {
                '@k': "oneway",
                '@v': "yes"
            },
            {
                '@k': "junction",
                '@v': "roundabout"
            }
        ]
    }
    assert highway_fixer.search_for_tag(tags_only_dict, "oneway", "yes") is True
    assert highway_fixer.search_for_tag(tags_only_dict, "a", "b") is False
    assert highway_fixer.search_for_tag(tags_list, "oneway", "yes") is True
    assert highway_fixer.search_for_tag(tags_list, "a", "b") is False


def test_add_tag_to_item():
    tags_only_dict = {
        "tag": {
            '@k': "oneway",
            '@v': "yes"
        }
    }
    tags_list = {
        "tag": [
            {
                '@k': "oneway",
                '@v': "yes"
            },
            {
                '@k': "junction",
                '@v': "roundabout"
            }
        ]
    }

    result_tags_only_dict = {
        "tag": [
            {
                '@k': "oneway",
                '@v': "yes"
            },
            {
                '@k': "a",
                '@v': "b"
            }
        ]
    }
    result_tags_list = {
        "tag": [
            {
                '@k': "oneway",
                '@v': "yes"
            },
            {
                '@k': "junction",
                '@v': "roundabout"
            },
            {
                '@k': "a",
                '@v': "b"
            }
        ]
    }
    add_item_to_dict = highway_fixer.add_tag_to_item("a", "b", tags_only_dict)
    add_item_to_list = highway_fixer.add_tag_to_item("a", "b", tags_list)

    assert add_item_to_dict == result_tags_only_dict
    assert add_item_to_list == result_tags_list


def test_insert_array_items_to_a_specific_position():
    where = ["-1", "-2", "-3", "-6", "-5", "-7"]
    from_array = ["-5", "-6", "-7"]
    to_position = 3
    how_many = len(from_array)
    result_assert = ["-1", "-2", "-3", "-5", "-6", "-7"]
    result = highway_fixer.insert_array_items_to_a_specific_position(where, from_array, to_position, how_many)
    assert result == result_assert


def test_remove_oneway_and_forward_tag_from_certain_members_remove_true():
    # We delete the oneway/forward tag from those which shouldn't be in the relation, since the route doesn't split.
    file_path = f"{project_path}/test/files/files_for_fixer/route_bad_tags_roles.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 5
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[1], ways_to_search[2], ways_to_search[3],
                                ways_to_search[4], ways_to_search[5], ways_to_search[6]]
    current_forward = way_queries.get_role(ways_to_search[index]) == "forward"  # should give false
    current_oneway = way_queries.is_oneway(ways_to_search[index])  # should give true,
    current_roundabout = way_queries.is_roundabout(ways_to_search[index])  # should give false
    remove_oneway_true = True
    oneway_series_starting_way_index = 4
    oneway_series_ending_way_index = 5
    corrected_ways_to_search_removed, remove_one_way_tag, oneway_series_starting_way_index, oneway_series_ending_way_index = highway_fixer.remove_oneway_and_forward_tag_from_certain_members(
        corrected_ways_to_search, current_forward, current_oneway, current_roundabout, index, remove_oneway_true,
        oneway_series_starting_way_index, oneway_series_ending_way_index
    )
    assert way_queries.get_role(corrected_ways_to_search_removed[index]) == ""
    assert way_queries.is_oneway(corrected_ways_to_search_removed[index]) is False
    assert remove_one_way_tag is False
    assert oneway_series_starting_way_index == -1
    assert oneway_series_ending_way_index == -1


def test_remove_oneway_and_forward_tag_from_certain_members_remove_false():
    # We delete the oneway/forward tag from those which shouldn't be in the relation, since the route doesn't split.
    file_path = f"{project_path}/test/files/files_for_fixer/route_bad_tags_roles.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 4
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[1], ways_to_search[2], ways_to_search[3],
                                ways_to_search[4], ways_to_search[5], ways_to_search[6], ways_to_search[7]]
    current_forward = way_queries.get_role(ways_to_search[index]) == "forward"  # should give true
    current_oneway = way_queries.is_oneway(ways_to_search[index])  # should give true,
    current_roundabout = way_queries.is_roundabout(ways_to_search[index])  # should give false
    remove_oneway_false = False
    oneway_series_starting_way_index = 4
    oneway_series_ending_way_index = 5
    corrected_ways_to_search, remove_one_way_tag, oneway_series_starting_way_index, oneway_series_ending_way_index = highway_fixer.remove_oneway_and_forward_tag_from_certain_members(
        corrected_ways_to_search, current_forward, current_oneway, current_roundabout, index, remove_oneway_false,
        oneway_series_starting_way_index, oneway_series_ending_way_index
    )
    assert way_queries.get_role(corrected_ways_to_search[index]) == "forward"
    assert way_queries.is_oneway(corrected_ways_to_search[index]) is True
    assert remove_one_way_tag is False
    assert oneway_series_starting_way_index == 4
    assert oneway_series_ending_way_index == 5


def test_remove_oneway_tag_from_non_roundabout_members_if_needed_remove_one_way_tag_is_false():
    file_path = f"{project_path}/test/files/files_for_fixer/search_for_connection_wrong_order_road_non_roundabout.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[1], ways_to_search[2], ways_to_search[3],
                                ways_to_search[5], ways_to_search[4], ways_to_search[6]]
    index = 6
    oneway_series_starting_way_index = 1
    oneway_series_ending_way_index = 5
    oneway_series_starting_node_detected = False
    closed_roundabout_detected = False
    previous_oneway = way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"  # should give false
    current_oneway = way_queries.is_oneway(corrected_ways_to_search[index])  # should give false,
    current_roundabout = way_queries.is_roundabout(corrected_ways_to_search[index])  # should give false
    previous_forward = way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"
    current_forward = way_queries.get_role(corrected_ways_to_search[index]) == "forward"
    remove_one_way_tag = False

    index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected = highway_fixer.remove_oneway_tag_from_non_roundabout_members_if_needed(
        corrected_ways_to_search, current_forward,
        current_oneway, index, oneway_series_ending_way_index,
        oneway_series_starting_node_detected,
        oneway_series_starting_way_index, previous_forward,
        previous_oneway, remove_one_way_tag, current_roundabout, closed_roundabout_detected)
    assert index == 1
    assert oneway_series_starting_way_index == 1
    assert oneway_series_ending_way_index == 5
    assert oneway_series_starting_node_detected is False
    assert remove_one_way_tag is True
    # Determine if the oneway series starting node is detected
    oneway_series_starting_node_detected = True
    index = 6
    index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected = highway_fixer.remove_oneway_tag_from_non_roundabout_members_if_needed(
        corrected_ways_to_search, current_forward,
        current_oneway, index, oneway_series_ending_way_index,
        oneway_series_starting_node_detected,
        oneway_series_starting_way_index, previous_forward,
        previous_oneway, remove_one_way_tag, current_roundabout, closed_roundabout_detected)
    assert index == 6  # since we didn't change the index variable...
    assert oneway_series_starting_way_index == 1
    assert oneway_series_ending_way_index == 5
    assert oneway_series_starting_node_detected is False
    assert remove_one_way_tag is True
    # Determine at the end of the oneway series that we are at the end of it or not
    index = 5
    previous_oneway = way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"  # should give true
    current_oneway = way_queries.is_oneway(corrected_ways_to_search[index])  # should give true,
    current_roundabout = way_queries.is_roundabout(corrected_ways_to_search[index])
    previous_forward = way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"
    current_forward = way_queries.get_role(corrected_ways_to_search[index]) == "forward"
    index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected = highway_fixer.remove_oneway_tag_from_non_roundabout_members_if_needed(
        corrected_ways_to_search, current_forward,
        current_oneway, index, oneway_series_ending_way_index,
        oneway_series_starting_node_detected,
        oneway_series_starting_way_index, previous_forward,
        previous_oneway, remove_one_way_tag, current_roundabout, closed_roundabout_detected)
    assert index == 5  # since we didn't change the index variable...
    assert oneway_series_starting_way_index == 1
    assert oneway_series_ending_way_index == 5
    assert oneway_series_starting_node_detected is False
    assert remove_one_way_tag is True


def test_remove_oneway_tag_from_non_roundabout_members_if_needed_remove_one_way_tag_is_false_closed_roundabout():
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_divided_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2], ways_to_search[1], ways_to_search[3],
                                ways_to_search[5], ways_to_search[4], ways_to_search[6]]
    index = 3
    oneway_series_starting_way_index = 1
    oneway_series_ending_way_index = 2
    oneway_series_starting_node_detected = True
    closed_roundabout_detected = True
    previous_oneway = way_queries.get_role(ways_to_search[index - 1]) == "forward"  # should give true
    current_oneway = way_queries.is_oneway(ways_to_search[index])  # should give false,
    current_roundabout = way_queries.is_roundabout(ways_to_search[index])  # should give true
    previous_forward = way_queries.get_role(ways_to_search[index - 1]) == "forward"
    current_forward = way_queries.get_role(ways_to_search[index]) == "forward"
    remove_one_way_tag = False

    index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected = highway_fixer.remove_oneway_tag_from_non_roundabout_members_if_needed(
        corrected_ways_to_search, current_forward,
        current_oneway, index, oneway_series_ending_way_index,
        oneway_series_starting_node_detected,
        oneway_series_starting_way_index, previous_forward,
        previous_oneway, remove_one_way_tag, current_roundabout, closed_roundabout_detected)
    assert index == 3
    assert oneway_series_starting_way_index == 1
    assert oneway_series_ending_way_index == 2
    assert oneway_series_starting_node_detected is False
    assert remove_one_way_tag is False


def test_detect_if_oneway_road_is_split_or_not():
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_divided_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[2], ways_to_search[1], ways_to_search[3],
                                ways_to_search[5], ways_to_search[4], ways_to_search[6]]

    index = 2
    oneway_series_starting_way_index = 1
    corrected_first_node_current = way_queries.get_start_node(corrected_ways_to_search[index])
    corrected_last_node_current = way_queries.get_end_node(corrected_ways_to_search[index])
    oneway_series_starting_node_detected = False
    oneway_series_starting_node_detected = highway_fixer.detect_if_oneway_road_is_split_or_not(
        corrected_first_node_current, corrected_last_node_current,
        corrected_ways_to_search, index, oneway_series_starting_node_detected,
        oneway_series_starting_way_index)
    assert oneway_series_starting_node_detected is True

    oneway_series_starting_way_index = -1
    oneway_series_starting_node_detected = False
    oneway_series_starting_node_detected = highway_fixer.detect_if_oneway_road_is_split_or_not(
        corrected_first_node_current, corrected_last_node_current,
        corrected_ways_to_search, index, oneway_series_starting_node_detected,
        oneway_series_starting_way_index)
    assert oneway_series_starting_node_detected is False


def test_add_forward_role_where_needed():
    file_path = f"{project_path}/test/files/files_for_fixer/route_bad_tags_roles.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    # here the order doesn't matter since it's a unit test.
    index = 2
    corrected_first_node_current = way_queries.get_start_node(ways_to_search[index])
    corrected_first_node_previous = way_queries.get_start_node(ways_to_search[index - 1])
    corrected_last_node_current = way_queries.get_end_node(ways_to_search[index])
    corrected_last_node_previous = way_queries.get_end_node(ways_to_search[index - 1])
    current_oneway = way_queries.is_oneway(ways_to_search[index])
    previous_oneway = way_queries.is_oneway(ways_to_search[index])
    corrected_ways_to_search = highway_fixer.add_forward_role_where_needed(corrected_first_node_current,
                                                                           corrected_first_node_previous,
                                                                           corrected_last_node_current,
                                                                           corrected_last_node_previous,
                                                                           ways_to_search, current_oneway,
                                                                           index, previous_oneway)
    assert way_queries.get_role(corrected_ways_to_search[index]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"


def test_add_forward_role_where_needed_roundabout_edition():
    file_path = f"{project_path}/test/files/files_for_fixer/route_bad_tags_roles.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    index = 8
    corrected_first_node_current = way_queries.get_start_node(ways_to_search[index])
    corrected_first_node_previous = way_queries.get_start_node(ways_to_search[index - 1])
    corrected_last_node_current = way_queries.get_end_node(ways_to_search[index])
    corrected_last_node_previous = way_queries.get_end_node(ways_to_search[index - 1])
    current_oneway = way_queries.is_oneway(ways_to_search[index])
    previous_oneway = way_queries.is_oneway(ways_to_search[index])
    corrected_ways_to_search = highway_fixer.add_forward_role_where_needed(corrected_first_node_current,
                                                                           corrected_first_node_previous,
                                                                           corrected_last_node_current,
                                                                           corrected_last_node_previous,
                                                                           ways_to_search, current_oneway,
                                                                           index, previous_oneway)
    assert way_queries.get_role(corrected_ways_to_search[index]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"


def test_correct_way_roles_tags():
    file_path = f"{project_path}/test/files/files_for_fixer/route_bad_tags_roles.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[1], ways_to_search[2], ways_to_search[3],
                                ways_to_search[4], ways_to_search[5], ways_to_search[6], ways_to_search[7],
                                ways_to_search[8]]
    corrected_ways_to_search = highway_fixer.correct_way_roles_tags(corrected_ways_to_search)
    assert way_queries.get_role(corrected_ways_to_search[1]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[2]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[3]) == ""
    assert way_queries.get_role(corrected_ways_to_search[7]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[8]) == "forward"


def test_check_for_forward_ways_end_of_split_highway():
    # correct order is 1,4,6,5,2,3, but we now check the 1,4,6,2,5 case, when it's not reversed.
    file_path = f"{project_path}/test/files/files_for_fixer/route_split_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[3], ways_to_search[5], ways_to_search[1]]
    already_added_members = ["-1", "-4", "-6", "-2"]
    index = 4
    index_of_the_connecting_way = 4  # since it's in order "luckily"
    number_of_members_of_this_forward_series = 3
    previous_role = way_queries.get_role(corrected_ways_to_search[index - 1])
    first_node_previous = way_queries.get_start_node(corrected_ways_to_search[index - 1])
    last_node_previous = way_queries.get_end_node(corrected_ways_to_search[index - 1])
    split_highway_members = [ways_to_search[3], ways_to_search[5], ways_to_search[1]]
    banned_roundabout_ways = []
    already_added_members, corrected_ways_to_search, split_highway_members, number_of_members_of_this_forward_series = highway_fixer.check_for_forward_ways(
        already_added_members, corrected_ways_to_search,
        first_node_previous,
        index_of_the_connecting_way, last_node_previous,
        number_of_members_of_this_forward_series,
        previous_role, split_highway_members,
        ways_to_search, banned_roundabout_ways)
    assert already_added_members == ["-1", "-4", "-6", "-5", "-2"]
    assert number_of_members_of_this_forward_series == 4


def test_check_for_forward_ways_way_after_split_highway():
    # correct order is 1,4,6,5,2,3, but we now check the 1,4,6,2,5 case, when it's not reversed.
    file_path = f"{project_path}/test/files/files_for_fixer/route_split_wrong_order.xml"
    relation_info = get_relation_info(file_path)
    ways_to_search = relation_info["ways_to_search"]
    corrected_ways_to_search = [ways_to_search[0], ways_to_search[3], ways_to_search[5], ways_to_search[4],
                                ways_to_search[1]]
    already_added_members = ["-1", "-4", "-6", "-5", "-2"]
    index = 5
    index_of_the_connecting_way = 2
    number_of_members_of_this_forward_series = 4
    previous_role = way_queries.get_role(corrected_ways_to_search[index - 1])
    first_node_previous = way_queries.get_start_node(corrected_ways_to_search[index - 1])
    last_node_previous = way_queries.get_end_node(corrected_ways_to_search[index - 1])
    split_highway_members = [ways_to_search[3], ways_to_search[5], ways_to_search[1]]
    banned_roundabout_ways = []
    already_added_members, corrected_ways_to_search, split_highway_members, number_of_members_of_this_forward_series = highway_fixer.check_for_forward_ways(
        already_added_members, corrected_ways_to_search,
        first_node_previous,
        index_of_the_connecting_way, last_node_previous,
        number_of_members_of_this_forward_series,
        previous_role, split_highway_members,
        ways_to_search, banned_roundabout_ways)
    assert already_added_members == ["-1", "-4", "-6", "-5", "-2", "-3"]
    assert number_of_members_of_this_forward_series == 0


