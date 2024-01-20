#!/usr/bin/python3

from src.lib.osm_data_parser import retrieve_xml_from_api


def test_retrieve_xml_from_api():
    dictionary = retrieve_xml_from_api("23099")
    assert type(dictionary) is dict
