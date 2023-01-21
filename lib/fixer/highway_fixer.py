#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import way_queries


class HighwayFixer:
    def search_for_connection_exiting_from_closed_roundabout(self, previous_roundabout, first_node_previous,
                                                             last_node_previous,
                                                             roundabout_nodes, corrected_ways_to_search,
                                                             already_added_members, ways_to_search):

        count_found_ways = 0
        for node in roundabout_nodes:
            for way in ways_to_search:
                way_ref = way_queries.get_way_ref(way)
                # unfortunately we have to look through every way. of course, there's a big cliffhanger.
                # We need to apply this twice, because we need two connections to the roundabout. (of course it happens we only have one connection :-) )
                # the if statement should contain way_queries.get_role(way) == "forward", but I realized this is not needed,
                # there are cases when there is a single way going from the roundabout out, if it has no role of course, and it's not oneway.
                if (way_queries.get_start_node(way) == node or
                    way_queries.get_end_node == node) \
                        and way_ref not in already_added_members and count_found_ways < 1:
                    corrected_ways_to_search.append(way)
                    already_added_members.append(way_ref)
                    count_found_ways += 1
                    if way_queries.get_role(way) == "" and way_queries.is_oneway(way):
                        return corrected_ways_to_search, already_added_members
        while count_found_ways < 2:
            for way in ways_to_search:
                way_ref = way_queries.get_way_ref(way)
                if way_queries.get_role(way) == "forward" and way_queries.check_connectivity(
                        way_queries.get_start_node(way), way_queries.get_end_node(way),
                        way_queries.get_start_node(corrected_ways_to_search[-1]),
                        way_queries.get_end_node(corrected_ways_to_search[-1])) \
                        and way_ref not in already_added_members:
                    corrected_ways_to_search.append(way)
                    already_added_members.append(way_ref)
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

    def add_tag_to_item(self, key, value, tags: list):
        tag = {
            "@k": key,
            "@v": value
        }
        tags.append(tag)
        return tag

    def find_first_non_roundabout_backwards(self, index, corrected_relation):
        while index > 1 and way_queries.is_roundabout(corrected_relation[index - 1]):
            index -= 1
        return index

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
                    previous_roundabout, first_node_previous, last_node_previous,
                    way_queries.get_nodes(corrected_ways_to_search[index - 1]), corrected_ways_to_search,
                    already_added_members, ways_to_search)
            elif previous_roundabout and first_node_previous != last_node_previous:
                # roundabout_entry_f_n_index: we need this so we can determine when we traverse back, what should be the limiter
                # of iterating, so we don't iterate through the entire corrected array
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
                              roundabout_entry_first_way_index):
        tmp_index = -1
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
                                                                 already_added_members, roundabout_entry_first_node,
                                                                 roundabout_entry_first_node,
                                                                 roundabout_entry_first_way_index)

            pass
