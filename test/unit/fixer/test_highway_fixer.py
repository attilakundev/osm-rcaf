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
    where = ["-1", "-2", "-3", "-4"]
    from_array = ["-5", "-6", "-7"]
    to_position = 2
    how_many = 2
    result_assert = ["-1", "-2", "-3", "-5", "-6", "-4"]
    result = highway_fixer.insert_array_items_to_a_specific_position(where,from_array,to_position,how_many)
    assert result == result_assert