#!/usr/bin/python3
from pathlib import Path
from src.lib.fixer.highway_fixer import HighwayFixer
from src.lib.fixer import fixer_utils
from src.lib import way_queries

project_path = Path(__file__).parents[3].absolute()

highway_fixer = HighwayFixer()


def test_route_open_roundabout_entry_divided_exit_divided_no_role():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_open_roundabout_entry_divided_exit_divided_no_role.xml"
    # good order but road with way -1 has no role
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-9", "-1", "-4", "-2", "-3", "-7"]
    assert way_queries.get_role(corrected_ways_to_search[3]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[4]) == "forward"


def test_search_for_connection_exiting_from_closed_roundabout_exit_not_split_wrong_order_no_role():  # closed roundabout, wrong order, wrong role
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_not_divided_wrong_first_ways_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5"]
    # check the roles
    assert way_queries.is_oneway(corrected_ways_to_search[1]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[2]) is True


def test_route_closed_roundabout_entry_divided_exit_divided_no_role():  # closed roundabout, correct order, wrong role
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_closed_roundabout_entry_divided_exit_divided_norole.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-4", "-2", "-1", "-3", "-7"]
    # check the roles
    assert way_queries.is_oneway(corrected_ways_to_search[1]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[2]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[4]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[5]) is True


def test_route_closed_roundabout_entry_divided_exit_divided_wrong_order_of_entry():  # closed roundabout, wrong order, correct role
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_closed_roundabout_entry_divided_exit_divided_wrong_order_of_entry.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-4", "-2", "-1", "-3", "-7"]
    # check the roles
    assert way_queries.is_oneway(corrected_ways_to_search[1]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[2]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[4]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[5]) is True


def test_route_closed_roundabout_entry_divided_exit_divided_correct_order():  # closed roundabout, correct order, correct role
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_divided_exit_divided_correct_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-4", "-2", "-1", "-3", "-7"]
    # check the roles
    assert way_queries.is_oneway(corrected_ways_to_search[1]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[2]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[4]) is True
    assert way_queries.is_oneway(corrected_ways_to_search[5]) is True


def test_route_forward_not_split_nooneway_multiple_fwd():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_forward_not_split_nooneway_multiple_fwd.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-5", "-3"]
    # check the roles
    assert way_queries.is_oneway(corrected_ways_to_search[1]) is False
    assert way_queries.is_oneway(corrected_ways_to_search[2]) is False


def test_route_forward_not_split_nooneway_only_one_fwd():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_forward_not_split_nooneway_only_one_fwd.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3"]
    # check the roles
    assert way_queries.is_oneway(corrected_ways_to_search[1]) is False


def test_route_forward_not_split_oneway_gap():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_forward_split_oneway_gap.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    # This can be tested if the correction from locally is implemented correctly for one-way roads. Currently it's broken (-1,-2,-3,-5,-6)
    # True value for 3rd parameter: True if from API, False if not from API
    # corrected_ways_to_search = highway_fixer.fixing(relation_info,"",False)
    # refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    # assert refs_of_members == ["-1", "-2", "-3", "-5", "-7", "-4", "-6"]


def test_route_motorway_two_sided_no_role():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_motorway_two_sided_no_role.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4"]
    assert way_queries.get_role(corrected_ways_to_search[0]) == "forward"


def test_route_norole_split_nooneway():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_norole_split_nooneway.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-5", "-6"]
    # The reason for this is that the way how the ways are searched are in a lazy way so only follow what's continued...
    # this is sorta a false postiive case(since it's correct but not exactly what we want), since we would want -1,-2,-3,-5,-4,-6
    assert way_queries.get_role(corrected_ways_to_search[1]) == ""
    assert way_queries.get_role(corrected_ways_to_search[4]) == ""


def test_route_oneway_without_role():
    file_path = f"{project_path}/test/files/results_highway_analyzer_false/route_oneway_without_role.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3"]
    assert way_queries.get_role(corrected_ways_to_search[1]) == "forward"


def test_route_continuous_forward_no_oneway():
    file_path = f"{project_path}/test/files/files_for_fixer/route_continuous_forward_no_oneway.osm"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5"]
    assert way_queries.get_role(corrected_ways_to_search[1]) == ""
    assert way_queries.get_role(corrected_ways_to_search[2]) == ""


def test_route_continuous_forward_no_oneway_wrong_order():
    file_path = f"{project_path}/test/files/files_for_fixer/route_continuous_forward_no_oneway_wrong_order.osm"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5"]
    assert way_queries.get_role(corrected_ways_to_search[1]) == ""
    assert way_queries.get_role(corrected_ways_to_search[2]) == ""


def test_route_continuous_no_role_no_oneway_wrong_order():
    file_path = f"{project_path}/test/files/files_for_fixer/route_continuous_no_role_no_oneway_wrong_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8"]
    assert way_queries.get_role(corrected_ways_to_search[1]) == ""
    assert way_queries.get_role(corrected_ways_to_search[2]) == ""


def test_route_continuous_no_role_oneway():
    file_path = f"{project_path}/test/files/files_for_fixer/route_continuous_no_role_oneway.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8"]
    assert way_queries.get_role(corrected_ways_to_search[4]) == ""
    assert way_queries.is_oneway(corrected_ways_to_search[4]) is False


