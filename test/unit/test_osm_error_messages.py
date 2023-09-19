from src.lib import osm_error_messages
from src.lib.model.previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon
from src.lib.model.error_hwy import ErrorHighway, ErrorMultipolygon

from src.lib.osm_data_parser import convert_multiple_dataclasses_to_dicts
from src.lib.osm_error_messages import remote_relation, remote_way, \
    remote_last_forward_way_ref_nodes_before_backward, remote_node, previous_current_nodes_hwy, \
    previous_current_nodes_multi, return_messages

prev_curr_hwy = PreviousCurrentHighway(first_node_previous="1", last_node_previous="2",
                                       previous_role="forward", previous_roundabout=False,
                                       previous_oneway=False,
                                       first_node_current="3", last_node_current="4",
                                       current_role="", current_roundabout=False,
                                       current_oneway=False,
                                       previous_ref="1", current_ref="2"
                                       )  # this can be anything btw, since we make unit tests
prev_curr_multi = PreviousCurrentMultipolygon(first_node_previous="1", last_node_previous="2",
                                              previous_role="outer", first_node_current="3",
                                              last_node_current="4",
                                              current_role="inner")  # same for here
error_information_list_no_dict_conversion_hwy = [ErrorHighway(prev_curr_hwy, "Gap")]
error_information_list_hwy = convert_multiple_dataclasses_to_dicts(
    error_information_list_no_dict_conversion_hwy)
error_information_list_no_dict_conversion_multi = [
    ErrorMultipolygon(prev_curr_multi, "Gap in multipolygon")]
error_information_list_multi = convert_multiple_dataclasses_to_dicts(
    error_information_list_no_dict_conversion_multi)
nodes_with_link = (
    "Previous way's first and last nodes: https://osm.org/node/1 and https://osm.org/node/2 \n"
    "Role: forward \n"
    "Roundabout: False \n"
    "One way road: False \n"
    "Current way's first and last nodes: https://osm.org/node/3 and https://osm.org/node/4 \n"
    "Role:  \n"
    "Roundabout: False \n"
    "One way road: False \n")
nodes_without_link = ("Previous way's first and last nodes: 1 and 2 \n"
                      "Role: forward \n"
                      "Roundabout: False \n"
                      "One way road: False \n"
                      "Current way's first and last nodes: 3 and 4 \n"
                      "Role:  \n"
                      "Roundabout: False \n"
                      "One way road: False \n")
nodes_multi_with_link = (
    "Previous way's first and last nodes: https://osm.org/node/1 and https://osm.org/node/2 \n"
    "Role: outer \n"
    "Current way's first and last nodes: https://osm.org/node/3 and https://osm.org/node/4 \n"
    "Role: inner \n")
nodes_multi_without_link = ("Previous way's first and last nodes: 1 and 2 \n"
                            "Role: outer \n"
                            "Current way's first and last nodes: 3 and 4 \n"
                            "Role: inner \n")


def test_remote_relation():
    relation_id = 23099
    not_from_api = False
    from_api = True
    when_source_has_nothing = remote_relation(relation_id, not_from_api)
    when_source_has_content = remote_relation(relation_id, from_api)
    assert when_source_has_content == "https://osm.org/relation/23099"
    assert when_source_has_nothing == 23099


def test_remote_way():
    way_id = 1
    not_from_api = False
    from_api = True
    when_source_has_nothing = remote_way(way_id, not_from_api)
    when_source_has_content = remote_way(way_id, from_api)
    assert when_source_has_content == "https://osm.org/way/1"
    assert when_source_has_nothing == 1


def test_remote_last_forward_way_before_backward_direction():
    array = ["-1", ["-1", "-2"]]  # since the array usually has 2 items
    not_from_api = False
    from_api = True
    # Act
    result_empty = remote_last_forward_way_ref_nodes_before_backward(array, not_from_api)
    result_content = remote_last_forward_way_ref_nodes_before_backward(array, from_api)

    assert result_content == "https://osm.org/way/-1"
    assert result_empty == array[0]


def test_remote_node():
    node_id = 1
    not_from_api = False
    from_api = True
    when_source_has_nothing = remote_node(node_id, not_from_api)
    when_source_has_content = remote_node(node_id, from_api)
    assert when_source_has_content == "https://osm.org/node/1"
    assert when_source_has_nothing == 1


def test_previous_current_nodes_hwy():
    # Arrange is done at the top of the .py file (prev_curr_hwy)
    # Act
    not_from_api = False
    from_api = True
    result_string_link = previous_current_nodes_hwy(error_information_list_hwy[0]["prev_curr"],
                                                    from_api)
    result_string_no_link = previous_current_nodes_hwy(error_information_list_hwy[0]["prev_curr"],
                                                       not_from_api)
    assert result_string_link == nodes_with_link
    assert result_string_no_link == nodes_without_link


def test_previous_current_nodes_multi():
    # Arrange is done at the top of the .py file (prev_curr_hwy)
    # Act
    not_from_api = False
    from_api = True
    result_string_link = previous_current_nodes_multi(error_information_list_multi[0]["prev_curr"],
                                                      from_api)
    result_string_no_link = previous_current_nodes_multi(
        error_information_list_multi[0]["prev_curr"],
        not_from_api)
    assert result_string_link == nodes_multi_with_link
    assert result_string_no_link == nodes_multi_without_link


