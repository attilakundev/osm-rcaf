#!/usr/bin/python3
import mock as mock
import pytest
from unittest.mock import MagicMock
from pathlib import Path
import xmltodict
from src.lib.analyzer.analyzer import Analyzer
from src.lib.osm_data_parser import get_relation_ids, retrieve_xml_from_api, \
    gather_way_and_relation_info, __gather_relation_info__, \
    append_ways_to_search_with_useful_info, \
    __copy_attributes__, unparse_data_to_xml_prettified, check_way_attributes_id
from src.test.files import osm_data_parser_dicts

project_path = Path(__file__).parents[2].absolute()

analyzer = Analyzer()

@mock.patch("src.lib.osm_data_parser.requests.get")
def test_retrieve_xml_from_api(requests_get):
    mock_response = MagicMock()
    mock_response.content = open(f'{project_path}/test/files/simplest_way.xml').read()
    requests_get.return_value = mock_response
    result_dictionary = retrieve_xml_from_api("1")
    assert result_dictionary == osm_data_parser_dicts.result_dict


def test_get_relation_ids_multiple():
    file = open(f'{project_path}/test/files/results_multi_analyzer/double_multipolygon.xml',
                "r").read()
    data = xmltodict.parse(file)
    relation_ids = get_relation_ids(data)
    assert relation_ids == ["-99748", "-99750"]


def test_get_relation_ids_single():
    file = open(f'{project_path}/test/files/simplest_way.xml', "r").read()
    data = xmltodict.parse(file)
    relation_ids = get_relation_ids(data)
    assert relation_ids == "-99775"


def test_gather_way_and_relation_info_dict():
    relation_info = gather_way_and_relation_info(osm_data_parser_dicts.result_dict)
    assert relation_info == osm_data_parser_dicts.relation_info_result


# list means that there are more than a way and relation members and tags in it,
# so it goes well for that case too.
def test_gather_way_and_relation_info_list():
    relation_info = gather_way_and_relation_info(
        osm_data_parser_dicts.result_dict_multi_ways)
    assert relation_info == osm_data_parser_dicts.relation_info_result_multi_ways


def test_gather_way_and_relation_info_list_mutcd():
    relation_info = gather_way_and_relation_info(
        osm_data_parser_dicts.result_dict_MUTCD)
    assert relation_info == osm_data_parser_dicts.relation_info_result_relation_multiple_tags


def test_helper_gather_relation_info_dict():
    relation_info: dict = {"ways_to_search": []}
    relation_info = __gather_relation_info__(
        osm_data_parser_dicts.result_dict["osm"]["relation"].items(),
        relation_info)

    assert relation_info == {
        "ways_to_search": osm_data_parser_dicts.relation_info_result["ways_to_search"],
        "ref": osm_data_parser_dicts.relation_info_result["ref"],
        "route": osm_data_parser_dicts.relation_info_result["route"],
        "type": osm_data_parser_dicts.relation_info_result["type"]}


# same meaning for list here as mentioned above.
def test_helper_gather_relation_info_list():
    relation_info = gather_way_and_relation_info(
        osm_data_parser_dicts.result_dict_multi_relation)
    assert relation_info == osm_data_parser_dicts.relation_info_result


def test_append_ways_to_search_with_useful_info():
    result = append_ways_to_search_with_useful_info(
        osm_data_parser_dicts.relation_info_result)
    assert result == osm_data_parser_dicts.relation_info_result_appended
    result_where_relation_has_multiple_tags = append_ways_to_search_with_useful_info(
        osm_data_parser_dicts.relation_info_result_relation_multiple_tags)
    assert result_where_relation_has_multiple_tags == osm_data_parser_dicts.\
        relation_info_way_has_multiple_tags_result_appended


def test_helper_copy_attributes():
    attributes = __copy_attributes__(
        osm_data_parser_dicts.relation_info_result["ways"][0])
    assert attributes == {
        '@id': '-1'
    }


def test_unparse_data_to_xml_prettified():
    xml = unparse_data_to_xml_prettified(osm_data_parser_dicts.corrected_relation_data)
    final_result_xml_file_to_expect = open(f"{project_path}/test/files/final_result.xml").read()
    assert xml == final_result_xml_file_to_expect


def test_check_way_attributes_id():
    file_path = f"{project_path}/test/files/simplest_way_way_not_in_relation.xml"
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(data)
    with pytest.raises(KeyError):
        check_way_attributes_id(relation_info)
