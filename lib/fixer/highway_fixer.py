#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import way_queries


class HighwayFixer:
    def search_for_connection_exiting_from_closed_roundabout(self,
                                                             roundabout_nodes, corrected_ways_to_search,
                                                             already_added_members, ways_to_search):
        count_found_ways = 0
        index = 0
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
                if ((start_node == node and count_found_ways == 0 and (is_forward or is_oneway))
                    or (end_node == node and (is_forward or is_oneway) and count_found_ways == 1)
                    or ((start_node == node or end_node == node) and not is_forward and not is_oneway)) \
                        and way_ref not in already_added_members and count_found_ways < 2:
                    corrected_ways_to_search.append(ways_to_search[way_index])
                    already_added_members.append(way_ref)
                    count_found_ways += 1
                    index = 0
                    way_index = 0
                    if not is_forward and not is_oneway and count_found_ways == 1:
                        return corrected_ways_to_search, already_added_members
                    if count_found_ways == 2:
                        return corrected_ways_to_search, already_added_members
                way_index += 1
            index += 1
        return corrected_ways_to_search, already_added_members

    def search_for_connection_in_open_roundabout(self, ways_to_search, corrected_ways_to_search,
                                                 already_added_members, roundabout_entry_first_node,
                                                 roundabout_entry_first_way_index):
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
            checking_condition, index, corrected_ways_to_search, already_added_members = self.check_what_type_of_way_we_want_to_search_in_roundabout(
                already_added_members, checking_condition,
                connected, corrected_ways_to_search, index,
                is_oneway, is_roundabout, not_in_array,
                roundabout_entry_first_node, ways_to_search)
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
            found, j, roundabout_entry_first_way_index, ways_to_search)
        return corrected_ways_to_search, already_added_members

    def reverse_the_other_side_of_roundabout(self, already_added_members, checking_condition, corrected_ways_to_search,
                                             found, j, roundabout_entry_first_way_index, ways_to_search):
        while roundabout_entry_first_way_index <= j and not found:
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
                    corrected_ways_to_search = corrected_ways_to_search + returned_array_of_the_ways_other_side
                    already_added_members.append(way_ref)
                    return corrected_ways_to_search, already_added_members
                else:
                    index += 1
            j -= 1
        return corrected_ways_to_search, already_added_members

    def check_what_type_of_way_we_want_to_search_in_roundabout(self, already_added_members, checking_condition,
                                                               connected,
                                                               corrected_ways_to_search, index, is_oneway,
                                                               is_roundabout, not_in_array,
                                                               roundabout_entry_first_node, ways_to_search):
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
            corrected_ways_to_search.append(ways_to_search[index])
            already_added_members.append(way_queries.get_way_ref(ways_to_search[index]))
            index = -1
            checking_condition = "oneway"
        return checking_condition, index, corrected_ways_to_search, already_added_members

    def search_for_tag(self, array, key, value):
        for tags in array["tag"]:
            for tag in tags:
                if tag["@k"] == key and tag["@v"] == value:
                    return True
        return False

    def check_relation_item_if_connected_then_add_it_to_the_corrected_relation(self, first_node_previous,
                                                                               last_node_previous, first_node_current,
                                                                               last_node_current, index,
                                                                               ways_to_search, corrected_ways_to_search,
                                                                               already_added_members):
        way_ref = way_queries.get_way_ref(ways_to_search[index])
        if way_ref not in already_added_members and way_queries.check_connectivity(first_node_previous,
                                                                                   last_node_previous,
                                                                                   first_node_current,
                                                                                   last_node_current):
            already_added_members.append(way_ref)
            corrected_ways_to_search.append(ways_to_search[index])
        return corrected_ways_to_search, already_added_members

    def add_tag_to_item(self, key, value, array: dict):
        tag = {
            "@k": key,
            "@v": value
        }
        array["tag"].append(tag)
        return array

    def find_first_non_roundabout_backwards(self, index, corrected_relation):
        while index > 1 and way_queries.is_roundabout(corrected_relation[index - 1]):
            index -= 1
        return index

    def check_for_forward_ways(self, already_added_members, corrected_ways_to_search, first_node_previous,
                               index_of_the_connecting_way, last_node_previous,
                               number_of_members_of_this_forward_series, previous_role, split_highway_members,
                               ways_to_search):
        connecting_way_role = way_queries.get_role(ways_to_search[index_of_the_connecting_way])
        connecting_way_first_node = way_queries.get_start_node(ways_to_search[index_of_the_connecting_way])
        connecting_way_last_node = way_queries.get_end_node(ways_to_search[index_of_the_connecting_way])
        corrected_ways_to_search, already_added_members = self.check_relation_item_if_connected_then_add_it_to_the_corrected_relation(
            first_node_previous, last_node_previous, connecting_way_first_node, connecting_way_first_node,
            index_of_the_connecting_way, ways_to_search, corrected_ways_to_search, already_added_members)
        # we came to a road part which has roles.
        # note, we need to create a separate method for creating cardinal relations for "american" roads)
        if previous_role == "" and connecting_way_role == "forward":
            number_of_members_of_this_forward_series = 1
        elif previous_role == "forward" and connecting_way_role == "forward":
            number_of_members_of_this_forward_series += 1
            split_highway_members.append(ways_to_search[index_of_the_connecting_way])
            # It may happen that the members literally loop back to the beginning of the relation, sorta because of the order of the relation's members.
            # To fix this, we need to check if we can insert a way to another way which has no role, but it's not included in the split_highway_members array of course.
            if connecting_way_last_node == way_queries.get_start_node(split_highway_members[0]):
                # loop detected (so we got back to the beginning of the split highway)
                i = 0
                found = False
                while i < len(ways_to_search) and not found:
                    j = 0
                    while j < len(split_highway_members) and not found:
                        if way_queries.get_start_node(ways_to_search[i]) == way_queries.get_end_node(
                                ways_to_search[i]) and way_queries.get_way_ref(ways_to_search[i]) \
                                not in map(lambda x: x["@ref"], split_highway_members):
                            found = True
                            # get the index of the member already contained in the corrected relation
                            try:
                                index_of_first_side_of_roads_last_way = corrected_ways_to_search.index(
                                    split_highway_members[j])
                            except ValueError:
                                index_of_first_side_of_roads_last_way = -1
                            # reverse the ways after it
                            returned_temp_array = list(reversed(
                                corrected_ways_to_search[
                                index_of_first_side_of_roads_last_way + 1::]))
                            # insert it into the array, the length is the difference between
                            # the length of the split highway's(or carriageway, etc) members
                            # and the position where the already contained member is in.
                            corrected_ways_to_search = self.insert_array_items_to_a_specific_position(
                                where=corrected_ways_to_search, from_array=returned_temp_array,
                                to_position=index_of_first_side_of_roads_last_way,
                                how_many=len(split_highway_members) - j)
                        j += 1
                    i += 1
        elif previous_role == "forward" and connecting_way_role == "":
            # we reached the end of the forward series.
            split_highway_members.append(ways_to_search[index_of_the_connecting_way])

        return already_added_members, corrected_ways_to_search, split_highway_members

    def insert_array_items_to_a_specific_position(self, where: list, from_array: list, to_position: int, how_many: int):
        for index in range(len(where)):
            if index == to_position:
                beginning_of_where = where[0:to_position]
                rest_of_where = where[to_position:]
                to_be_returned = beginning_of_where
                for index in range(how_many):
                    to_be_returned.append(from_array[index])
                to_be_returned += rest_of_where
                return to_be_returned

    def search_for_connection(self, index, first_node_previous, last_node_previous, do_not_search_a_roundabout,
                              ways_to_search, already_added_members, corrected_ways_to_search,
                              roundabout_entry_first_node,
                              roundabout_entry_first_way_index, number_of_members_of_this_forward_series):
        temp_forward_way = -1
        while index < len(ways_to_search):
            first_node_sought_way = way_queries.get_start_node(ways_to_search[index])
            last_node_sought_way = way_queries.get_end_node(ways_to_search[index])
            if way_queries.check_connectivity(first_node_previous, last_node_previous, first_node_sought_way,
                                              last_node_sought_way):
                index += 1
            elif way_queries.get_way_ref(ways_to_search[index]) in already_added_members:
                index += 1
            elif do_not_search_a_roundabout and way_queries.is_roundabout(ways_to_search[index]):
                index += 1
                do_not_search_a_roundabout = False
            elif way_queries.is_oneway(ways_to_search[index]) and way_queries.get_start_node(
                    ways_to_search[index]) == way_queries.get_end_node(ways_to_search[index]):
                # save the index here, it'll depend on which index we will return, in open roundabout the latter,
                # in closed roundabout, the first.
                if self.search_for_connection_in_open_roundabout(ways_to_search, corrected_ways_to_search,
                                                                 already_added_members,
                                                                 roundabout_entry_first_node,
                                                                 roundabout_entry_first_way_index):
                    index += 1
                return index
            elif number_of_members_of_this_forward_series == 1 and not way_queries.is_oneway(
                    ways_to_search[index]) and not way_queries.is_roundabout(ways_to_search[index]):
                # This is a regular road, but this is not THAT what we want, we either want a roundabout piece or a oneway road
                # BUT. It may happen that there won't be any of those case, so save it.
                temp_forward_way = index
                index += 1
            elif number_of_members_of_this_forward_series == 1 and way_queries.is_roundabout(
                    ways_to_search[index]) and way_queries.get_start_node(
                ways_to_search[index]) == way_queries.get_end_node(ways_to_search[index]):
                # it's a roundabout, but I want two sides of that roundabout... (since that roundabout is closed!)
                index += 1
            else:
                return index
        if temp_forward_way != -1:
            return temp_forward_way

    def remove_oneway_and_forward_tag_from_certain_members(self, corrected_ways_to_search, current_forward,
                                                           current_oneway, current_roundabout, index,
                                                           remove_one_way_tag):
        # We delete the oneway/forward tag from those which shouldn't be in the relation, since the route doesn't split.
        if (current_oneway or (current_forward and not current_roundabout)) and remove_one_way_tag:
            corrected_ways_to_search[index] = way_queries.remove_tag(corrected_ways_to_search[index], "oneway",
                                                                     "yes")
            corrected_ways_to_search[index] = way_queries.modify_role(corrected_ways_to_search[index], "")
        return corrected_ways_to_search

    def remove_oneway_tag_from_non_roundabout_members_if_needed(self, corrected_ways_to_search, current_forward,
                                                                current_oneway, index, oneway_series_ending_way_index,
                                                                oneway_series_starting_node_detected,
                                                                oneway_series_starting_way_index, previous_forward,
                                                                previous_oneway, remove_one_way_tag):
        if (previous_oneway and not current_oneway) or previous_oneway and previous_forward and not current_forward:
            # save the position where it needs to stop searching for other members for resetting
            oneway_series_ending_way_index = index
            if not oneway_series_starting_node_detected and not remove_one_way_tag:
                index = oneway_series_starting_way_index - 1  # why? since we'll have an i++, let's say we have i=4 but our series starts at 5..
                remove_one_way_tag = True
            # prepare for the case though when this ends, so it won't mess up bigger relations
            if oneway_series_starting_node_detected:
                oneway_series_starting_node_detected = False
        elif (previous_oneway and not current_oneway) or (
                not previous_oneway and previous_forward and not current_forward) and way_queries.is_roundabout(
            corrected_ways_to_search[index]):
            # for those which have roundabout after the thing: skip it, because this is correct..
            oneway_series_starting_node_detected = False
        return index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag

    def detect_if_oneway_road_is_split_or_not(self, corrected_first_node_current, corrected_last_node_current,
                                              corrected_ways_to_search, index, oneway_series_starting_node_detected,
                                              oneway_series_starting_way_index):
        # Oneway roads: detect if it's split or not.
        if oneway_series_starting_way_index != -1 and index != oneway_series_starting_way_index \
                and corrected_first_node_current == way_queries.get_start_node(corrected_ways_to_search[
                                                                                   oneway_series_starting_way_index]) \
                or corrected_last_node_current == way_queries.get_start_node(
            corrected_ways_to_search[oneway_series_starting_way_index]):
            if way_queries.is_oneway(corrected_ways_to_search[index]):
                oneway_series_starting_node_detected = True
        return oneway_series_starting_node_detected

    def add_forward_role_where_needed(self, corrected_first_node_current, corrected_first_node_previous,
                                      corrected_last_node_current, corrected_last_node_previous,
                                      corrected_ways_to_search, current_oneway, index, previous_oneway):
        if previous_oneway:
            corrected_ways_to_search[index - 1]["role"] = "forward"
        if current_oneway:
            corrected_ways_to_search[index]["role"] = "forward"
        if way_queries.is_roundabout(corrected_ways_to_search[
                                         index - 1]) and corrected_first_node_previous != corrected_last_node_previous \
                and way_queries.get_role(corrected_ways_to_search[index - 1] == ""):
            corrected_ways_to_search[index - 1]["role"] = "forward"
        if way_queries.is_roundabout(corrected_ways_to_search[
                                         index]) and corrected_first_node_current != corrected_last_node_current and way_queries.get_role(
            corrected_ways_to_search[index] == ""):
            corrected_ways_to_search[index]["role"] = "forward"
        return corrected_ways_to_search

    def add_oneway_tag_where_needed(self, corrected_ways_to_search, current_forward, index, previous_forward):
        if previous_forward and current_forward:
            if not self.search_for_tag(corrected_ways_to_search[index - 1], "oneway", "yes"):
                corrected_ways_to_search[index - 1] = self.add_tag_to_item("oneway", "yes",
                                                                           corrected_ways_to_search[index - 1])
            if not self.search_for_tag(corrected_ways_to_search[index], "oneway", "yes"):
                corrected_ways_to_search[index] = self.add_tag_to_item("oneway", "yes",
                                                                       corrected_ways_to_search[index])
        return corrected_ways_to_search

    def highway_correction(self, relation_info: dict, relation_id: str = "", first_way: str = ""):
        idx = 0
        corrected_ways_to_search = []  # substitute this list back at the end of this
        ways_to_search = relation_info["ways_to_search"]
        while (idx < len(ways_to_search) and ways_to_search[idx]["@ref"] != first_way):
            idx += 1
        if idx != 0:
            temp = ways_to_search[idx]
            ways_to_search[idx] = ways_to_search[0]
            ways_to_search[0] = temp
        corrected_ways_to_search.append(ways_to_search[0])
        already_added_members = []  # we don't tolerate duplication
        split_highway_members = []
        number_of_members_of_this_forward_series = 0
        last_saved_item_index = 0
        roundabout_entry_first_node = 0
        do_not_search_a_roundabout = False
        for index in range(1, len(ways_to_search)):
            first_node_previous = way_queries.get_start_node(ways_to_search[index - 1])
            last_node_previous = way_queries.get_end_node(ways_to_search[index - 1])
            previous_roundabout = way_queries.is_roundabout(ways_to_search[index - 1])
            previous_role = way_queries.get_role(ways_to_search[index - 1])
            # we'll search the item that is CONNECTING to the next way. (the easiest case, however, we have to check
            # after that, if it's a roundabout, a oneway thing etc.)

            # in case the previous way was a roundabout, see if the two ends connect together,
            # then try to look for a node that connects to another way.
            if previous_roundabout and first_node_previous == last_node_previous:
                corrected_ways_to_search, already_added_members = self.search_for_connection_exiting_from_closed_roundabout(
                    way_queries.get_nodes(corrected_ways_to_search[index - 1]), corrected_ways_to_search,
                    already_added_members, ways_to_search)
            elif previous_roundabout and first_node_previous != last_node_previous:
                # roundabout_entry_first_node_index: we need this so we can determine when we traverse back, what
                # should be the limiter of iterating, so we don't iterate through the entire corrected array
                roundabout_entry_first_node_index = self.find_first_non_roundabout_backwards(index,
                                                                                             corrected_ways_to_search)
                roundabout_entry_first_node = way_queries.get_start_node(
                    corrected_ways_to_search[roundabout_entry_first_node_index])
                corrected_ways_to_search, already_added_members = self.search_for_connection_in_open_roundabout(
                    ways_to_search, corrected_ways_to_search, already_added_members, roundabout_entry_first_node,
                    roundabout_entry_first_node_index
                )
            else:
                # be suspicious, look for a roundabout somewhere (so the previous way and the way before it connects
                # into a common point, both are oneways and not roundabouts)
                index_of_the_connecting_way = self.search_for_connection(index, first_node_previous, last_node_previous,
                                                                         do_not_search_a_roundabout, ways_to_search)
                already_added_members, corrected_ways_to_search, split_highway_members = self.check_for_forward_ways(
                    already_added_members,
                    corrected_ways_to_search,
                    first_node_previous,
                    index_of_the_connecting_way,
                    last_node_previous,
                    number_of_members_of_this_forward_series,
                    previous_role,
                    split_highway_members,
                    ways_to_search)
        # post operations on the corrected relation, since they can't be done on-the-go
        oneway_series_starting_way_index = -1;
        oneway_series_ending_way_index = -1;
        oneway_series_starting_node_detected = False  # if false, we have to go back to the index where it started
        remove_one_way_tag = False
        index = 1
        while index < len(corrected_ways_to_search):
            corrected_first_node_previous = way_queries.get_start_node(corrected_ways_to_search[index - 1])
            corrected_last_node_previous = way_queries.get_end_node(corrected_ways_to_search[index - 1])
            corrected_first_node_current = way_queries.get_start_node(corrected_ways_to_search[index])
            corrected_last_node_current = way_queries.get_end_node(corrected_ways_to_search[index])
            previous_oneway = way_queries.is_oneway(corrected_ways_to_search[index - 1])
            current_oneway = way_queries.is_oneway(corrected_ways_to_search[index - 1])
            previous_forward = way_queries.get_role(corrected_ways_to_search[index - 1]) == "forward"
            current_forward = way_queries.get_role(corrected_ways_to_search[index]) == "forward"
            current_roundabout = way_queries.is_roundabout(corrected_ways_to_search[index])
            corrected_ways_to_search = self.add_forward_role_where_needed(corrected_first_node_current,
                                                                          corrected_first_node_previous,
                                                                          corrected_last_node_current,
                                                                          corrected_last_node_previous,
                                                                          corrected_ways_to_search, current_oneway,
                                                                          index, previous_oneway)
            corrected_ways_to_search = self.add_oneway_tag_where_needed(corrected_ways_to_search, current_forward,
                                                                        index, previous_forward)

            oneway_series_starting_node_detected = self.detect_if_oneway_road_is_split_or_not(
                corrected_first_node_current, corrected_last_node_current, corrected_ways_to_search, index,
                oneway_series_starting_node_detected, oneway_series_starting_way_index)
            # For forwards, we only remove oneway tags for those which aren't roundabout members.
            index, oneway_series_ending_way_index, oneway_series_starting_node_detected, remove_one_way_tag = self.remove_oneway_tag_from_non_roundabout_members_if_needed(
                corrected_ways_to_search, current_forward, current_oneway, index, oneway_series_ending_way_index,
                oneway_series_starting_node_detected, oneway_series_starting_way_index, previous_forward,
                previous_oneway, remove_one_way_tag)
            if index == oneway_series_ending_way_index and remove_one_way_tag:
                remove_one_way_tag = False
                oneway_series_starting_way_index = -1
                oneway_series_ending_way_index = -1
            corrected_ways_to_search = self.remove_oneway_and_forward_tag_from_certain_members(corrected_ways_to_search,
                                                                                               current_forward,
                                                                                               current_oneway,
                                                                                               current_roundabout,
                                                                                               index,
                                                                                               remove_one_way_tag)
            if index > 0 and (not previous_oneway and current_oneway or not previous_forward and current_forward):
                oneway_series_starting_way_index = index
            index += 1
        return corrected_ways_to_search
