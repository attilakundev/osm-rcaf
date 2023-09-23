#!/usr/bin/python3
from src.lib import way_queries
from src.test.files import way_queries_dicts
from src.test.files import osm_data_parser_dicts


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
    way_queries.remove_tag(way_queries_dicts.relation["ways"][0], "oneway")
    way_queries.remove_tag(osm_data_parser_dicts.relation_info_result_appended["ways"][0], "oneway")
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


def test_put_ref_from_relation_to_highway_way():
    #Hey, this function is not implemented yet into
    # the fixer. would you mind implementing it?
    # Arrange
    assertion = {
        "@k": "ref",
        "@v": 710
    }
    # Act
    way_queries.put_ref_from_relation_to_highway_way(way_queries_dicts.relation)
    # Assert - this will be a for loop since we check the entire way_queries_dicts.relation
    # of highways
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
    assert way_queries.check_connectivity(first_way_previous, last_way_previous, first_way_current,
                                          last_way_current)


def test_get_relation_type():
    assert way_queries.get_relation_type(way_queries_dicts.relation) == "route"
    assert way_queries.get_relation_type(way_queries_dicts.relation2) == ""


def test_get_network():
    assert way_queries.get_network(way_queries_dicts.relation) == "HU:national"


def test_determine_if_country_has_mutcd_or_similar():
    result = way_queries.determine_if_country_has_MUTCD_or_similar(way_queries_dicts.relation2)
    assert result is True


def test_get_relation_member_type():
    data = {}
    result = way_queries.get_relation_member_type(data)
    assert result == ""


def test_get_index_of_way():
    array = [{"@ref": "0"}]
    result = way_queries.get_index_of_way(array, "-1")
    assert result == -1

def test_get_coordinates_of_nodes():
    data = {"nodes": [{"@lat": "1", "@lon": "1"},{"@lat": "2", "@lon": "2"}]}
    result = way_queries.get_coordinates_of_nodes(data)
    assert result == [["1","1"],["2","2"]]

def test_get_relation_from_list():
    # the dictionary version can be found at test_compare.py where there is only one relation.
    relation_id = "10"
    data = {
        "osm":{
            "relation":[
                {
                    "@id": "1",
                    "member": [{"@ref": "1"},
                               {"@ref": "2"}]
                },
                {
                    "@id": "10",
                    "member": [{"@ref": "3"},
                               {"@ref": "4"}]

                }
            ]
        }
    }
    given_relation = way_queries.get_relation(relation_id,data)
    assert given_relation["@id"] == relation_id
    assert len(given_relation["member"]) == 2