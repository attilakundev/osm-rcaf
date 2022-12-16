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
import osm_data_parser_dicts
data_parser = OSMDataParser()


def get_xml_file(param):
    f = open(f'{project_path}/test/files/simplest_way.xml')
    return f.read()


def test_retrieve_XML_from_API(monkeypatch):
    monkeypatch.setattr(requests, "get", get_xml_file)
    relation_file = requests.get("")
    dictionary = xmltodict.parse(relation_file)
    assert dictionary == osm_data_parser_dicts.result_dict


def test_gather_way_and_relation_info_dict():
    relation_info = data_parser.gather_way_and_relation_info(osm_data_parser_dicts.result_dict)
    assert relation_info == osm_data_parser_dicts.relation_info_result


# list means that there are more than one ways and relation members and tags in it, so it goes well for that case too.
def test_gather_way_and_relation_info_list():
    relation_info = data_parser.gather_way_and_relation_info(osm_data_parser_dicts.result_dict_multi_ways)
    assert relation_info == osm_data_parser_dicts.relation_info_result_multi_ways


def test_helper_gather_relation_info_dict():
    relation_info: dict = {"ways_to_search": []}
    relation_info = data_parser.__gather_relation_info__(osm_data_parser_dicts.result_dict["osm"]["relation"].items(), relation_info)

    assert relation_info == {"ways_to_search": osm_data_parser_dicts.relation_info_result["ways_to_search"],
                             "ref": osm_data_parser_dicts.relation_info_result["ref"]}


# same meaning for list here as mentioned above.
def test_helper_gather_relation_info_list():
    relation_info: dict = {"ways_to_search": []}
    relation_info = data_parser.__gather_relation_info__(osm_data_parser_dicts.result_dict_multi_ways["osm"]["relation"].items(), relation_info)

    assert relation_info == {"ways_to_search": osm_data_parser_dicts.relation_info_result_multi_ways["ways_to_search"],
                             "ref": osm_data_parser_dicts.relation_info_result["ref"]}


def test_append_ways_to_search_with_useful_info():
    asd = data_parser.append_ways_to_search_with_useful_info(osm_data_parser_dicts.relation_info_result)
    assert asd == osm_data_parser_dicts.relation_info_result_appended


def test_helper_copy_attributes():
    attributes = data_parser.__copy_attributes__(osm_data_parser_dicts.relation_info_result["ways"][0])
    assert attributes == {
        '@id': '-101789'
    }
