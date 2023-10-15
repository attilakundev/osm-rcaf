import xmltodict
from pathlib import Path
from src.lib.analyzer.analyzer import Analyzer
from src.lib.fixer.fixer import RelationFixer
from src.lib.fixer.fixer_base import FixerBase
from src.lib import way_queries

project_path = Path(__file__).parents[3].absolute()

analyzer = Analyzer()
fixer = RelationFixer()


def test_route_split_wrong_order_backward_gap_with_correctly_returned_data():
    file = open(
        f"{project_path}/test/files/files_for_fixer/route_split_wrong_order_backward_gap.xml",
        "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search = fixer.fixing(relation_info, "-1", False)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-6", "-5", "-2", "-3"]
    relation_data = fixer. \
        detect_differences_in_original_and_repaired_relation(data, relation_info,
                                                             corrected_ways_to_search)
    assert "@action" in relation_data["osm"]["relation"] and relation_data["osm"]["relation"][
        "@action"] == "modify"
    assert "@action" in relation_data["osm"]["way"][1] and relation_data["osm"]["way"][1][
        "@action"] == "modify"


def test_relation_67157_route_67():
    file = open(f"{project_path}/test/files/67157.xml", encoding="utf8").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search = fixer.fixing(relation_info, first_way="4293039", is_from_api=False)
    corrected_ways_to_search = fixer.correct_way_roles_tags(relation_info, corrected_ways_to_search)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members[0] == "4293039"
    assert refs_of_members[-1] == "571346755"
    assert way_queries.get_role(corrected_ways_to_search[2]) == ""
    assert way_queries.get_role(corrected_ways_to_search[-1]) == "forward"

def not_working_test_relation_6280352_route_4():
    file = open(f"{project_path}/test/files/6280352.xml", encoding="utf8").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search = fixer.fixing(relation_info, first_way="1156348391", is_from_api=False)
    corrected_ways_to_search = fixer.correct_way_roles_tags(relation_info, corrected_ways_to_search)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members[0] == "1156348391"
    assert refs_of_members[-1] == "27792544"
    assert way_queries.is_oneway(corrected_ways_to_search[0])
    assert way_queries.get_role(corrected_ways_to_search[-1]) == ""
def test_fixing_abstract_method():
    FixerBase.__abstractmethods__ = set()
    dummy_fixer_base = FixerBase()
    fixing = dummy_fixer_base.fixing({})
    assert fixing is None


def test_detect_differences_in_original_and_repaired_relation():
    file = open(f"{project_path}/test/files/simplest_way.xml", encoding="utf8").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    corrected_ways_to_search = fixer.fixing(relation_info, first_way="-1", is_from_api=False)
    data = fixer.detect_differences_in_original_and_repaired_relation(data, relation_info,
                                                                      corrected_ways_to_search)
    assert type(data["osm"]["way"]) == dict
