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


def test_one_way_one_area_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/one_way_one_area_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert correct_ways_count == 0


def test_two_way_one_area_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/two_way_one_area_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert correct_ways_count == 1


def test_two_way_two_area_both_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/two_way_two_area_both_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    assert 1 == 1
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert correct_ways_count == 0


def test_two_way_two_area_first_way_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/two_way_two_area_first_way_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert correct_ways_count == 1


def test_two_way_two_area_second_way_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/two_way_two_area_second_way_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert correct_ways_count == 1


def test_two_area_multiple_pieces_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/two_area_multiple_pieces_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert correct_ways_count == 2
