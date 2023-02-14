#!/usr/bin/python3
import sys
from pathlib import Path
import copy

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import fixer_utils
import way_queries


class HighwayFixer:
    def search_for_connection_exiting_from_closed_roundabout(self,
                                                             roundabout_nodes, corrected_ways_to_search,
                                                             already_added_members, ways_to_search):
        count_found_ways = 0
        index = 0
        common_point = "0"  # by default it's zero. there's no such way with "0" identifier
        while index < len(roundabout_nodes):
            way_index = 0
            while way_index < len(ways_to_search):
                node = roundabout_nodes[index]
                way_ref = way_queries.get_way_ref(ways_to_search[way_index])
                start_node = way_queries.get_start_node(ways_to_search[way_index])
                end_node = way_queries.get_end_node(ways_to_search[way_index])
                is_oneway = way_queries.is_oneway(ways_to_search[way_index])
                is_forward = way_queries.get_role(ways_to_search[way_index]) == "forward"

                # It's important to note the order: the exit way's connecting node should be the start node to
                # the roundabout, so we know that's the direct exit and not the entry from the other way around
                # Also important note: the program is prone to such situations like if both of the found ways don't have a common point,
                # it means they're not connecting, so we need to search for another way...
                # (if they have a common point, it means they're the entry and exits)
                if ((start_node == node and count_found_ways == 0 and (is_forward or is_oneway))
                    or (end_node == node and (is_forward or is_oneway) and count_found_ways == 1)
                    or ((start_node == node or end_node == node) and not is_forward and not is_oneway)) \
                        and way_ref not in already_added_members and count_found_ways < 2:
                    if count_found_ways == 0:
                        common_point = end_node
                    if count_found_ways == 0 or start_node == common_point:
                        corrected_ways_to_search.append(ways_to_search[way_index])
                        already_added_members.append(way_ref)
                        count_found_ways += 1
                        index = 0
                        way_index = 0
                    if not is_forward and not is_oneway and count_found_ways == 1 and start_node != common_point:
                        is_common_point = False
                        return corrected_ways_to_search, already_added_members, is_common_point, roundabout_nodes
                    if count_found_ways == 2:
                        is_common_point = True
                        return corrected_ways_to_search, already_added_members, is_common_point, roundabout_nodes
                way_index += 1
            index += 1
        is_common_point = count_found_ways == 2
        return corrected_ways_to_search, already_added_members, is_common_point, roundabout_nodes

    def search_for_connection_in_open_roundabout(self, ways_to_search, corrected_ways_to_search,
                                                 already_added_members, roundabout_entry_first_node,
                                                 roundabout_entry_first_node_index, banned_roundabout_ways):
        index = 0
        checking_condition = "oneway"
        while index < len(ways_to_search) and checking_condition != "normal_road":
            # order to search: oneway -> roundabout* ->normal_road
            # *(until it finds a oneway - this needs to be fixed, since it happens that
            # there are more than 1 roundabout piece until the exit)
            connected = way_queries.check_connectivity(way_queries.get_start_node(corrected_ways_to_search[-1]),
                                                       way_queries.get_end_node(corrected_ways_to_search[-1]),
                                                       way_queries.get_start_node(ways_to_search[index]),
                                                       way_queries.get_end_node(ways_to_search[index]))
            not_in_array = way_queries.get_way_ref(ways_to_search[index]) not in already_added_members
            is_oneway = way_queries.is_oneway(ways_to_search[index])
            is_roundabout = way_queries.is_roundabout(ways_to_search[index])
            checking_condition, index, corrected_ways_to_search, already_added_members, banned_roundabout_ways = self.check_what_type_of_way_we_want_to_search_in_roundabout(
                already_added_members, checking_condition,
                connected, corrected_ways_to_search, index,
                is_oneway, is_roundabout, not_in_array,
                roundabout_entry_first_node, ways_to_search, banned_roundabout_ways)
            index += 1
            if index == len(ways_to_search):
                if checking_condition == "oneway":
                    checking_condition = "roundabout"
                    index = 0
                elif checking_condition == "roundabout":
                    checking_condition = "normal_road"
        # check if we can connect a "normal road" (having no oneway nor any other thing)
        # anyways: this is the other side of the roundabout, so when we found a normal road, we have to reverse as many items as are in the other side
        j = len(
            corrected_ways_to_search) - 1  # initially the index of last item, but then we go back way by way until we find the entry way's index
        found = False
        corrected_ways_to_search, already_added_members = self.reverse_the_other_side_of_roundabout(
            already_added_members, checking_condition, corrected_ways_to_search,
            found, j, roundabout_entry_first_node_index, ways_to_search)
        return corrected_ways_to_search, already_added_members, banned_roundabout_ways

    def reverse_the_other_side_of_roundabout(self, already_added_members, checking_condition, corrected_ways_to_search,
                                             found, j, roundabout_entry_first_node_index, ways_to_search):
        while roundabout_entry_first_node_index <= j and not found:
            index = 0
            while index < len(ways_to_search):
                connected = way_queries.check_connectivity(way_queries.get_start_node(corrected_ways_to_search[j]),
                                                           way_queries.get_end_node(corrected_ways_to_search[j]),
                                                           way_queries.get_start_node(ways_to_search[index]),
                                                           None)  # None, because it happens that we find another piece of roundabout item which is NOT what we want
                way_ref = way_queries.get_way_ref(ways_to_search[index])
                not_in_array = way_ref not in already_added_members
                is_oneway = way_queries.is_oneway(ways_to_search[index])
                is_roundabout = way_queries.is_roundabout(ways_to_search[index])
                is_a_normal_road = not is_oneway and not is_roundabout
                if checking_condition == "normal_road" and connected and not_in_array and is_a_normal_road:
                    returned_array_of_the_ways_other_side = list(reversed(
                        corrected_ways_to_search[
                        j::]))  # reverse the items, since this is how it's connected real life.
                    returned_array_of_the_ways_other_side_refs = list(reversed(already_added_members[j::]))
                    corrected_ways_to_search = corrected_ways_to_search[0:j] + returned_array_of_the_ways_other_side + [
                        ways_to_search[index]]
                    already_added_members = already_added_members[0:j] + returned_array_of_the_ways_other_side_refs + [
                        way_ref]
                    return corrected_ways_to_search, already_added_members
                else:
                    index += 1
            j -= 1
        return corrected_ways_to_search, already_added_members

    def check_what_type_of_way_we_want_to_search_in_roundabout(self, already_added_members, checking_condition,
                                                               connected,
                                                               corrected_ways_to_search, index, is_oneway,
                                                               is_roundabout, not_in_array,
                                                               roundabout_entry_first_node, ways_to_search,
                                                               banned_roundabout_ways):

        if checking_condition == "oneway" and connected and not_in_array and is_oneway and not is_roundabout:
            corrected_ways_to_search.append(ways_to_search[index])
            already_added_members.append(way_queries.get_way_ref(ways_to_search[index]))
            # condition: if we reached the beginning of the roundabout: RETURN.
            # (don't return but go back to the point where you find a normal way)
            index = 0
            if roundabout_entry_first_node == way_queries.get_end_node(ways_to_search[index]):
                checking_condition = "normal_road"
                index = -1
        elif checking_condition == "roundabout" and connected and not_in_array and is_roundabout:
            is_banned = self.determine_if_roundabout_way_should_be_banned_from_relation(ways_to_search,
                                                                                        corrected_ways_to_search, index)
            way_ref = way_queries.get_way_ref(ways_to_search[index])
            if is_banned and way_ref not in banned_roundabout_ways:
                banned_roundabout_ways.append(way_ref)
            elif not is_banned:
                corrected_ways_to_search.append(ways_to_search[index])
                already_added_members.append(way_ref)
                index = -1
                checking_condition = "oneway"
        return checking_condition, index, corrected_ways_to_search, already_added_members, banned_roundabout_ways

    def check_relation_item_if_connected_then_add_it_to_the_corrected_relation(self, first_node_previous,
                                                                               last_node_previous, first_node_current,
                                                                               last_node_current, index,
                                                                               ways_to_search, corrected_ways_to_search,
                                                                               already_added_members,
                                                                               banned_roundabout_ways):
        way_ref = way_queries.get_way_ref(ways_to_search[index])
        is_roundabout = way_queries.is_roundabout(ways_to_search[index])
        is_closed_roundabout = True if way_queries.get_start_node(ways_to_search[index]) == way_queries.get_end_node(
            ways_to_search[index]) else False
        previous_corrected_nodes = way_queries.get_nodes(corrected_ways_to_search[-1])
        sought_way_nodes = way_queries.get_nodes(ways_to_search[index])
        does_the_way_connect_into_roundabout = way_queries.roundabout_checker(sought_way_nodes,
                                                                              previous_corrected_nodes)
        is_motorway = way_queries.get_highway(ways_to_search[index])
        connecting = way_queries.check_connectivity(first_node_previous, last_node_previous, first_node_current,
                                                    last_node_current)
        if way_ref not in already_added_members and way_ref not in banned_roundabout_ways and connecting or (
                is_roundabout and is_closed_roundabout and does_the_way_connect_into_roundabout) or (
                is_motorway and not connecting):
            already_added_members.append(way_ref)
            corrected_ways_to_search.append(ways_to_search[index])
            if is_roundabout and is_closed_roundabout and does_the_way_connect_into_roundabout and index > 1 and way_queries.get_end_node(
                    corrected_ways_to_search[-3]) == way_queries.get_start_node(corrected_ways_to_search[-2]):
                # swap them, because their order is bad.
                corrected_ways_to_search = fixer_utils.swap_items(corrected_ways_to_search,
                                                                  len(corrected_ways_to_search) - 2,
                                                                  len(corrected_ways_to_search) - 3)
                already_added_members = fixer_utils.swap_items(already_added_members, len(already_added_members) - 2,
                                                               len(already_added_members) - 3)
        return corrected_ways_to_search, already_added_members

    def find_first_non_roundabout_backwards(self, index, corrected_relation):
        while index > 1 and way_queries.is_roundabout(corrected_relation[index - 1]):
            index -= 1
        return index

    def check_for_forward_ways(self, already_added_members, corrected_ways_to_search, first_node_previous,
                               index_of_the_connecting_way, last_node_previous,
                               number_of_members_of_this_forward_series, previous_role, split_highway_members,
                               ways_to_search, banned_roundabout_ways):
        connecting_way_role = way_queries.get_role(ways_to_search[index_of_the_connecting_way])
        connecting_way_first_node = way_queries.get_start_node(ways_to_search[index_of_the_connecting_way])
        connecting_way_last_node = way_queries.get_end_node(ways_to_search[index_of_the_connecting_way])
        corrected_ways_to_search, already_added_members = self.check_relation_item_if_connected_then_add_it_to_the_corrected_relation(
            first_node_previous, last_node_previous, connecting_way_first_node, connecting_way_last_node,
            index_of_the_connecting_way, ways_to_search, corrected_ways_to_search, already_added_members,
            banned_roundabout_ways)
        # we came to a road part which has roles.
        # note, we need to create a separate method for creating cardinal relations for "american" roads)
        if previous_role == "" and connecting_way_role == "forward":
            number_of_members_of_this_forward_series = 1
            split_highway_members.append(ways_to_search[index_of_the_connecting_way])
        elif previous_role == "forward" and connecting_way_role == "forward":
            number_of_members_of_this_forward_series += 1
            split_highway_members.append(ways_to_search[index_of_the_connecting_way])
            # It may happen that the members literally loop back to the beginning of the relation, sorta because of the order of the relation's members.
            # To fix this, we need to check if we can insert a way to another way which has no role, but it's not included in the split_highway_members array of course.
            if connecting_way_last_node == way_queries.get_start_node(split_highway_members[0]):
                # loop detected (so we got back to the beginning of the split highway)
                index_of_the_way_where_relation_would_continue = 0
                found = False
                while index_of_the_way_where_relation_would_continue < len(ways_to_search) and not found:
                    j = 0
                    while j < len(split_highway_members) and not found:
                        if way_queries.get_start_node(ways_to_search[
                                                          index_of_the_way_where_relation_would_continue]) == way_queries.get_end_node(
                            split_highway_members[j]) and way_queries.get_way_ref(
                            ways_to_search[index_of_the_way_where_relation_would_continue]) \
                                not in map(lambda x: x["@ref"], split_highway_members):
                            found = True
                            # get the index of the member already contained in the corrected relation
                            try:
                                index_of_second_side_of_roads_first_way = corrected_ways_to_search.index(
                                    split_highway_members[
                                        j]) + 1  # the j marks the last item of the first side of the road (eg. right side)
                            except ValueError:
                                index_of_second_side_of_roads_first_way = -1
                            # reverse the ways after it
                            returned_temp_array = list(reversed(
                                corrected_ways_to_search[index_of_second_side_of_roads_first_way::]))
                            # insert it into the array, the length is the difference between
                            # the length of the split highway's(or carriageway, etc.) members
                            # and the position where the already contained member is in.
                            corrected_ways_to_search = self.insert_array_items_to_a_specific_position(
                                where=corrected_ways_to_search, from_array=returned_temp_array,
                                to_position=index_of_second_side_of_roads_first_way,
                                how_many=len(returned_temp_array))
                            already_added_members = list(map(lambda x: x["@ref"], corrected_ways_to_search))
                            return already_added_members, corrected_ways_to_search, split_highway_members, number_of_members_of_this_forward_series
                        j += 1
                    index_of_the_way_where_relation_would_continue += 1
        elif previous_role == "forward" and connecting_way_role == "":
            # we reached the end of the forward series.
            number_of_members_of_this_forward_series = 0
        return already_added_members, corrected_ways_to_search, split_highway_members, number_of_members_of_this_forward_series

    def insert_array_items_to_a_specific_position(self, where: list, from_array: list, to_position: int, how_many: int):
        beginning_of_where = where[0:to_position]
        to_be_returned = beginning_of_where
        for index in range(how_many):
            to_be_returned.append(from_array[index])
        return to_be_returned

    def search_for_connection(self, index, first_node_previous, last_node_previous,
                              ways_to_search, already_added_members, corrected_ways_to_search,
                              number_of_members_of_this_forward_series, is_common_point, previous_roundabouts_nodes):
        temp_forward_way = -1
        retries = 0  # when we don't find the particular item because it's probably at the beginning of the array.
        items_to_add = []
        while index < len(ways_to_search):
            first_node_sought_way = way_queries.get_start_node(ways_to_search[index])
            last_node_sought_way = way_queries.get_end_node(ways_to_search[index])
            way_ref = way_queries.get_way_ref(ways_to_search[index])
            previous_corrected_nodes = way_queries.get_nodes(corrected_ways_to_search[-1])
            sought_way_nodes = way_queries.get_nodes(ways_to_search[index])
            is_previous_roundabout = way_queries.is_roundabout(corrected_ways_to_search[-1])
            is_roundabout = way_queries.is_roundabout(ways_to_search[index])
            if is_roundabout and first_node_sought_way == last_node_sought_way and way_queries.get_way_ref(
                    ways_to_search[index]) not in already_added_members and way_queries.roundabout_checker(
                sought_way_nodes, previous_corrected_nodes):
                if number_of_members_of_this_forward_series == 1 and retries == 0 and index < len(ways_to_search) - 1:
                    index = 0  # because we don't want the roundabout but we want the other half of the roundabout entry in case of a closed roundabout (now go to the beginning)
                    retries += 1
                elif number_of_members_of_this_forward_series == 1 and retries == 1 and index < len(ways_to_search) - 1:
                    index += 1
                    retries += 1
                elif retries == 2 or retries == 3:  # retries =3: we assume we didn't find the item at the 2nd try, so we wanna add that for sure
                    items_to_add.append(ways_to_search[index])
                    # Basically save this member into an array, then try to search for other forward members that connect between those roundabouts
                    items_to_add = self.check_whether_there_are_missing_items_between_two_closed_roundabouts(
                        is_common_point, ways_to_search, previous_roundabouts_nodes, items_to_add,
                        already_added_members)
                    return index, items_to_add
                else:
                    return index, items_to_add  # If no success, return the roundabout's index (for the future, it should be solved to get the given way from Overpass turbo API
            elif way_queries.get_highway(ways_to_search[index]) == "motorway" and not way_queries.check_connectivity(
                    first_node_previous, last_node_previous, first_node_sought_way,
                    last_node_sought_way):
                return index, items_to_add
            elif not way_queries.check_connectivity(first_node_previous, last_node_previous, first_node_sought_way,
                                                    last_node_sought_way):
                index += 1
                if index == len(ways_to_search) and not is_previous_roundabout and (retries == 0 or retries == 2):
                    index = 0
                    retries += 1
            elif way_ref in already_added_members:  # no duplications are allowed
                index += 1
                if index == len(ways_to_search) and (retries == 0 or retries == 2):
                    index = 0
                    retries += 1
            elif is_roundabout and (
                    not is_previous_roundabout and way_queries.is_roundabout(corrected_ways_to_search[-2])):
                index += 1
                if index == len(ways_to_search) and (retries == 0 or retries == 2):
                    index = 0
                    retries += 1
            elif way_queries.is_oneway(ways_to_search[index]) and way_queries.get_start_node(
                    corrected_ways_to_search[-1]) == way_queries.get_end_node(ways_to_search[index]):
                # We don't want the other side of the roundabout entry, so we search for roundabouts.
                # save the index here, it'll depend on which index we will return, in open roundabout the latter,
                # in closed roundabout, the first.
                roundabout_index = self.search_for_open_roundabout(already_added_members, ways_to_search,
                                                                   first_node_previous, last_node_previous)
                if roundabout_index != -1:
                    return roundabout_index, items_to_add
                return index, items_to_add
            elif way_queries.is_oneway(ways_to_search[index]) and way_queries.get_end_node(
                    corrected_ways_to_search[-1]) == way_queries.get_end_node(ways_to_search[index]) \
                    and not way_queries.is_oneway(corrected_ways_to_search[-1]):
                index += 1
                if index == len(ways_to_search) and (retries == 0 or retries == 2):
                    index = 0
                    retries += 1
            elif number_of_members_of_this_forward_series == 1 and not way_queries.is_oneway(
                    ways_to_search[index]) and not way_queries.is_roundabout(
                ways_to_search[index]) and not way_queries.get_highway(ways_to_search[index]) == "motorway":
                # This is a regular road, but this is not THAT what we want, we either want a roundabout piece or a oneway road
                # BUT. It may happen that there won't be any of those case, so save it.
                temp_forward_way = index
                index += 1
                if index == len(ways_to_search) and (retries == 0 or retries == 2):
                    index = 0
                    retries += 1
            else:
                return index, items_to_add
        if temp_forward_way != -1:
            return temp_forward_way, items_to_add
        return -1, items_to_add  # This means we reached the end of the relation, no further connections can be made.

    def remove_oneway_and_forward_tag_from_certain_members(self, corrected_ways_to_search, current_forward,
                                                           current_oneway, current_roundabout, index,
                                                           remove_one_way_tag, oneway_series_starting_way_index,
                                                           oneway_series_ending_way_index):
        # We delete the oneway/forward tag from those which shouldn't be in the relation, since the route doesn't split.
        if (current_oneway or (current_forward and not current_roundabout)) and remove_one_way_tag:
            corrected_ways_to_search[index] = way_queries.remove_tag(corrected_ways_to_search[index], "oneway",
                                                                     "yes")
            corrected_ways_to_search[index] = way_queries.modify_role(corrected_ways_to_search[index], "")
            if index == oneway_series_ending_way_index and remove_one_way_tag:
                remove_one_way_tag = False
                oneway_series_starting_way_index = -1
                oneway_series_ending_way_index = -1
            return corrected_ways_to_search, remove_one_way_tag, oneway_series_starting_way_index, oneway_series_ending_way_index
        else:
            return corrected_ways_to_search, remove_one_way_tag, oneway_series_starting_way_index, oneway_series_ending_way_index

    def remove_oneway_tag_from_non_roundabout_members_if_needed(self, corrected_ways_to_search, current_forward,
                                                                current_oneway, index, oneway_series_ending_way_index,
                                                                oneway_series_starting_node_detected,
                                                                oneway_series_starting_way_index, previous_forward,
                                                                previous_oneway, remove_one_way_tag,
                                                                previous_roundabout,
                                                                current_roundabout, closed_roundabout_detected):
        if ((previous_oneway and not current_oneway) or (
                not previous_oneway and (previous_forward and not current_forward))) and not current_roundabout:
            # save the position where it needs to stop searching for other members for resetting
            oneway_series_ending_way_index = index - 1  # Let's say we're on a non-oneway, so we want the last one which is one way before
            if not oneway_series_starting_node_detected and not remove_one_way_tag:
                if not closed_roundabout_detected and not previous_roundabout:
                    index = oneway_series_starting_way_index
                    remove_one_way_tag = True
                else:
                    closed_roundabout_detected = False
                    oneway_series_starting_way_index = -1
                    oneway_series_ending_way_index = -1
                return index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected
            # prepare for the case though when this ends, so it won't mess up bigger relations
            if oneway_series_starting_node_detected:
                oneway_series_starting_node_detected = False
        elif (previous_oneway and not current_oneway) or (
                not previous_oneway and previous_forward and not current_forward) and (way_queries.is_roundabout(
            corrected_ways_to_search[index]) and way_queries.get_start_node(
            corrected_ways_to_search[index]) == way_queries.get_end_node(corrected_ways_to_search[index])):
            # for those which have roundabout after the thing: skip it, because this is correct.. (closed roundabouts have no roles)
            oneway_series_starting_node_detected = False
        return index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected

    def detect_if_oneway_road_is_split_or_not(self, corrected_first_node_current, corrected_last_node_current,
                                              corrected_ways_to_search, index, oneway_series_starting_node_detected,
                                              oneway_series_starting_way_index):
        # Oneway roads: detect if it's split or not.
        if oneway_series_starting_way_index != -1 and index != oneway_series_starting_way_index \
                and corrected_first_node_current == way_queries.get_start_node(corrected_ways_to_search[
                                                                                   oneway_series_starting_way_index]) \
                or corrected_last_node_current == way_queries.get_start_node(
            corrected_ways_to_search[oneway_series_starting_way_index]) and way_queries.is_oneway(
            corrected_ways_to_search[index]):
            return True
        else:
            return oneway_series_starting_node_detected

    def add_forward_role_where_needed(self, corrected_first_node_current, corrected_first_node_previous,
                                      corrected_last_node_current, corrected_last_node_previous,
                                      corrected_ways_to_search, current_oneway, index, previous_oneway):
        if previous_oneway and way_queries.get_role(corrected_ways_to_search[index - 1]) != "forward":
            way_queries.modify_role(corrected_ways_to_search[index - 1], "forward")
        if current_oneway and way_queries.get_role(corrected_ways_to_search[index]) != "forward":
            way_queries.modify_role(corrected_ways_to_search[index], "forward")
        if way_queries.is_roundabout(corrected_ways_to_search[
                                         index - 1]) and corrected_first_node_previous != corrected_last_node_previous \
                and way_queries.get_role(corrected_ways_to_search[index - 1]) == "":
            way_queries.modify_role(corrected_ways_to_search[index - 1], "forward")
        if way_queries.is_roundabout(corrected_ways_to_search[
                                         index]) and corrected_first_node_current != corrected_last_node_current and way_queries.get_role(
            corrected_ways_to_search[index]) == "":
            way_queries.modify_role(corrected_ways_to_search[index], "forward")
        return corrected_ways_to_search

    def highway_correction(self, relation_info: dict, first_way: str = ""):
        idx = 0
        ways_to_search = relation_info["ways_to_search"]
        first_way = way_queries.get_way_ref(ways_to_search[0]) if first_way == "" else first_way
        while (idx < len(ways_to_search) and way_queries.get_way_ref(ways_to_search[idx]) != first_way):
            idx += 1
        if idx != 0:
            ways_to_search = fixer_utils.swap_items(ways_to_search, 0, idx)
        corrected_ways_to_search = [ways_to_search[0]]
        already_added_members = [way_queries.get_way_ref(ways_to_search[0])]  # we don't tolerate duplication
        split_highway_members = []
        banned_roundabout_ways = []
        number_of_members_of_this_forward_series = 0
        index = 1
        roundabout_entry_first_node = "0"
        roundabout_entry_first_node_index = -1
        roundabouts_nodes = []
        is_common_point = False
        while index < len(ways_to_search) and len(corrected_ways_to_search) < len(ways_to_search):
            corrected_ways_to_search[-1] = self.get_nodes_roles_and_change_if_necessary(relation_info,
                                                                                        corrected_ways_to_search,
                                                                                        len(corrected_ways_to_search) - 1)
            first_node_previous = way_queries.get_start_node(corrected_ways_to_search[-1])
            last_node_previous = way_queries.get_end_node(corrected_ways_to_search[-1])
            previous_role = way_queries.get_role(corrected_ways_to_search[-1])
            previous_roundabout = way_queries.is_roundabout(corrected_ways_to_search[-1])
            # we'll search the item that is CONNECTING to the next way. (the easiest case, however, we have to check
            # after that, if it's a roundabout, a oneway thing etc.)
            # in case the previous way was a roundabout, see if the two ends connect together,
            # then try to look for a node that connects to another way.
            if previous_roundabout and first_node_previous == last_node_previous:
                corrected_ways_to_search, already_added_members, is_common_point, roundabouts_nodes = self.search_for_connection_exiting_from_closed_roundabout(
                    way_queries.get_nodes(corrected_ways_to_search[index - 1]), corrected_ways_to_search,
                    already_added_members, ways_to_search)
            elif previous_roundabout and first_node_previous != last_node_previous:
                # roundabout_entry_first_node_index: we need this so we can determine when we traverse back, what
                # should be the limiter of iterating, so we don't iterate through the entire corrected array
                roundabout_entry_first_node_index = self.find_first_non_roundabout_backwards(index,
                                                                                             corrected_ways_to_search)
                roundabout_entry_first_node = way_queries.get_start_node(
                    corrected_ways_to_search[roundabout_entry_first_node_index])
                corrected_ways_to_search, already_added_members, banned_roundabout_ways = self.search_for_connection_in_open_roundabout(
                    ways_to_search, corrected_ways_to_search, already_added_members, roundabout_entry_first_node,
                    roundabout_entry_first_node_index, banned_roundabout_ways)
            else:
                # be suspicious, look for a roundabout somewhere (so the previous way and the way before it connects
                # into a common point, both are oneways and not roundabouts)
                index_of_the_connecting_way, items_to_be_added = self.search_for_connection(index, first_node_previous,
                                                                                            last_node_previous,
                                                                                            ways_to_search,
                                                                                            already_added_members,
                                                                                            corrected_ways_to_search,
                                                                                            number_of_members_of_this_forward_series,
                                                                                            is_common_point,
                                                                                            roundabouts_nodes)
                if items_to_be_added:
                    corrected_ways_to_search = corrected_ways_to_search + items_to_be_added
                    already_added_members = already_added_members + list(map(lambda x: x["@ref"], items_to_be_added))
                    split_highway_members = []
                    number_of_members_of_this_forward_series = 0
                    roundabouts_nodes = way_queries.get_nodes(items_to_be_added[-1])
                    index = len(corrected_ways_to_search) - 1
                else:
                    ways_to_search[index_of_the_connecting_way] = self.get_nodes_roles_and_change_if_necessary(
                        relation_info, ways_to_search, index_of_the_connecting_way)
                    if index_of_the_connecting_way != -1 and number_of_members_of_this_forward_series == 2 and way_queries.get_role(
                            ways_to_search[index_of_the_connecting_way]) == "forward" and way_queries.is_oneway(
                        ways_to_search[index_of_the_connecting_way]):
                        split_highway_members, corrected_ways_to_search, index_of_the_connecting_way = self.if_not_roundabout_then_get_rid_of_the_other_half_of_the_road(
                            index, ways_to_search, already_added_members,
                            corrected_ways_to_search,
                            number_of_members_of_this_forward_series, split_highway_members, previous_role,
                            banned_roundabout_ways,is_common_point,roundabouts_nodes
                        )
                    if index_of_the_connecting_way == -1:
                        return corrected_ways_to_search, already_added_members

                    already_added_members, corrected_ways_to_search, split_highway_members, number_of_members_of_this_forward_series = self.check_for_forward_ways(
                        already_added_members,
                        corrected_ways_to_search,
                        first_node_previous,
                        index_of_the_connecting_way,
                        last_node_previous,
                        number_of_members_of_this_forward_series,
                        previous_role,
                        split_highway_members,
                        ways_to_search, banned_roundabout_ways)
            index += 1
        corrected_ways_to_search = self.correct_way_roles_tags(corrected_ways_to_search)
        return corrected_ways_to_search, already_added_members

    def correct_way_roles_tags(self, corrected_ways_to_search):
        """
        post operations on the corrected relation, since they can't be done on-the-go

        :param corrected_ways_to_search:
        :return:
        """
        oneway_series_starting_way_index = -1
        oneway_series_ending_way_index = -1
        oneway_series_starting_node_detected = False  # if false, we have to go back to the index where it started
        remove_one_way_tag = False
        closed_roundabout_detected = False
        index = 1
        while index < len(corrected_ways_to_search):
            corrected_first_node_previous = way_queries.get_start_node(corrected_ways_to_search[index - 1])
            corrected_last_node_previous = way_queries.get_end_node(corrected_ways_to_search[index - 1])
            corrected_first_node_current = way_queries.get_start_node(corrected_ways_to_search[index])
            corrected_last_node_current = way_queries.get_end_node(corrected_ways_to_search[index])
            previous_oneway = way_queries.is_oneway(corrected_ways_to_search[index - 1])
            current_oneway = way_queries.is_oneway(corrected_ways_to_search[index])
            previous_forward = way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"
            current_forward = way_queries.get_role(corrected_ways_to_search[index]) == "forward"
            previous_roundabout = way_queries.is_roundabout(corrected_ways_to_search[index - 1])
            current_roundabout = way_queries.is_roundabout(corrected_ways_to_search[index])
            corrected_ways_to_search = self.add_forward_role_where_needed(corrected_first_node_current,
                                                                          corrected_first_node_previous,
                                                                          corrected_last_node_current,
                                                                          corrected_last_node_previous,
                                                                          corrected_ways_to_search, current_oneway,
                                                                          index, previous_oneway)

            oneway_series_starting_node_detected = self.detect_if_oneway_road_is_split_or_not(
                corrected_first_node_current, corrected_last_node_current, corrected_ways_to_search, index,
                oneway_series_starting_node_detected, oneway_series_starting_way_index)
            closed_roundabout_detected = self.detect_closed_roundabout(corrected_ways_to_search, index,
                                                                       closed_roundabout_detected)
            index_before_change = copy.deepcopy(index)
            # For forwards, we only remove oneway tags for those which aren't roundabout members.
            index, oneway_series_starting_way_index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag, closed_roundabout_detected = self.remove_oneway_tag_from_non_roundabout_members_if_needed(
                corrected_ways_to_search, current_forward, current_oneway, index, oneway_series_ending_way_index,
                oneway_series_starting_node_detected, oneway_series_starting_way_index, previous_forward,
                previous_oneway, remove_one_way_tag, previous_roundabout, current_roundabout,
                closed_roundabout_detected)
            if index_before_change == index:
                corrected_ways_to_search, remove_one_way_tag, oneway_series_starting_way_index, oneway_series_ending_way_index = self.remove_oneway_and_forward_tag_from_certain_members(
                    corrected_ways_to_search,
                    current_forward,
                    current_oneway,
                    current_roundabout,
                    index,
                    remove_one_way_tag, oneway_series_starting_way_index, oneway_series_ending_way_index)
                if index >= 0 and (not previous_oneway and current_oneway or not previous_forward and current_forward):
                    oneway_series_starting_way_index = index
                index += 1
        return corrected_ways_to_search

    def search_for_open_roundabout(self, already_added_members, ways_to_search, first_node_previous,
                                   last_node_previous):
        """
        open roundabout = it's not closed, it consists of multiple pieces.

        :param already_added_members:
        :param ways_to_search:
        :param first_node_previous:
        :param last_node_previous:
        :return:
        """
        for index, way in enumerate(ways_to_search):
            first_node = way_queries.get_start_node(way)
            last_node = way_queries.get_end_node(way)
            way_ref = way_queries.get_way_ref(way)
            if way_ref not in already_added_members and way_queries.is_roundabout(way) and first_node != last_node and \
                    way_queries.check_connectivity(first_node_previous, last_node_previous, first_node, last_node):
                return index
        return -1

    def determine_if_roundabout_way_should_be_banned_from_relation(self, ways_to_search,
                                                                   corrected_ways_to_search, index):
        """
        what should be banned is the way pieces where cars don't usually go on, except when drivers fail to
        take the right exit
        """
        first_node_roundabout_piece = way_queries.get_start_node(ways_to_search[index])
        last_node_roundabout_piece = way_queries.get_end_node(ways_to_search[index])
        first_node_exists_already = False
        last_node_exists_already = False
        for local_index in range(0, len(corrected_ways_to_search)):
            first_node_corrected_way = way_queries.get_start_node(corrected_ways_to_search[local_index])
            last_node_corrected_way = way_queries.get_end_node(corrected_ways_to_search[local_index])
            if (
                    first_node_corrected_way == first_node_roundabout_piece or last_node_corrected_way == first_node_roundabout_piece):
                first_node_exists_already = True
            elif (
                    first_node_corrected_way == last_node_roundabout_piece or last_node_corrected_way == last_node_roundabout_piece):
                last_node_exists_already = True
        if first_node_exists_already and last_node_exists_already:
            return True  # BAN IT
        return False

    def detect_closed_roundabout(self, corrected_ways_to_search, index, closed_roundabout_detected):
        return True if way_queries.is_roundabout(corrected_ways_to_search[index]) and way_queries.get_start_node(
            corrected_ways_to_search[index]) == way_queries.get_end_node(
            corrected_ways_to_search[index]) and closed_roundabout_detected is False else closed_roundabout_detected

    def if_not_roundabout_then_get_rid_of_the_other_half_of_the_road(self, index,
                                                                     ways_to_search, already_added_members,
                                                                     corrected_ways_to_search,
                                                                     number_of_members_of_this_forward_series,
                                                                     split_highway_members, previous_role,
                                                                     banned_roundabout_ways, is_common_point,
                                                                     previous_roundabouts_nodes):
        # get the index of the way first what we want to delete (eg. it's 5, but we want 6, because not a closed roundabout)
        # in some cases we got the other side of the road and yes that's wrong completely
        index_of_the_wrong_way = way_queries.get_index_of_way(ways_to_search,
                                                              way_queries.get_way_ref(corrected_ways_to_search[-1]))
        first_node_previous = way_queries.get_start_node(corrected_ways_to_search[-2])
        last_node_previous = way_queries.get_start_node(corrected_ways_to_search[-2])
        index_of_the_connecting_way, _ = self.search_for_connection(index_of_the_wrong_way + 1, first_node_previous,
                                                                 last_node_previous,
                                                                 ways_to_search, already_added_members,
                                                                 corrected_ways_to_search,
                                                                 number_of_members_of_this_forward_series - 1,
                                                                 is_common_point, previous_roundabouts_nodes) #items_to_be_added is not necessary here, just the return values are like that
        if index_of_the_connecting_way == -1:
            return split_highway_members, corrected_ways_to_search, index_of_the_connecting_way
        else:
            # remove the wrong way
            corrected_ways_to_search.remove(corrected_ways_to_search[-1])
            split_highway_members.remove(split_highway_members[-1])
            already_added_members.remove(already_added_members[-1])
            number_of_members_of_this_forward_series -= 1
            # insert the correct way into place
            already_added_members, corrected_ways_to_search, split_highway_members, number_of_members_of_this_forward_series = self.check_for_forward_ways(
                already_added_members,
                corrected_ways_to_search,
                first_node_previous,
                index_of_the_connecting_way,
                last_node_previous,
                number_of_members_of_this_forward_series,
                previous_role,
                split_highway_members,
                ways_to_search, banned_roundabout_ways)
            # then find the good correct connecting way,and then return
            index_of_the_connecting_way, _ = self.search_for_connection(index, first_node_previous,
                                                                     last_node_previous,
                                                                     ways_to_search, already_added_members,
                                                                     corrected_ways_to_search,
                                                                     number_of_members_of_this_forward_series,is_common_point, previous_roundabouts_nodes)
            return split_highway_members, corrected_ways_to_search, index_of_the_connecting_way

    def get_nodes_roles_and_change_if_necessary(self, relation_info, array_where_get_the_role, index):
        if relation_info["route"] != "bicycle" and way_queries.get_role(array_where_get_the_role[index]) == "backward":
            way = way_queries.modify_role(array_where_get_the_role[index], "forward")
            way = list(reversed(way["nd"]))
            return way
        else:
            return array_where_get_the_role[index]

    def check_whether_there_are_missing_items_between_two_closed_roundabouts(self, is_common_point, ways_to_search,
                                                                             previous_roundabouts_nodes, items_to_add,
                                                                             already_added_members):
        """
        The intention of the method is that we have a double CLOSED roundabout. We collected a roundabout member instead of the other side of the ways of the forward series connecting the
        two roundabout. If we know that there's no common point to make a unified road, we know it's clearly a double roundabout situation.
        :param is_common_point:
        :param ways_to_search:
        :param previous_roundabouts_nodes:
        :param items_to_add:
        :param already_added_members:
        :return:
        """
        current_roundabouts_nodes = way_queries.get_nodes(items_to_add[0])
        index = 0
        if is_common_point is False:
            while index < len(ways_to_search):
                current_ways_nodes = way_queries.get_nodes(ways_to_search[index])
                way_ref = way_queries.get_way_ref(ways_to_search[index])
                if len(items_to_add) == 1 and way_queries.roundabout_checker(previous_roundabouts_nodes,
                                                                             current_ways_nodes) and way_ref not in already_added_members:
                    items_to_add = [ways_to_search[index]] + items_to_add
                elif len(items_to_add) >= 2 and way_queries.check_connectivity(
                        way_queries.get_start_node(items_to_add[len(items_to_add) - 2]),
                        way_queries.get_end_node(items_to_add[len(items_to_add) - 2]),
                        way_queries.get_start_node(ways_to_search[index]),
                        way_queries.get_end_node(
                            ways_to_search[index])) and way_ref not in already_added_members and way_ref not in map(
                    lambda x: x["@ref"], items_to_add):
                    items_to_add = items_to_add[0:-1] + [ways_to_search[index]] + [items_to_add[-1]]
                    if way_queries.roundabout_checker(current_roundabouts_nodes,
                                                      way_queries.get_nodes(ways_to_search[index])):
                        return items_to_add
                index += 1
            pass
        else:
            return items_to_add