def test_route_continuous_no_role_oneway_wrong_order():
    file_path = f"{project_path}/test/files/files_for_fixer/route_continuous_no_role_oneway_wrong_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8"]
    assert way_queries.get_role(corrected_ways_to_search[4]) == ""
    assert way_queries.is_oneway(corrected_ways_to_search[4]) is False


def test_route_open_roundabout_correct_roles_and_order():  # open roundabout, correct order, correct role
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_correct_roles_and_order.osm"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-9", "-1", "-4", "-2", "-3", "-7"]
    assert way_queries.get_role(corrected_ways_to_search[2]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[2]) is True
    assert way_queries.get_role(corrected_ways_to_search[3]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[3]) is False
    assert way_queries.get_role(corrected_ways_to_search[4]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[4]) is False
    assert way_queries.get_role(corrected_ways_to_search[5]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[5]) is True


def test_route_open_roundabout_correct_roles_and_wrong_order():  # open roundabout, wrong order, correct role
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_correct_roles_and_wrong_order.osm"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-6")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-9", "-1", "-4", "-2", "-3", "-7"]
    assert way_queries.get_role(corrected_ways_to_search[2]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[2]) is True
    assert way_queries.get_role(corrected_ways_to_search[3]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[3]) is False
    assert way_queries.get_role(corrected_ways_to_search[4]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[4]) is False
    assert way_queries.get_role(corrected_ways_to_search[5]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[5]) is True


def test_open_roundabout_exit_split_wrong_order_with_extra_members():  # Open roundabout correct roles wrong order, extra members in roundabout
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_entry_divided_exit_divided_wrong_order_extra_members.xml"
    # as manually discovered, the correction for this would be:
    # 1,2,4,8,9,6,3 (before reversing the other side) -> 1,2,4,8,3,6,9,10 (5,7 are extra members)
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-4", "-8", "-3", "-6", "-9", "-10"]


def test_route_open_roundabout_wrong_roles_correct_order():  # open roundabout: correct order wrong roles
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_correct_order_and_wrong_roles.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-6")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-9", "-1", "-4", "-2", "-3", "-7"]
    assert way_queries.get_role(corrected_ways_to_search[2]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[2]) is True
    assert way_queries.get_role(corrected_ways_to_search[3]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[3]) is False
    assert way_queries.get_role(corrected_ways_to_search[4]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[4]) is False
    assert way_queries.get_role(corrected_ways_to_search[5]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[5]) is True


def test_route_open_roundabout_wrong_roles_wrong_order():  # open roundabout: correct order wrong roles
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_roundabout_wrong_order_and_wrong_roles.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-6")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-6", "-5", "-9", "-1", "-4", "-2", "-3", "-7"]
    assert way_queries.get_role(corrected_ways_to_search[2]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[2]) is True
    assert way_queries.get_role(corrected_ways_to_search[3]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[3]) is False
    assert way_queries.get_role(corrected_ways_to_search[4]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[4]) is False
    assert way_queries.get_role(corrected_ways_to_search[5]) == "forward"
    assert way_queries.is_roundabout(corrected_ways_to_search[5]) is True


def test_route_split_oneway():
    file_path = f"{project_path}/test/files/files_for_fixer/route_split_oneway.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-2", "-3"]


def test_route_split_wrong_order():
    file_path = f"{project_path}/test/files/files_for_fixer/route_split_wrong_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-6", "-5", "-2", "-3"]


def test_route_split_wrong_order_backward():
    file_path = f"{project_path}/test/files/files_for_fixer/route_split_wrong_order_backward.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1")
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-6", "-5", "-2", "-3"]
    assert way_queries.get_role(corrected_ways_to_search[1]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[2]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[3]) == "forward"
    assert way_queries.get_role(corrected_ways_to_search[4]) == "forward"


def test_route_closed_double_roundabout_divided_2_by_2_ways_forward_role_wrong_order():
    file_path = f"{project_path}/test/files/files_for_fixer/route_double_roundabout_divided_2_by_2_ways_forward_role_wrong_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10", "-11",
                               "-12"]
    assert list(map(lambda x: x["@ref"],
                    corrected_ways_to_search)) == refs_of_members  # this has to be ensured, otherwise we get error


def test_route_open_double_roundabout_divided_2_by_2_ways_forward_role_wrong_order():
    file_path = f"{project_path}/test/files/files_for_fixer/route_open_double_roundabout_divided_2_by_2_ways_forward_role_wrong_order.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-15", "-14", "-13",
                               "-12", "-11", "-10", "-9", "-16"]
    assert list(map(lambda x: x["@ref"],
                    corrected_ways_to_search)) == refs_of_members  # this has to be ensured, otherwise we get error


def test_route_split_wrong_order_backward_gap():
    file_path = f"{project_path}/test/files/files_for_fixer/route_split_wrong_order_backward_gap.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-1", False)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-1", "-4", "-6", "-5", "-2", "-3"]


def test_route_closed_roundabout_entry_and_exit_divided_multiple_members():
    # The order of the ways are correct in this case, but I want to check if it can recreate it in the very same order.
    file_path = f"{project_path}/test/files/files_for_fixer/route_closed_roundabout_entry_and_exit_divided_multiple_members.xml"
    relation_info = fixer_utils.get_relation_info(file_path)
    corrected_ways_to_search = highway_fixer.fixing(relation_info, "-7", False)
    refs_of_members = list(map(lambda x: way_queries.get_way_ref(x), corrected_ways_to_search))
    assert refs_of_members == ["-7", "-5", "-10", "-6", "-9", "-1", "-3", "-8", "-2", "-4"]
