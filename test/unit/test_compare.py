import pytest

from src.lib import compare


def setup():
    old_data = {
        "osm": {
            "relation": {
                "@id": "1",
                "member": [{"@ref": 1, "@role": ""},
                            {"@ref": 3, "@role": ""},
                            {"@ref": 2, "@role": ""},
                            {"@ref": 4, "@role": "forward"}]
            }
        }
    }

    new_data = {
        "osm": {
            "relation": {
                "@id": "1",
                "member": [{"@ref": 1, "@role": ""},
                            {"@ref": 2, "@role": ""},
                            {"@ref": 3, "@role": ""}]
            }
        }
    }
    return old_data, new_data

def setup_one_member():
    old_data = {
        "osm": {
            "relation": {
                "@id": "1",
                "member": {"@ref": 1, "@role": ""}
            }
        }
    }

    new_data = {
        "osm": {
            "relation": {
                "@id": "1",
                "member": {"@ref": 1, "@role": ""}
            }
        }
    }

    return old_data, new_data

def test_compare_two_relation_data():
    # GIVEN
    old_data, new_data = setup()
    relation_id = 1
    # WHEN
    changes, deletions = compare.compare_two_relation_data(old_data, new_data, relation_id)
    # THEN
    assert changes[0]["old_id"] == 3
    assert changes[0]["new_id"] == 2
    assert deletions[0]["old_id"] == 4
    assert deletions[0]["old_role"] == "forward"

def test_compare_two_relation_data_one_member():
    # GIVEN
    old_data, new_data = setup_one_member()
    relation_id = 1
    # WHEN
    changes, deletions = compare.compare_two_relation_data(old_data, new_data, relation_id)
    # THEN
    assert len(changes) == 0
    assert len(deletions) == 0

def test_compare_type_error(caplog):
    #GIVEN
    old_data = []
    new_data = []
    relation_id = 1
    # WHEN
    compare.compare_two_relation_data(old_data, new_data, relation_id)
    #THEN
    assert "list indices must be integers" in caplog.text