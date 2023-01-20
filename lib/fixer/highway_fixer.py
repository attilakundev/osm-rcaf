#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import way_queries


class HighwayFixer:
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
        do_not_search_a_roundabout = False
        for index in range(1, len(ways_to_search)):
            index = len(corrected_ways_to_search)
            first_node_previous = way_queries.get_start_node(ways_to_search[index - 1])
            last_node_previous = way_queries.get_end_node(ways_to_search[index - 1])
            previous_roundabout = way_queries.is_roundabout(ways_to_search[index - 1])
            previous_role = way_queries.get_role(ways_to_search[index - 1])
            # we'll search the item that is CONNECTING to the next way. (the easiest case, however, we have to check
            # after that, if it's a roundabout, a oneway thing etc.)

            corrected_ways_to_search, already_added_members = self.search_for_connection_in_closed_roundabout(
                previous_roundabout, first_node_previous, last_node_previous, index,
                way_queries.get_nodes(corrected_ways_to_search[index - 1]), corrected_ways_to_search,
                already_added_members, ways_to_search)

    pass

    def search_for_connection_to_closed_roundabout(self, previous_roundabout, first_node_previous, last_node_previous,
                                                   index, roundabout_nodes, corrected_ways_to_search,
                                                   already_added_members, ways_to_search):
        if previous_roundabout and first_node_previous == last_node_previous:
            count_found_ways = 0
            for node in roundabout_nodes:
                for way in ways_to_search:
                    way_ref = way_queries.get_way_ref(way)
                    # unfortunately we have to look through all ways. of course, there's a big cliffhanger.
                    # We need to apply this twice, because we need two connections to the roundabout. (of course it happens we only have one connection :-) )
                    # the if statement should contain way_queries.get_role(way) == "forward", but I realized this is not needed, there are cases when there is a single way going from the roundabout out, if it has no role of course, and it's not oneway.
                    if (way_queries.get_start_node(way) == node or
                        way_queries.get_end_node == node) \
                                and way_ref not in already_added_members and count_found_ways < 1:
                        corrected_ways_to_search.append(way)
                        already_added_members.append(way_ref)
                        count_found_ways += 1
                        if way_queries.get_role(way) == "" and way_queries.is_oneway(way):
                            return corrected_ways_to_search, already_added_members
            while count_found_ways < 2:
                for node in roundabout_nodes:
                    for way in ways_to_search:
                        pass # to be done
        else:
            return corrected_ways_to_search, already_added_members
