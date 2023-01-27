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


def test_search_for_connection_exiting_from_open_roundabout_exit_split_wrong_order_with_extra_members():
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_entry_divided_exit_divided_wrong_order_extra_members.xml"
    # as manually discovered, the correction for this would be:
    # 1,2,4,8,9,6,3 (before reversing the other side) -> 1,2,4,8,3,6,9,10 (5,7 are extra members)
    relation_info = get_relation_info(file_path)
    corrected_ways_to_search, already_added_members = highway_fixer.highway_correction(relation_info, "-1")
    assert already_added_members == ["-1", "-2", "-4", "-8", "-3", "-6", "-9", "-10"]


def test_search_for_connection_exiting_from_closed_roundabout_exit_not_split_wrong_order():
    pass

#note: create a system test for correcting