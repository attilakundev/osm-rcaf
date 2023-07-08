#!/usr/bin/python3
from src.lib import way_queries
from src.lib.model.previous_current import PreviousCurrentHighway
from src.lib.analyzer.analyzer_base import AnalyzerBase


class RailwayAnalyzer(AnalyzerBase):
    def checking(self, relation_info):
        error_information = []
        prev_curr = PreviousCurrentHighway()
        for elem_val in relation_info["ways_to_search"]:
            prev_curr = self.set_up_current_member(elem_val, prev_curr)
            # just check, if the way is connected to the other
            self.check_if_connected_to_other_member(error_information, prev_curr)
            self.set_previous_member(elem_val, prev_curr)
        correct_ways_count = len(relation_info["ways_to_search"]) - len(error_information)
        return error_information, correct_ways_count

    def check_if_connected_to_other_member(self, error_information, prev_curr):
        if prev_curr.first_node_previous != "" and prev_curr.last_node_previous != "" \
                and prev_curr.previous_ref != "":
            is_error = self.check_rails_if_the_ways_are_not_connected(prev_curr)
            if is_error:
                error_information.append([prev_curr, "Railway not connecting"])

    def set_previous_member(self, elem_val, prev_curr):
        prev_curr.first_node_previous = way_queries.get_start_node(elem_val)
        prev_curr.last_node_previous = way_queries.get_end_node(elem_val)
        prev_curr.previous_ref = way_queries.get_way_ref(elem_val)

    def set_up_current_member(self, elem_val, prev_curr: PreviousCurrentHighway):
        prev_curr.first_node_current = way_queries.get_start_node(elem_val)
        prev_curr.last_node_current = way_queries.get_end_node(elem_val)
        prev_curr.current_ref = way_queries.get_way_ref(elem_val)
        return prev_curr

    def check_rails_if_the_ways_are_not_connected(self, prev_curr):
        if prev_curr.first_node_previous != "" and prev_curr.last_node_previous != "" \
                and not way_queries.check_connectivity(
                prev_curr.first_node_previous, prev_curr.last_node_previous,
                prev_curr.first_node_current, prev_curr.last_node_current):
            return True
        return False
