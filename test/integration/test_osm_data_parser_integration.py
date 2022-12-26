#!/usr/bin/python3
import pytest
import sys
from pathlib import Path
import requests
import xml

import xmltodict

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/test/files")
from osm_data_parser import OSMDataParser
import way_queries
import osm_data_parser_dicts
data_parser = OSMDataParser()

def test_retrieve_XML_from_API():
    dictionary = data_parser.retrieve_XML_from_API("23099")
    assert type(dictionary) is dict
