import pytest
import sys
import src.lib.way_queries as way_queries
from pathlib import Path

project_path = Path(__file__).parent.parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")

relation = {
    "ways": [
        {
            "@ref": "1",
            "@role": "",
            "@type": "way",
            "attributes": {
                "@id": "1"
            },
            "nd": [
                {
                    "@ref": 1
                },
                {
                    "@ref": 2
                },
                {
                    "@ref": 3
                }
            ],
            "tag": [
                {
                    "@k": "highway",
                    "@v": "primary"
                },
                {
                    "@k": "railway",
                    "@v": "rail"
                },
                {
                    "@k": "oneway",
                    "@v": "yes"
                },
                {
                    "@k": "junction",
                    "@v": "roundabout"
                },
            ]
        },
        {
            "@ref": "2",
            "@role": "",
            "@type": "way",
            "attributes": {
                "@id": "1"
            },
            "nd": [
                {
                    "@ref": 3
                },
                {
                    "@ref": 4
                },
                {
                    "@ref": 5
                },
                {
                    "@ref": 6
                },
                {
                    "@ref": 3
                }
            ],
            "tag": [
                {
                    "@k": "highway",
                    "@v": "primary"
                },
                {
                    "@k": "railway",
                    "@v": "rail"
                },
                {
                    "@k": "oneway",
                    "@v": "yes"
                },
                {
                    "@k": "junction",
                    "@v": "roundabout"
                },
            ]
        }
    ],
    "ref": 710
}


def test_get_nodes():
    # Arrange is done at the beginning
    # Act
    nodes = way_queries.get_nodes(relation["ways"][0])
    # Assert
    assert nodes == [1, 2, 3]


def test_start_node():
    # Arrange is done at the beginning
    # Act
    first_node = way_queries.get_start_node(relation["ways"][0])
    # Assert
    assert first_node == 1


def test_end_node():
    # Arrange is done at the beginning
    # Act
    last_node = way_queries.get_end_node(relation["ways"][0])
    # Assert
    assert last_node == 3


def test_is_roundabout():
    # Arrange is done at the beginning
    # Act
    roundabout = way_queries.is_roundabout(relation["ways"][0])
    # Assert
    assert roundabout


def test_is_oneway():
    # Arrange is done at the beginning
    # Act
    oneway = way_queries.is_oneway(relation["ways"][0])
    # Assert
    assert oneway


def test_remove_tag():
    # Arrange is done at the beginning
    # Act
    way_queries.remove_tag(relation["ways"][0], "oneway", "yes")
    # Assert
    assert relation["ways"][0]["tag"] == [{
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


def test_modify_role():
    way_queries.modify_role(relation["ways"][0], "backward")
    assert relation["ways"][0]["@role"] == "backward"


def test_get_ref_of_the_route():
    # Arrange is done at the beginning
    # Act
    ref = way_queries.get_ref_of_the_route(relation)
    # Assert
    assert ref == 710


def test_get_id_of_the_relation_members():
    # Arrange is done at the beginning
    # Act
    refs = way_queries.get_id_of_the_relation_members(relation["ways"])
    # Assert
    assert refs == ['1', '2']


def test_put_ref_from_relation_to_highway_way():
    # Arrange
    assertion = {
        "@k": "ref",
        "@v": 710
    }
    # Act
    way_queries.put_ref_from_relation_to_highway_way(relation)
    # Assert - this will be a for loop since we check the entire relation of highways
    for index, way in enumerate(relation["ways"]):
        for key_value_pair in way["tag"]:
            if key_value_pair["@k"] == "highway":
                assert assertion in way["tag"]


def test_roundabout_checker():
    nodes_of_previous_way = way_queries.get_nodes(relation["ways"][0])
    nodes_of_roundabout = way_queries.get_nodes(relation["ways"][1])
    assert way_queries.roundabout_checker(nodes_of_roundabout, nodes_of_previous_way)


def test_check_connectivity():
    first_way_previous = way_queries.get_start_node(relation["ways"][0])
    last_way_previous = way_queries.get_end_node(relation["ways"][0])
    first_way_current = way_queries.get_start_node(relation["ways"][1])
    last_way_current = way_queries.get_end_node(relation["ways"][1])
    assert way_queries.check_connectivity(first_way_previous, last_way_previous, first_way_current, last_way_current)


if __name__ == '__main__':
    pytest.main([f"f{project_path}/test/test_way.py"])