def test_return_messages_not_verbose():
    correct_ways_count = 2
    errors_to_decrease = 0
    relation_id = "23099"
    verbose = False
    is_from_api = True
    result = return_messages(error_information_list_no_dict_conversion_hwy, correct_ways_count,
                             errors_to_decrease,
                             relation_id, is_from_api,
                             verbose)
    assert result == [f"=================[Relation #{relation_id}]=================",
                      f"Link of the relation: https://osm.org/relation/{relation_id}",
                      "To download the XML file: https://www.openstreetmap.org/api/0.6/relation/"
                      f"{relation_id}/full",
                      f"This relation has {len(error_information_list_no_dict_conversion_hwy)}"
                      f" errors and {correct_ways_count} correct ways. "
                      "That's 66.67% correct."]


def test_return_messages_verbose_all_errors_hwy():
    correct_ways_count = 2
    errors_to_decrease = 0
    relation_id = "1"
    verbose = True
    is_from_api = True
    error_messages_all_errors = [ErrorHighway(prev_curr_hwy, "Gap"),
                                 ErrorHighway(prev_curr_hwy, "Gap at the beginning"),
                                 ErrorHighway(prev_curr_hwy, "Split roundabout"),
                                 ErrorHighway(prev_curr_hwy, "Forward but not oneway"),
                                 ErrorHighway(prev_curr_hwy, "Wrong role setup"),
                                 ErrorHighway(prev_curr_hwy, "Roundabout gap"),
                                 ErrorHighway(prev_curr_hwy, "Gap in forward series"),
                                 ErrorHighway(prev_curr_hwy,
                                              "Only one forward way before closed roundabout"),
                                 ErrorHighway(prev_curr_hwy,
                                              "Wrong order of roundabout entries"),
                                 ErrorHighway(prev_curr_hwy,
                                              "Duplicated roundabout ways"),
                                 ErrorHighway(prev_curr_hwy,
                                              "Forward role missing at roundabout"),
                                 ErrorHighway(prev_curr_hwy,
                                              "Forward and non-oneway without ability to move"
                                              " backward"),
                                 ErrorHighway(prev_curr_hwy, "Motorway not split"),
                                 ErrorHighway(prev_curr_hwy, "Not supported")]
    result_all_hwy = return_messages(error_messages_all_errors, correct_ways_count,
                                     errors_to_decrease, relation_id,
                                     is_from_api,
                                     verbose)
    assert result_all_hwy[3] == (
        f"\n[ERROR] Relation with route number {prev_curr_hwy.currently_checked_ref} "
        f"has gap at way: https://osm.org/way/{prev_curr_hwy.current_ref} \n"
        f"{nodes_with_link}")
    remote_last_forward_way_ref_nodes_before_backward_result = \
        osm_error_messages.remote_last_forward_way_ref_nodes_before_backward(
            prev_curr_hwy.last_forward_way_ref_nodes_before_backward, is_from_api)
    assert result_all_hwy[4] == (
        f"\n[ERROR] Relation with route number {prev_curr_hwy.currently_checked_ref}"
        f" has gap at way: https://osm.org/way/{prev_curr_hwy.current_ref} \n"
        "This case occured because there is a gap,"
        "this happened at the beginning of the "
        "relation, since it started with a 2x2 seperated highway. "
        "The ID of last way before going to backward direction: "
        f"{remote_last_forward_way_ref_nodes_before_backward_result} \n{nodes_with_link}")
    assert result_all_hwy[5] == (f"\nINFO: There is a roundabout split up to multiple ways, "
                                 f"last known way is "
                                 f"https://osm.org/way/{prev_curr_hwy.current_ref} \n"
                                 f"{nodes_with_link}")
    assert result_all_hwy[6] == ("\n[ERROR] Relation with route number "
                                 f"{prev_curr_hwy.currently_checked_ref} has a road segment which "
                                 "has forward role, but not oneway and the following road segment "
                                 f"is a normal road segment, way number where this was found: "
                                 f"https://osm.org/way/{prev_curr_hwy.current_ref} \n"
                                 f"Previous way: https://osm.org/way/{prev_curr_hwy.previous_ref}\n"
                                 f"{nodes_with_link}")
    assert result_all_hwy[7] == ("\n[ERROR] Relation with route number "
                                 f"{prev_curr_hwy.currently_checked_ref}"
                                 f" has wrong role setup at way:"
                                 f" https://osm.org/way/{prev_curr_hwy.current_ref}\n"
                                 f"{nodes_with_link}")
    assert result_all_hwy[8] == ("\n[ERROR] Relation with route number "
                                 f"{prev_curr_hwy.currently_checked_ref} has gap at roundabout:"
                                 f" https://osm.org/way/{prev_curr_hwy.current_ref}"
                                 f"\n{nodes_with_link}")
    assert result_all_hwy[9] == ("\n[ERROR] Relation with route number "
                                 f"{prev_curr_hwy.currently_checked_ref} has gap at way:"
                                 f" https://osm.org/way/{prev_curr_hwy.current_ref} \n"
                                 "It's found in a series of ways with forward role.\n"
                                 f"{nodes_with_link}")
    assert result_all_hwy[10] == ("\n[ERROR] Relation with route number "
                                 f"{prev_curr_hwy.currently_checked_ref} has gap at way:"
                                 f" https://osm.org/way/{prev_curr_hwy.current_ref} \n"
                                 "There is only one connecting way into the closed "
                                 "(its start and end nodes are the same) roundabout"
                                 " instead of two.\n"
                                 f"{nodes_with_link}")
    assert result_all_hwy[11] == ("\n[ERROR] Relation with route number "
                                  f"{prev_curr_hwy.currently_checked_ref} has the way"
                                  f" https://osm.org/way/{prev_curr_hwy.current_ref} "
                                  "earlier than needed, it's a roundabout entry node and "
                                  "it should be swapped in order to maintain the continuity. \n"
                                  f"{nodes_with_link}")
    assert result_all_hwy[12] == ("\n[ERROR] Relation with route number "
                                  f"{prev_curr_hwy.currently_checked_ref} has the way"
                                  f" https://osm.org/way/{prev_curr_hwy.current_ref} "
                                  "roundabout way duplicated, this is wrong, "
                                  "since the route only contains the roundabout once. \n"
                                  f"{nodes_with_link}")
    assert result_all_hwy[13] == ("\n[ERROR] Relation with route number "
                                  f"{prev_curr_hwy.currently_checked_ref} has a roundabout"
                                  f" https://osm.org/way/{prev_curr_hwy.current_ref}"
                                  " with forward role missing. \n"
                                  f"{nodes_with_link}")
    assert result_all_hwy[14] == ("\n[ERROR] Relation with route number "
                                  f"{prev_curr_hwy.currently_checked_ref} has a forward road"
                                  f" piece or series,"
                                  f"previous ref which is one of the affected:"
                                  f" https://osm.org/way/{prev_curr_hwy.previous_ref} \n"
                                  "This is not good, because in some cases like"
                                  " 2x1 lane trunk/motorways "
                                  "the traffic can't traverse in the backwards direction."
                                  f"{nodes_with_link}")
    assert result_all_hwy[15] == (
        "\n[WARNING] The motorway is continuous, however it reached back from start point to"
        " (almost) start point via other lane. It should be done that the motorway's right"
        " lane goes first to the end point, then left lane from first to end point.")
    assert result_all_hwy[16] == "This public transportation relation type is not supported."


