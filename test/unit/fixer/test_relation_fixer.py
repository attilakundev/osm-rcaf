import sys
from pathlib import Path

NOT_SUPPORTED = "not supported"

NOT_IMPLEMENTED_YET = "Not implemented yet"

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/fixer")
from fixer import RelationFixer
fixer = RelationFixer()

def test_railway_fixer_not_implemented():
    relation_info = {
        "type": "route",
        "route": "railway"
    }
    result = fixer.fixing(relation_info)
    correct_roles_result = fixer.correct_way_roles_tags(relation_info, None)
    assert NOT_IMPLEMENTED_YET in result["Error"]
    assert NOT_IMPLEMENTED_YET in correct_roles_result["Error"]

def test_multipolygon_fixer_not_implemented():
    relation_info = {
        "type": "multipolygon"
    }
    result= fixer.fixing(relation_info)
    correct_roles_result = fixer.correct_way_roles_tags(relation_info, None)
    assert NOT_IMPLEMENTED_YET in result["Error"]
    assert NOT_IMPLEMENTED_YET in correct_roles_result["Error"]

def test_public_transport_fixer_not_implemented():
    relation_info = {
        "type": "public_transport"
    }
    result= fixer.fixing(relation_info)
    correct_roles_result = fixer.correct_way_roles_tags(relation_info, None)
    assert NOT_SUPPORTED in result["Error"]
    assert NOT_SUPPORTED in correct_roles_result["Error"]