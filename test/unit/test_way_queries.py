#!/usr/bin/python3
import pytest
import sys

from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/test/files")
import way_queries
import way_queries_dicts
import osm_data_parser_dicts


def test_get_nodes():
    # Arrange is done at the beginning
    # Act
    nodes = way_queries.get_nodes(way_queries_dicts.relation["ways"][0])
    # Assert
    assert nodes == [1, 2, 3]
def test_get_role():
    has_role = way_queries.get_role(way_queries_dicts.relation["ways"][0])
    no_role = way_queries.get_role(way_queries_dicts.relation2)
    assert has_role == "forward"
    assert no_role == ""

def test_start_node():
    # Arrange is done at the beginning
    # Act
    first_node = way_queries.get_start_node(way_queries_dicts.relation["ways"][0])
    # Assert
    assert first_node == 1


def test_end_node():
    # Arrange is done at the beginning
    # Act
    last_node = way_queries.get_end_node(way_queries_dicts.relation["ways"][0])
    # Assert
    assert last_node == 3


def test_get_way_ref():
    assert way_queries.get_way_ref(way_queries_dicts.relation["ways"][2]) == "3"
    assert way_queries.get_way_ref(way_queries_dicts.relation["ways"]) == ""

def test_get_highway():
    assert way_queries.get_highway(way_queries_dicts.relation["ways"][0]) == "primary"
    assert way_queries.get_highway(way_queries_dicts.relation["ways"][2]) == ""
    assert way_queries.get_highway(way_queries_dicts.relation["ways"]) == ""
def test_get_railway():
    assert way_queries.get_railway(way_queries_dicts.relation["ways"][0]) == "rail"
    assert way_queries.get_railway(way_queries_dicts.relation["ways"][3]) == ""
    assert way_queries.get_railway(way_queries_dicts.relation["ways"]) == ""
def test_get_highway_ref():
    assert way_queries.get_highway_ref(way_queries_dicts.relation["ways"][0]) == ""
    assert way_queries.get_highway_ref(way_queries_dicts.relation["ways"][1]) == "3"
    assert way_queries.get_highway_ref(way_queries_dicts.relation["ways"]) == ""

def test_is_roundabout():
    # Arrange is done at the beginning
    # Act
    roundabout = way_queries.is_roundabout(way_queries_dicts.relation["ways"][0])
    # Assert
    assert roundabout


def test_is_oneway():
    # Arrange is done at the beginning
    # Act
    oneway = way_queries.is_oneway(way_queries_dicts.relation["ways"][0])
    # Assert
    assert oneway


def test_remove_tag():
    # Arrange is done at the beginning
    # Act
    way_queries.remove_tag(way_queries_dicts.relation["ways"][0], "oneway", "yes")
    way_queries.remove_tag(osm_data_parser_dicts.relation_info_result_appended["ways"][0], "oneway", "yes")
    # Assert
    assert way_queries_dicts.relation["ways"][0]["tag"] == [{
        "@k": "highway",
        "@v": "primary"
    },
        {
            "@k": "railway",
            "@v": "rail"
        }, {
            "@k": "junction",
            "@v": "roundabout"
        }]
    assert osm_data_parser_dicts.relation_info_result_appended["ways"][0]["tag"] == []


def test_modify_role():
    way_queries.modify_role(way_queries_dicts.relation["ways"][0], "backward")
    assert way_queries_dicts.relation["ways"][0]["@role"] == "backward"
    way_queries.modify_role(way_queries_dicts.relation["ways"][0], "forward")
    assert way_queries_dicts.relation["ways"][0]["@role"] == "forward"

def test_get_ref_of_the_route():
    # Arrange is done at the beginning
    # Act
    ref = way_queries.get_ref_of_the_route(way_queries_dicts.relation)
    # Assert
    assert ref == 710


def test_get_id_of_the_relation_members():
    # Arrange is done at the beginning
    # Act
    refs = way_queries.get_id_of_the_relation_members(way_queries_dicts.relation["ways"])
    # Assert
    assert refs == ['1', '2', '3', '4']


def test_put_ref_from_relation_to_highway_way():
    # Arrange
    assertion = {
        "@k": "ref",
        "@v": 710
    }
    # Act
    way_queries.put_ref_from_relation_to_highway_way(way_queries_dicts.relation)
    # Assert - this will be a for loop since we check the entire way_queries_dicts.relation of highways
    for index, element in enumerate(way_queries_dicts.relation["ways"]):
        if element["@type"] == "way":
            for key_value_pair in element["tag"]:
                if key_value_pair["@k"] == "highway":
                    assert assertion in element["tag"]


def test_roundabout_checker():
    # Arrange
    nodes_of_previous_way = way_queries.get_nodes(way_queries_dicts.relation["ways"][0])
    nodes_of_roundabout = way_queries.get_nodes(way_queries_dicts.relation["ways"][1])
    # Act & Assert
    assert way_queries.roundabout_checker(nodes_of_roundabout, nodes_of_previous_way)


def test_check_connectivity():
    # Arrange
    first_way_previous = way_queries.get_start_node(way_queries_dicts.relation["ways"][0])
    last_way_previous = way_queries.get_end_node(way_queries_dicts.relation["ways"][0])
    first_way_current = way_queries.get_start_node(way_queries_dicts.relation["ways"][1])
    last_way_current = way_queries.get_end_node(way_queries_dicts.relation["ways"][1])
    # Act & Assert
    assert way_queries.check_connectivity(first_way_previous, last_way_previous, first_way_current, last_way_current)


def test_get_relation_type():
    assert way_queries.get_relation_type(way_queries_dicts.relation) == "route"
    assert way_queries.get_relation_type(way_queries_dicts.relation2) == ""


def test_get_the_refs_of_ways_in_the_relation():
    assert way_queries.get_the_refs_of_ways_in_the_relation(way_queries_dicts.relation["ways"]) == ['1', '2', '4']


def test_get_network():
    assert way_queries.get_network(way_queries_dicts.relation) == "HU:national"

def test_determine_if_country_has_MUTCD_or_similar():
    result = way_queries.determine_if_country_has_MUTCD_or_similar(way_queries_dicts.relation2)
    assert result is True