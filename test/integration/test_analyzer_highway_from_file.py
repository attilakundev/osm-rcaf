#!/usr/bin/python3
import sys
from pathlib import Path

import xmltodict

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from osm_data_parser import OSMDataParser
from analyzer import Analyzer

analyzer = Analyzer()
data_parser = OSMDataParser()

def test_double_roundabout_divided_2_by_2_ways_forward_role():
    file_path = f"{project_path}/test/files/results_analyzer_true/route_double_roundabout_divided_2_by_2_ways_forward_role.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    way_ids = data_parser.check_way_attributes_id(relation_info)
    assert way_ids == ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10", "-11", "-12"]
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 12
def test_route_closed_roundabout_correct_roles_correct_order():
    file_path = f"{project_path}/test/files/results_analyzer_true/route_closed_roundabout_correct_roles_correct_order.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    way_ids = data_parser.check_way_attributes_id(relation_info)
    assert way_ids == ["-6", "-5", "-4", "-2", "-1", "-3", "-7"]
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 7


def test_route_open_roundabout_correct_roles_correct_order():
    file_path = f"{project_path}/test/files/results_analyzer_true/route_open_roundabout_correct_roles_and_order.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    way_ids = data_parser.check_way_attributes_id(relation_info)
    assert way_ids == ["-6", "-5", "-9", "-1", "-4", "-2", "-3", "-7"]
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 8

def test_route_split_oneway():
    file_path = f"{project_path}/test/files/results_analyzer_true/route_split_oneway.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    way_ids = data_parser.check_way_attributes_id(relation_info)
    assert way_ids == ["-1", "-4", "-2", "-3"]
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 4


def test_route_splits_at_the_end():
    file_path = f"{project_path}/test/files/results_analyzer_true/route_way_splits_at_the_end.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    way_ids = data_parser.check_way_attributes_id(relation_info)
    assert way_ids == ["-1", "-2", "-3", "-4", "-5", "-6"]
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 6

def test_route_motorway_two_sided():
    file_path = f"{project_path}/test/files/results_analyzer_true/route_motorway_two_sided.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    way_ids = data_parser.check_way_attributes_id(relation_info)
    assert way_ids == ["-1", "-2", "-3", "-4"]
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 4
