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


def test_search_for_connection_exiting_from_open_roundabout_exit_split_wrong_order_with_extra_members():
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_entry_divided_exit_divided_wrong_order_extra_members.xml"
    # as manually discovered, the correction for this would be:
    # 1,2,4,8,9,6,3 (before reversing the other side) -> 1,2,4,8,3,6,9,10 (5,7 are extra members)
    relation_info = get_relation_info(file_path)
    corrected_ways_to_search, already_added_members = highway_fixer.highway_correction(relation_info, "-1")
    assert already_added_members == ["-1", "-2", "-4", "-8", "-3", "-6", "-9", "-10"]
    pass


def test_search_for_connection_exiting_from_open_roundabout_exit_not_split_wrong_order():
    pass
