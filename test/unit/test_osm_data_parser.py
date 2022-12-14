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
from osm_data_parser import OSMDataParser

data_parser = OSMDataParser()

result_dict = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-101768',
                '@action': 'modify',
                '@visible': 'true',
                '@lat': '38.9227584215',
                '@lon': '-81.21145252705'
            },
            {
                '@id': '-101769',
                '@action': 'modify',
                '@visible': 'true',
                '@lat': '38.92212404922',
                '@lon': '-81.1961746645',
            }
        ],
        'way': {
            '@id': '-101789',
            '@action': 'modify',
            '@visible': 'true',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        },
        'relation': {
            '@id': '-99775',
            '@action': 'modify',
            '@visible': 'true',
            'member': {
                '@type': 'way',
                '@ref': '-101789',
                '@role': 'outer'
            },
            'tag': {
                '@k': 'ref',
                '@v': '999'
            }
        }
    }
}

result_dict_multi_ways = {
    'osm': {
        '@generator': 'JOSM',
        '@version': '0.6',
        'node': [
            {
                '@id': '-101768',
                '@action': 'modify',
                '@visible': 'true',
                '@lat': '38.9227584215',
                '@lon': '-81.21145252705'
            },
            {
                '@id': '-101769',
                '@action': 'modify',
                '@visible': 'true',
                '@lat': '38.92212404922',
                '@lon': '-81.1961746645',
            }
        ],
        'way': [{
            '@id': '-101789',
            '@action': 'modify',
            '@visible': 'true',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        },
            {
                '@id': '-101790',
                '@action': 'modify',
                '@visible': 'true',
                'nd': [
                    {'@ref': '-101768'},
                    {'@ref': '-101769'}
                ]
            }
        ],
        'relation': {
            '@id': '-99775',
            '@action': 'modify',
            '@visible': 'true',
            'member': [{
                '@type': 'way',
                '@ref': '-101789',
                '@role': 'outer'
            },
                {
                    '@type': 'way',
                    '@ref': '-101790',
                    '@role': 'outer'
                },
            ],
            'tag': {
                '@k': 'ref',
                '@v': '999'
            }
        }
    }
}

relation_info_result = {
    'nodes': [
        {
            '@id': '-101768',
            '@action': 'modify',
            '@visible': 'true',
            '@lat': '38.9227584215',
            '@lon': '-81.21145252705'
        },
        {
            '@id': '-101769',
            '@action': 'modify',
            '@visible': 'true',
            '@lat': '38.92212404922',
            '@lon': '-81.1961746645',
        }
    ],
    'ways': [
        {
            '@id': '-101789',
            '@action': 'modify',
            '@visible': 'true',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-101789',
            '@role': 'outer'
        }
    ],
    'ref': '999'
}

relation_info_result_multi_ways = {
    'nodes': [
        {
            '@id': '-101768',
            '@action': 'modify',
            '@visible': 'true',
            '@lat': '38.9227584215',
            '@lon': '-81.21145252705'
        },
        {
            '@id': '-101769',
            '@action': 'modify',
            '@visible': 'true',
            '@lat': '38.92212404922',
            '@lon': '-81.1961746645',
        }
    ],
    'ways': [
        {
            '@id': '-101789',
            '@action': 'modify',
            '@visible': 'true',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        },
        {
            '@id': '-101790',
            '@action': 'modify',
            '@visible': 'true',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-101789',
            '@role': 'outer'
        },
        {
            '@type': 'way',
            '@ref': '-101790',
            '@role': 'outer'
        }
    ],
    'ref': '999'
}

relation_info_result_appended = {
    'nodes': [
        {
            '@id': '-101768',
            '@action': 'modify',
            '@visible': 'true',
            '@lat': '38.9227584215',
            '@lon': '-81.21145252705'
        },
        {
            '@id': '-101769',
            '@action': 'modify',
            '@visible': 'true',
            '@lat': '38.92212404922',
            '@lon': '-81.1961746645',
        }
    ],
    'ways': [
        {
            '@id': '-101789',
            '@action': 'modify',
            '@visible': 'true',
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ways_to_search': [
        {
            '@type': 'way',
            '@ref': '-101789',
            '@role': 'outer',
            'attributes': {
                '@id': '-101789',
                '@action': 'modify',
                '@visible': 'true'
            },
            'nd': [
                {'@ref': '-101768'},
                {'@ref': '-101769'}
            ]
        }
    ],
    'ref': '999'
}


def get_xml_file(param):
    f = open(f'{project_path}/test/files/one_member_way.xml')
    return f.read()


def test_retrieve_XML_from_API(monkeypatch):
    monkeypatch.setattr(requests, "get", get_xml_file)
    relation_file = requests.get("")
    dictionary = xmltodict.parse(relation_file)
    assert dictionary == result_dict


def test_gather_way_and_relation_info_dict():
    relation_info = data_parser.gather_way_and_relation_info(result_dict)
    assert relation_info == relation_info_result


# list means that there are more than one ways and relation members and tags in it, so it goes well for that case too.
def test_gather_way_and_relation_info_list():
    relation_info = data_parser.gather_way_and_relation_info(result_dict_multi_ways)
    assert relation_info == relation_info_result_multi_ways


def test_helper_gather_relation_info_dict():
    relation_info: dict = {"ways_to_search": []}
    relation_info = data_parser.__gather_relation_info__(result_dict["osm"]["relation"].items(), relation_info)

    assert relation_info == {"ways_to_search": relation_info_result["ways_to_search"],
                             "ref": relation_info_result["ref"]}


# same meaning for list here as mentioned above.
def test_helper_gather_relation_info_list():
    relation_info: dict = {"ways_to_search": []}
    relation_info = data_parser.__gather_relation_info__(result_dict_multi_ways["osm"]["relation"].items(), relation_info)

    assert relation_info == {"ways_to_search": relation_info_result_multi_ways["ways_to_search"],
                             "ref": relation_info_result["ref"]}


def test_append_ways_to_search_with_useful_info():
    asd = data_parser.append_ways_to_search_with_useful_info(relation_info_result)
    assert asd == relation_info_result_appended


def test_helper_copy_attributes():
    attributes = data_parser.__copy_attributes__(relation_info_result["ways"][0])
    assert attributes == {
        '@id': '-101789',
        '@action': 'modify',
        '@visible': 'true'
    }
