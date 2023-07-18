#!/usr/bin/python3
import dataclasses

from src.lib.model.previous_current import PreviousCurrentMultipolygon
from src.lib.model.error_hwy import ErrorMultipolygon
from src.lib.analyzer.analyzer_base import AnalyzerBase
from src.lib import way_queries


class MultipolygonAnalyzer(AnalyzerBase):
    def checking(self, relation_info: dict):
        """

        :param relation_info: The relation's information regarding order of ways, attributes of ways, nodes and other important things
        :param error_information: It contains all the errors that the analyzer detects
        :return: error_information, number_of_correct_ways
        """
        error_information = []
        ways_to_search = relation_info["ways_to_search"]
        outer_index = 0
        count_members_that_arent_ways = 0
        while way_queries.get_relation_member_type(ways_to_search[outer_index]) != "way":
            outer_index += 1
            count_members_that_arent_ways += 1
        nodes_of_first_way_of_the_area = way_queries.get_nodes(
            ways_to_search[outer_index])  # the nodes of the area's first way
        ref_of_first_way_of_the_area = way_queries.get_way_ref(ways_to_search[outer_index])
        prev_curr = PreviousCurrentMultipolygon(nodes_of_first_way_of_the_area=
                                                nodes_of_first_way_of_the_area,
                                                ref_of_first_way_of_the_area=
                                                ref_of_first_way_of_the_area)
        for index, elem_val in enumerate(ways_to_search):
            # current = current way, previous = previous way
            if way_queries.get_relation_member_type(elem_val) == "way":
                self.__set_current_member__(elem_val, index, prev_curr, ways_to_search)

                error_information = self.check_if_current_way_has_no_role(error_information,
                                                                          prev_curr)
                error_information = self.check_if_the_only_polygon_consists_of_one_way(
                    index, ways_to_search, prev_curr, error_information)
                error_information, prev_curr = self.check_if_way_is_continuous_or_not(
                    prev_curr, error_information, index, ways_to_search, elem_val)
                self.__set_previous_member__(prev_curr)
        correct_ways_count = len(ways_to_search) - len(
            error_information) - count_members_that_arent_ways
        return error_information, correct_ways_count, 0

    def __set_previous_member__(self, prev_curr):
        prev_curr.first_node_previous = prev_curr.first_node_current
        prev_curr.last_node_previous = prev_curr.last_node_current
        prev_curr.previous_role = prev_curr.current_role
        prev_curr.previous_ref = prev_curr.current_ref

    def __set_current_member__(self, elem_val, index, prev_curr, ways_to_search):
        prev_curr.first_node_current = way_queries.get_start_node(elem_val)
        prev_curr.last_node_current = way_queries.get_end_node(elem_val)
        prev_curr.current_role = way_queries.get_role(elem_val)
        prev_curr.current_ref = way_queries.get_way_ref(elem_val)
        prev_curr.currently_sought_role = way_queries.get_role(ways_to_search[index])

    def check_if_way_is_continuous_or_not(self, previous_current: PreviousCurrentMultipolygon,
                                          error_information: list, index: int,
                                          ways_to_search: list, elem_val: dict):
        """
        This checks if way is continuous or not, depending on how many members does the area contain
        """
        if previous_current.way_count_of_one_polygon > 1:
            error_information, previous_current = self.check_if_area_consists_of_more_than_one_way(
                error_information, previous_current, index, ways_to_search, elem_val)
        else:
            error_information, previous_current = self.check_if_area_consists_of_one_way(
                error_information, previous_current, index, ways_to_search, elem_val)
        previous_current.way_count_of_one_polygon += 1
        return error_information, previous_current

    def check_if_area_consists_of_one_way(self, error_information, prev_curr, index,
                                          ways_to_search, elem_val):
        """
        This checks if area consists of one piece of way, because if yes, it's a gap.
        """
        # Check if there is no connection at all between the previous and the current area and the
        # previous one has the gap OR both has the gap:
        if not way_queries.check_connectivity(prev_curr.first_node_previous,
                                              prev_curr.last_node_previous,
                                              prev_curr.first_node_current,
                                              prev_curr.last_node_current) and 0 < index:
            if prev_curr.first_node_previous != prev_curr.last_node_previous:
                error_information.append(
                    ErrorMultipolygon(prev_curr, "Gap in an area consisting of one way"))
                prev_curr.nodes_of_first_way_of_the_area = way_queries.get_nodes(
                    elem_val)
                if index == len(ways_to_search) - 1 and prev_curr.first_node_current != \
                        prev_curr.last_node_current:
                    error_information.append(ErrorMultipolygon(dataclasses.replace(prev_curr),
                                                               "Gap in an area consisting of one "
                                                               "way at the end"))
            prev_curr.way_count_of_one_polygon = 0
            prev_curr.currently_sought_role = prev_curr.current_role
        # Check if the previous way connects but the current one doesn't, and it's at the end of
        # the relation.
        elif prev_curr.first_node_previous == prev_curr.last_node_previous and \
                prev_curr.first_node_current != prev_curr.last_node_current and \
                index == len(ways_to_search) - 1 > 0:
            error_information.append(
                ErrorMultipolygon(prev_curr,
                                  "Gap in an area consisting of one way at the end"))
        # Check if the way area consists of two ways only
        elif not self.check_way_closedness_for_two_ways(prev_curr.first_node_previous,
                                                        prev_curr.last_node_previous,
                                                        prev_curr.first_node_current,
                                                        prev_curr.last_node_current) \
                and index == len(ways_to_search) - 1 > 0:
            error_information.append(
                ErrorMultipolygon(dataclasses.replace(prev_curr),
                                  "Gap in multi way multipolygon at the end"))
        return error_information, prev_curr

    def check_if_area_consists_of_more_than_one_way(self, error_information, prev_curr,
                                                    index, ways_to_search, elem_val):
        """
        This checks the gaps in area if it consists more than a way.
        """
        # If we're at the second way, which is basically after the first two, check if those two connect together:
        if not way_queries.check_connectivity(prev_curr.first_node_previous,
                                              prev_curr.last_node_previous,
                                              prev_curr.first_node_current,
                                              prev_curr.last_node_current) and \
                1 < index < len(ways_to_search) - 1:
            prev_curr = self.check_if_previous_area_is_not_connecting(
                error_information, index, elem_val, prev_curr)
        # Check if we're at the last way. if the polygon's last item isn't connecting to the first item,
        # then it's an error.
        elif index == len(ways_to_search) - 1 > 0 and prev_curr.way_count_of_one_polygon > \
                1 and not \
                self.check_way_closedness_for_more_than_two_ways(
                    prev_curr.nodes_of_first_way_of_the_area[0],
                    prev_curr.nodes_of_first_way_of_the_area[-1],
                    prev_curr.first_node_current, prev_curr.last_node_current) and \
                prev_curr.current_role == prev_curr.currently_sought_role:
            error_information.append(
                ErrorMultipolygon(dataclasses.replace(prev_curr),
                                  "Gap in multi way multipolygon at the end"))
        return error_information, prev_curr

    def check_if_previous_area_is_not_connecting(self, error_information,
                                                 index, elem_val, previous_current):
        """This method checks if the previous area (because now we detected we are detecting a
        new area) is not connecting."""
        # If the previous two ways aren't connecting to each other, and now we are detecting another
        # area:
        if previous_current.way_count_of_one_polygon == 2 and not \
                self.check_way_closedness_for_two_ways(
                    previous_current.nodes_of_first_way_of_the_area[0],
                    previous_current.nodes_of_first_way_of_the_area[-1],
                    previous_current.first_node_previous, previous_current.last_node_previous) and \
                index > 1:
            previous_current.way_count_of_one_polygon = 0
            previous_current.nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
            previous_current.currently_sought_role = previous_current.current_role
            error_information.append(ErrorMultipolygon(dataclasses.replace(previous_current),
                                                       "Gap in multi way multipolygon"))
        elif previous_current.way_count_of_one_polygon > 2 and not \
                self.check_way_closedness_for_more_than_two_ways(
                    previous_current.nodes_of_first_way_of_the_area[0],
                    previous_current.nodes_of_first_way_of_the_area[-1],
                    previous_current.first_node_previous, previous_current.last_node_previous) and \
                index > 1:
            previous_current.way_count_of_one_polygon = 0
            previous_current.nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
            previous_current.currently_sought_role = previous_current.current_role
            error_information.append(ErrorMultipolygon(dataclasses.replace(previous_current),
                                                       "Gap in multi way multipolygon"))
        # If the series of ways are connecting (#of ways > 2, and now we are detecting another area:
        elif previous_current.way_count_of_one_polygon > 2 and \
                self.check_way_closedness_for_more_than_two_ways(
                    previous_current.nodes_of_first_way_of_the_area[0],
                    previous_current.nodes_of_first_way_of_the_area[-1],
                    previous_current.first_node_previous, previous_current.last_node_previous) \
                and index > 2:
            previous_current.way_count_of_one_polygon = 0
            previous_current.nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
            previous_current.currently_sought_role = previous_current.current_role
        # If we are detecting a new area but the way count is only two
        elif previous_current.way_count_of_one_polygon == 2 and \
                self.check_way_closedness_for_two_ways(
                    previous_current.nodes_of_first_way_of_the_area[0],
                    previous_current.nodes_of_first_way_of_the_area[-1],
                    previous_current.first_node_previous, previous_current.last_node_previous) \
                and index > 1:
            previous_current.way_count_of_one_polygon = 0
            previous_current.nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
            previous_current.currently_sought_role = previous_current.current_role
        return previous_current

    def check_if_the_only_polygon_consists_of_one_way(self,
                                                      index, ways_to_search, previous_current,
                                                      error_information):
        if index == len(ways_to_search) - 1 == 0 and previous_current.first_node_current != \
                previous_current.last_node_current:
            error_information.append(ErrorMultipolygon(dataclasses.replace(previous_current),
                                                       "Gap in an area consisting of one way"))
        return error_information

    def check_way_closedness_for_two_ways(self, first_node_previous: str, last_node_previous: str,
                                          first_node_current: str,
                                          last_node_current: str):
        """
        This method checks if the area consisting of two ways are closed, so they are connected
        some how (so both ways make its own "circle"- two separate areas, or those both ways
        connect to each other, so again, the area is closed)

        :param first_node_previous: Previous way's first node.
        :param last_node_previous: Previous way's last node.
        :param first_node_current: Current way's first node.
        :param last_node_current: Current way's last node.
        :return:
        """
        return ((first_node_current == last_node_previous and first_node_previous == last_node_current) or
                (first_node_previous == last_node_previous and first_node_current == last_node_current) or
                (first_node_previous == last_node_current and first_node_current == last_node_previous)
                or (first_node_previous == first_node_current and last_node_previous == last_node_current))

    def check_way_closedness_for_more_than_two_ways(self, first_node_previous: str,
                                                    last_node_previous: str,
                                                    first_node_current: str,
                                                    last_node_current: str):
        """
        This method checks for an area consisting of more than 2 ways if the two end ways(areas)
        aren't closed, so they go in a continuous unclosed line.

        :param first_node_previous: Previous way's first node.
        :param last_node_previous: Previous way's last node.
        :param first_node_current: Current way's first node.
        :param last_node_current: Current way's last node.
        :return:
        """
        return ((first_node_current == last_node_previous and
                 first_node_previous != last_node_current) or
                (first_node_previous == last_node_previous and
                 first_node_current != last_node_current) or
                (first_node_current == last_node_current and
                 first_node_previous != last_node_previous) or
                (first_node_previous == last_node_current and
                 first_node_current != last_node_previous))

    def check_if_current_way_has_no_role(self, error_information: list[ErrorMultipolygon],
                                         prev_curr: PreviousCurrentMultipolygon):
        """
        Checks if the current way has no role assigned in the relation. JOSM doesn't say anything
        if there is no role, just if you assigned the wrong role - although that requires a
        geometry analyzing tool, to determine if the outer or inner is swapped
        """
        if prev_curr.current_role == "":
            error_information.append(ErrorMultipolygon(dataclasses.replace(prev_curr), "No role"))
        return error_information