def test_return_messages_verbose_all_errors_multi():
    correct_ways_count = 2
    errors_to_decrease = 0
    relation_id = "1"
    verbose = True
    is_from_api = True
    error_messages_all_errors = [
        ErrorMultipolygon(prev_curr_multi, "Gap in an area consisting of one way"),
        ErrorMultipolygon(prev_curr_multi,
                          "Gap in an area consisting of one way at the end"),
        ErrorMultipolygon(prev_curr_multi, "Gap in multi way multipolygon at the end"),
        ErrorMultipolygon(prev_curr_multi, "Gap in multi way multipolygon"),
        ErrorMultipolygon(prev_curr_multi, "No role")
    ]
    result_all_multi = return_messages(error_messages_all_errors, correct_ways_count,
                                       errors_to_decrease, relation_id, is_from_api, verbose)
    assert result_all_multi[3] == ("\n[ERROR] Multipolygon"
                                   " has an area consisting of one way unclosed,"
                                   f" the way affected:"
                                   f" https://osm.org/way/{prev_curr_multi.current_ref}\n"
                                   f"\n{nodes_multi_with_link}")
    assert result_all_multi[4] == ("\n[ERROR] Multipolygon has an area consisting"
                                   " of one way unclosed at the end of the relation, "
                                   "the way affected:"
                                   f" https://osm.org/way/{prev_curr_multi.current_ref}\n"
                                   f"\n{nodes_multi_with_link}")
    assert result_all_multi[5] == ("\n[ERROR] Multipolygon"
                                   " has an area consisting of multiple ways unclosed at the end"
                                   " of the relation, the way affected: "
                                   f"https://osm.org/way/{prev_curr_multi.current_ref}\n"
                                   f"\n{nodes_multi_with_link}")
    assert result_all_multi[6] == ("\n[ERROR] Multipolygon"
                                   " has an area consisting of multiple ways unclosed, the way "
                                   "affected:"
                                   f" https://osm.org/way/{prev_curr_multi.current_ref}\n"
                                   f"\n{nodes_multi_with_link}")
    assert result_all_multi[7] == ("\n[ERROR] Multipolygon"
                                   " has a way which doesn't have a role, the way affected:"
                                   f" https://osm.org/way/{prev_curr_multi.current_ref}\n"
                                   f"\n{nodes_multi_with_link}")


def test_return_message_no_error():
    results_no_error = return_messages([], 1,  0, "23099", True, False)
    assert results_no_error[3] == "This relation has no errors and gaps at all."
