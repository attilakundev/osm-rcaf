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


def test_one_way_one_area_continuous():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/one_way_one_area_continuous.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    assert 1 == 1
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 1

def test_two_way_one_area_continuous():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/two_way_one_area_continuous.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    assert 1 == 1
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 2

def test_two_way_outer_one_inner_one_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/two_way_outer_one_inner_one_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 2
def test_two_way_outer_one_inner_one_pieces_same_role():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/two_way_outer_one_inner_one_pieces_same_role.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 2

def test_three_way_outer_two_inner_one_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/three_way_outer_two_inner_one_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 3

def test_three_way_outer_one_inner_two_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/three_way_outer_one_inner_two_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 3

def test_four_way_outer_two_inner_two_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/four_way_outer_two_inner_two_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 4