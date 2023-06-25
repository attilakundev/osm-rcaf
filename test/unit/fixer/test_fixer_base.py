import sys
import xmltodict
from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/analyzer")
sys.path.append(f"{project_path}/lib/fixer")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from analyzer import Analyzer
from fixer import RelationFixer
from fixer_base import FixerBase
import way_queries

analyzer = Analyzer()
fixer = RelationFixer()

def test_route_split_wrong_order_backward_gap_with_correctly_returned_data():
    file = open(f"{project_path}/test/files/files_for_fixer/route_split_wrong_order_backward_gap.xml", "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search = fixer.fixing(relation_info, "-1",False)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-6", "-5", "-2", "-3"]
    relation_data = fixer.detect_differences_in_original_and_repaired_relation_and_return_relation_dictionary_accordingly(data,relation_info, corrected_ways_to_search)
    assert "@action" in relation_data["osm"]["relation"] and relation_data["osm"]["relation"]["@action"] == "modify"
    assert "@action" in relation_data["osm"]["way"][1] and relation_data["osm"]["way"][1]["@action"] == "modify"

def test_relation_67157():
    file = open(f"{project_path}/test/files/67157.xml", encoding="utf8").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search = fixer.fixing(relation_info, first_way="4293039",is_from_api=False)
    corrected_ways_to_search = fixer.correct_way_roles_tags(relation_info,corrected_ways_to_search)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members[0] == "4293039"
    assert refs_of_members[-1] == "571346755"
    assert way_queries.get_role(corrected_ways_to_search[2]) == ""
    assert way_queries.get_role(corrected_ways_to_search[-1]) == "forward"

def test_fixing_abstract_method():
    FixerBase.__abstractmethods__ = set()
    dummy_fixer_base = FixerBase()
    fixing = dummy_fixer_base.fixing(None)
    assert fixing is None

def test_detect_differences_in_original_and_repaired_relation_and_return_relation_dictionary_accordingly():
    file = open(f"{project_path}/test/files/simplest_way.xml", encoding="utf8").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search= fixer.fixing(relation_info,first_way="-1", is_from_api=False)
    data = fixer.detect_differences_in_original_and_repaired_relation_and_return_relation_dictionary_accordingly(data,relation_info,corrected_ways_to_search)
    assert type(data["osm"]["way"]) == dict



