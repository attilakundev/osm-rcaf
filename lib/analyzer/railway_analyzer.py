#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

import way_queries
from previous_current import PreviousCurrentHighway


class RailwayAnalyzer:
    def railway_checking(self, relation_info, error_information):
        first_node_previous = ""
        last_node_previous = ""
        previous_ref = ""
        correct_ways_count = 0
        for elem_val in relation_info["ways_to_search"]:
            first_node_current = way_queries.get_start_node(elem_val)
            last_node_current = way_queries.get_end_node(elem_val)
            current_ref = way_queries.get_way_ref(elem_val)
            # just check, if the way is connected to the other
            if first_node_previous != "" and last_node_previous != "" and previous_ref != "":
                prev_curr = PreviousCurrentHighway(first_node_previous=first_node_previous,
                                                   last_node_previous=last_node_previous,
                                                   first_node_current=first_node_current,
                                                   last_node_current=last_node_current,
                                                   current_ref=current_ref, previous_ref=previous_ref)
                is_error = self.check_rails_if_the_ways_are_not_connected(first_node_previous, last_node_previous,
                                                                          first_node_current, last_node_current)
                if is_error:
                    error_information.append([prev_curr, "Railway not connecting"])
            first_node_previous = way_queries.get_start_node(elem_val)
            last_node_previous = way_queries.get_end_node(elem_val)
            previous_ref = way_queries.get_way_ref(elem_val)
            correct_ways_count = len(relation_info["ways_to_search"]) - len(error_information)
        return error_information, correct_ways_count  # the number of errors could be calculated
        # from len(error_information)

    def check_rails_if_the_ways_are_not_connected(self, first_node_previous, last_node_previous,
                                                  first_node_current, last_node_current):
        if first_node_previous != "" and last_node_previous != "" and not way_queries.check_connectivity(
                first_node_previous, last_node_previous, first_node_current, last_node_current):
            return True
        return False
