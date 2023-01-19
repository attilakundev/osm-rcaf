import sys
from pathlib import Path

project_path = Path(__file__).resolve().parents[1].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib/model")

from previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon
from osm_data_parser import OSMDataParser

data_parser = OSMDataParser()

class OSMErrorMessages:
    def remote_relation(self, relation_id, source):
        remote_relation = ("https://osm.org/relation/{}").format(relation_id) if not source else relation_id
        return remote_relation

    def remote_way(self, way_id, source):
        remote_relation = ("https://osm.org/way/{}").format(way_id) if not source else way_id
        return remote_relation

    def remote_last_forward_way_before_backward_direction(self, array, source):
        if not source and len(array) > 0:
            return ("https://osm.org/way/{}").format(array[0])
        elif len(array) >0:
            return array[0]
        return ""

    def remote_node(self, way_id, source):
        remote_relation = ("https://osm.org/node/{}").format(way_id) if not source else way_id
        return remote_relation

    def previous_current_nodes_hwy(self, prev_curr: PreviousCurrentHighway, source: str):
        string_to_return = ("Previous way's first and last nodes: {first_node_previous} and {last_node_previous} \n"
                            "Role: {previous_role} \n"
                            "Roundabout: {previous_roundabout} \n"
                            "One way road: {previous_oneway} \n"
                            "Current way's first and last nodes: {first_node_current} and {last_node_current} \n"
                            "Role: {current_role} \n"
                            "Roundabout: {current_roundabout} \n"
                            "One way road: {current_oneway} \n"
                            .format(first_node_previous=self.remote_node(prev_curr["first_node_previous"], source),
                                    last_node_previous=self.remote_node(prev_curr["last_node_previous"], source),
                                    previous_role=prev_curr["previous_role"],
                                    previous_roundabout=prev_curr["previous_roundabout"],
                                    previous_oneway=prev_curr["previous_oneway"],
                                    first_node_current=self.remote_node(prev_curr["first_node_current"], source),
                                    last_node_current=self.remote_node(prev_curr["last_node_current"], source),
                                    current_role=prev_curr["current_role"],
                                    current_roundabout=prev_curr["current_roundabout"],
                                    current_oneway=prev_curr["current_oneway"]
                                    )
                            )
        return string_to_return

    def previous_current_nodes_multi(self, prev_curr: PreviousCurrentMultipolygon, source: str):
        # _ = translation string
        string_to_return = ("Previous way's first and last nodes: {first_node_previous} and {last_node_previous} \n"
                            "Role: {previous_role} \n"
                            "Current way's first and last nodes: {first_node_current} and {last_node_current} \n"
                            "Role: {current_role} \n"
                            .format(first_node_previous=self.remote_node(prev_curr["first_node_previous"], source),
                                    last_node_previous=self.remote_node(prev_curr["last_node_previous"], source),
                                    previous_role=prev_curr["previous_role"],
                                    first_node_current=self.remote_node(prev_curr["first_node_current"], source),
                                    last_node_current=self.remote_node(prev_curr["last_node_current"], source),
                                    current_role=prev_curr["current_role"]
                                    ))
        return string_to_return

    def return_messages(self, error_information_list, correct_ways_count, relation_id, source, verbose):
        messages = []
        errors = len(error_information_list)
        total = errors + correct_ways_count
        relation = self.remote_relation(relation_id, source)
        correctness = round((correct_ways_count / total) * 100, 2)
        error_information_list = data_parser.convert_multiple_dataclasses_to_dicts(error_information_list)

        messages.append("=================[Relation #{relation_id}]=================".format(relation_id=relation_id))
        if "https" in relation:
            messages.append("Link of the relation: {relation}".format(relation=relation))
        if errors > 0:
            if not verbose:
                messages.append("This relation has {errors} errors and {correct_ways_count} correct ways. "
                                "That's {correctness}% correct.".format(errors=errors,
                                                                        correct_ways_count=correct_ways_count,
                                                                        correctness=correctness))
            else:
                for error in error_information_list:
                    if error["type"] == "Route":

                        previous_ref = self.remote_way(error["prev_curr"]["previous_ref"], source)
                        last_forward_way_before_backward_direction = self.remote_last_forward_way_before_backward_direction(
                            error["prev_curr"]["last_forward_way_before_backward_direction"], source)
                        currently_checked_ref = error["prev_curr"]["currently_checked_ref"]
                        current_ref = self.remote_way(error["prev_curr"]["current_ref"], source)
                        nodes_and_other_information = self.previous_current_nodes_hwy(error["prev_curr"],
                                                                                      source)
                        match error["error_type"]:
                            case "Gap at the beginning":
                                messages.append("\n[ERROR] Relation with route number {currently_checked_ref}"
                                                " has gap at way: {current_ref} \n"
                                                "This case occured because there is a gap,"
                                                "this happened at the beginning of the "
                                                "relation, since it started with a 2x2 seperated highway. "
                                                "The ID of last way before going to backward direction: "
                                                "{last_forward_way_before_backward_direction} \n{nodes}"
                                                .format(currently_checked_ref=currently_checked_ref,
                                                        current_ref=current_ref,
                                                        last_forward_way_before_backward_direction=last_forward_way_before_backward_direction,
                                                        nodes=nodes_and_other_information))

                            case "Split roundabout":
                                messages.append("\nINFO: There is a roundabout split up to multiple ways, "
                                                "last known way is {current_ref} \n{nodes}".format(
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Forward but not oneway":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has a road segment which "
                                                "has forward role, but not oneway and the following road segment "
                                                "is a normal road segment, way number where this was found: {current_ref} \n"
                                                "Previous way: {previous_ref}\n{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    previous_ref=previous_ref,
                                    nodes=nodes_and_other_information))
                            case "Wrong role setup":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has wrong role setup at way:"
                                                " {current_ref}\n{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Roundabout gap":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has gap at roundabout:"
                                                " {current_ref}\n{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information
                                    ))
                            case "Gap in forward series":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has gap at way: {current_ref} \n"
                                                "It's found in a series of ways with forward role.\n"
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Only one forward way before closed roundabout":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has gap at way: {current_ref} \n"
                                                "There is only one connecting way into the closed "
                                                "(its start and end nodes are the same) roundabout instead of two.\n"
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Wrong order of roundabout entries":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has the way {current_ref} "
                                                "earlier than needed, it's a roundabout entry node and "
                                                "it should be swapped in order to maintain the continuity. \n"
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Duplicated roundabout ways":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has the way {current_ref} "
                                                "roundabout way duplicated, this is wrong, "
                                                "since the route only contains the roundabout once. \n"
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Forward role missing at roundabout":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has a roundabout {current_ref} "
                                                " with forward role missing. \n"
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Forward and non-oneway without ability to move backward":
                                messages.append("\n[ERROR] Relation with route number "
                                                "{currently_checked_ref} has a forward road piece or series,"
                                                "previous ref which is one of the affected: {previous_ref} \n"
                                                "This is not good, because in some cases like 2x1 lane trunk/motorways "
                                                "the traffic can't traverse in the backwards direction."
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    previous_ref=previous_ref,
                                    nodes=nodes_and_other_information))
                            case "Motorway not split":
                                messages.append(
                                    "\n[WARNING] The motorway is continuous, however it reached back from start point to"
                                    " (almost) start point via other lane. It should be done that the motorway's right"
                                    " lane goes first to the end point, then left lane from first to end point.")
                            case "Gap":
                                messages.append("\n[ERROR] Relation with route number {currently_checked_ref} "
                                                "has gap at way: {current_ref} \n"
                                                "{nodes}".format(
                                    currently_checked_ref=currently_checked_ref,
                                    current_ref=current_ref,
                                    nodes=nodes_and_other_information))
                            case "Not supported":
                                messages.append("This public transportation relation type is not supported.")
                    else:
                        # type is ErrorMultipolygon
                        current_ref = self.remote_way(error["prev_curr"]["current_ref"], source)
                        nodes_and_other_information = self.previous_current_nodes_multi(error["prev_curr"],
                                                                                        source)
                        match error["error_type"]:
                            case "Gap in an area consisting of one way":
                                messages.append("\n[ERROR] Multipolygon"
                                                " has an area consisting of one way unclosed,"
                                                " the way affected: {current_ref}\n"
                                                "\n{nodes}"
                                                .format(current_ref=current_ref,
                                                        nodes=nodes_and_other_information))
                            case "Gap in an area consisting of one way at the end":
                                messages.append("\n[ERROR] Multipolygon"
                                                " has an area consisting of one way unclosed at the end of the relation,"
                                                " the way affected: {current_ref}\n"
                                                "\n{nodes}"
                                                .format(current_ref=current_ref,
                                                        nodes=nodes_and_other_information))
                            case "Gap in multi way multipolygon at the end":
                                messages.append("\n[ERROR] Multipolygon"
                                                " has an area consisting of multiple ways unclosed at the end of the relation,"
                                                " the way affected: {current_ref}\n"
                                                "\n{nodes}"
                                                .format(current_ref=current_ref,
                                                        nodes=nodes_and_other_information))
                            case "Gap in multi way multipolygon":
                                messages.append("\n[ERROR] Multipolygon"
                                                " has an area consisting of multiple ways unclosed,"
                                                " the way affected: {current_ref}\n"
                                                "\n{nodes}"
                                                .format(current_ref=current_ref,
                                                        nodes=nodes_and_other_information))
                            case "No role":
                                messages.append("\n[ERROR] Multipolygon"
                                                " has a way which doesn't have a role,"
                                                " the way affected: {current_ref}\n"
                                                "\n{nodes}"
                                                .format(current_ref=current_ref,
                                                        nodes=nodes_and_other_information))
        else:
            messages.append("This relation has no errors and gaps at all.")
            pass
        return messages
