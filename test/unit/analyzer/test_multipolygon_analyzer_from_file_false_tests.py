#!/usr/bin/python3
from pathlib import Path
import xmltodict
from src.lib.osm_data_parser import OSMDataParser
from src.lib.analyzer.analyzer import Analyzer

project_path = Path(__file__).parents[3].absolute()

analyzer = Analyzer()
data_parser = OSMDataParser()


def test_one_way_one_area_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/one_way_one_area_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in an area consisting of one way"
    assert correct_ways_count == 0


def test_two_way_one_area_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/two_way_one_area_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in multi way multipolygon at the end"
    assert correct_ways_count == 1


def test_two_way_two_area_both_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"two_way_two_area_gap_both.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    assert 1 == 1
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert error_information[0].error_type == "Gap in an area consisting of one way"
    assert error_information[1].error_type == "Gap in an area consisting of one way at the end"
    assert correct_ways_count == 0


def test_two_way_two_area_first_way_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"two_way_two_area_gap_first_way.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in an area consisting of one way"
    assert correct_ways_count == 1


def test_two_way_two_area_second_way_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"two_way_two_area_gap_second_way.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Gap in an area consisting of one way at the end"
    assert correct_ways_count == 1


def test_two_area_multiple_pieces_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"two_area_multiple_pieces_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert error_information[0].error_type == "Gap in multi way multipolygon"
    assert error_information[1].error_type == "Gap in multi way multipolygon at the end"
    assert correct_ways_count == 2


def test_five_way_one_area_gap():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/five_way_one_area_gap.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert correct_ways_count == 3


def test_eight_way_two_area_gap_at_first():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"eight_way_two_area_gap_at_first.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert correct_ways_count == 6


def test_eight_way_two_area_gap_at_second():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"eight_way_two_area_gap_at_second.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert correct_ways_count == 6


def test_eight_way_two_area_both():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/" \
                f"eight_way_two_area_gap_both.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 4
    assert correct_ways_count == 4


def test_area_without_roles():
    file_path = f"{project_path}/test/files/results_multi_analyzer/false/area_without_roles.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 4
    assert error_information[0].error_type == "No role"
    assert correct_ways_count == 0
