#!/usr/bin/python3
from pathlib import Path
import xmltodict
from src.lib.way_queries import get_relation_ids
from src.lib.analyzer.analyzer import Analyzer

project_path = Path(__file__).parents[3].absolute()

analyzer = Analyzer()


def test_one_way_one_area_continuous():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/one_way_one_area_continuous.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 1


def test_two_way_one_area_continuous():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/two_way_one_area_continuous.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 2


def test_two_way_outer_one_inner_one_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/two_way_outer_one_inner_one_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 2


def test_two_way_outer_one_inner_one_pieces_same_role():
    file_path = \
        f"{project_path}/test/files/results_multi_analyzer/true/two_way_outer_one_inner_one_pieces_same_role.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 2


def test_three_way_outer_two_inner_one_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/three_way_outer_two_inner_one_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 3


def test_three_way_outer_one_inner_two_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/three_way_outer_one_inner_two_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 3


def test_four_way_outer_two_inner_two_pieces():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/four_way_outer_two_inner_two_pieces.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 4


def test_four_way_one_area_continuous():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/four_way_one_area_continuous.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 4


def test_eight_way_two_area_continuous():
    file_path = f"{project_path}/test/files/results_multi_analyzer/true/eight_way_two_area_continuous.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 8


def test_los_angeles_good():
    file_path = f"{project_path}/test/files/results_multi_analyzer/los_angeles_good.xml"
    file = open(file_path, "r", encoding="utf8").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 0
    assert correct_ways_count == 214


def test_los_angeles_bad():
    file_path = f"{project_path}/test/files/results_multi_analyzer/los_angeles_bad.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data)
    assert len(error_information) == 2
    assert correct_ways_count == 212


def test_double_multipolygon_check_second():
    file_path = f"{project_path}/test/files/results_multi_analyzer/double_multipolygon.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_ids = get_relation_ids(data)
    error_information, correct_ways_count, _ = analyzer.relation_checking(data, relation_ids[1])
    assert len(error_information) == 0
    assert correct_ways_count == 2
