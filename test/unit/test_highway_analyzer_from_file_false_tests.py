#!/usr/bin/python3
import sys
from pathlib import Path

import xmltodict

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/analyzer")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from osm_data_parser import OSMDataParser
from analyzer import Analyzer

analyzer = Analyzer()
data_parser = OSMDataParser()


def test_route_forward_not_split_nooneway_multiple_fwd():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_forward_not_split_nooneway_multiple_fwd.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Forward and non-oneway without ability to move backward"
    assert correct_ways_count == 3


def test_route_forward_not_split_nooneway_only_one_fwd():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_forward_not_split_nooneway_only_one_fwd.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Forward and non-oneway without ability to move backward"
    assert correct_ways_count == 2


def test_route_simple_gap_in_road():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_simple_gap_in_road.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap"
    assert correct_ways_count == 3


def test_route_oneway_without_role():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_oneway_without_role.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Wrong role setup"
    assert correct_ways_count == 2


def test_route_forward_split_oneway_gap():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_forward_split_oneway_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in forward series"
    assert correct_ways_count == 5


def test_route_norole_split_nooneway():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_norole_split_nooneway.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap"
    assert correct_ways_count == 5


def test_route_closed_roundabout_entry_divided_exit_notdivided_norole():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_closed_roundabout_entry_divided_exit_notdivided_norole.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert error_information[0].error_type == "Wrong role setup"
    assert correct_ways_count == 3


def test_route_closed_roundabout_entry_divided_exit_divided_norole():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_closed_roundabout_entry_divided_exit_divided_norole.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 4
    assert error_information[0].error_type == "Wrong role setup"
    assert correct_ways_count == 3


def test_route_open_roundabout_entry_divided_exit_divided_no_role():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_open_roundabout_entry_divided_exit_divided_no_role.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert error_information[0].error_type == "Wrong role setup"
    assert correct_ways_count == 6


def test_route_open_roundabout_entry_divided_exit_divided_extra_members():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_open_roundabout_entry_divided_exit_divided_extra_members.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert error_information[0].error_type == "Duplicated roundabout ways"
    assert error_information[1].error_type == "Duplicated roundabout ways"
    assert correct_ways_count == 10


def test_route_open_roundabout_entry_divided_exit_divided_no_role_extra_members():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_open_roundabout_entry_divided_exit_divided_no_role_extra_members.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 10
    assert error_information[0].error_type == "Wrong role setup"
    assert error_information[1].error_type == "Forward role missing at roundabout"
    assert error_information[5].error_type == "Duplicated roundabout ways"
    assert error_information[6].error_type == "Forward role missing at roundabout"
    assert error_information[7].error_type == "Wrong role setup"
    assert error_information[8].error_type == "Gap"
    assert error_information[9].error_type == "Gap"
    assert correct_ways_count == 2


def test_route_motorway_two_sided_no_role():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_motorway_two_sided_no_role.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    assert 1 == 1
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 4
    assert error_information[0].error_type == "Wrong role setup"
    assert error_information[1].error_type == "Wrong role setup"
    assert error_information[2].error_type == "Gap"
    assert error_information[3].error_type == "Wrong role setup"
    assert correct_ways_count == 0


def test_route_motorway_not_split():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_motorway_not_split.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Motorway not split"
    assert correct_ways_count == 2


def test_route_closed_roundabout_entry_divided_exit_divided_wrong_order_of_entry_exit():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_closed_roundabout_entry_divided_exit_divided_wrong_order_of_entry.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    assert 1 == 1
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Wrong order of roundabout entries"
    assert correct_ways_count == 6
