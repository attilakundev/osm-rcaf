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


def test_route_not_split_oneway():
    # Roundabout near Gödöllő, it used to be more complex though like what's in Zamárdi
    file_path = f"{project_path}/test/files/results_analyzer_false/route_not_split_nooneway.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    error_information, correct_ways_count = analyzer.relation_checking(data)
    assert len(error_information) == 1
    assert error_information[0].error_type == "Forward and non-oneway without ability to move backward"
    assert correct_ways_count == 3
