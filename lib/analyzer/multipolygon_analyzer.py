#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from previous_current import PreviousCurrentMultipolygon
from error_hwy import ErrorMultipolygon
import way_queries


class MultipolygonAnalyzer:
    def multipolygon_checking(self, relation_info: dict, error_information: list):
        """

        :param relation_info: The relation's information regarding order of ways, attributes of ways, nodes and other important things
        :param error_information: It contains all the errors that the analyzer detects
        :return: error_information, number_of_correct_ways
        """
        ways_to_search = relation_info["ways_to_search"]
        index = 0
        count_members_that_arent_ways = 0
        while way_queries.get_relation_member_type(ways_to_search[index]) != "way":
            index += 1
            count_members_that_arent_ways += 1
        currently_sought_role = way_queries.get_role(ways_to_search[index])
        nodes_of_first_way_of_the_area = way_queries.get_nodes(
            ways_to_search[index])  # the nodes of the area's first way
        ref_of_first_way_of_the_area = way_queries.get_way_ref(ways_to_search[index])
        first_node_previous = last_node_previous = previous_role = previous_ref = ""
        way_count_of_one_polygon = 0
        ways_to_search_length = len(ways_to_search)
        for index, elem_val in enumerate(ways_to_search):
            # current = current way, previous = previous way
            if way_queries.get_relation_member_type(elem_val) == "way":
                first_node_current = way_queries.get_start_node(elem_val)
                last_node_current = way_queries.get_end_node(elem_val)
                current_ref = way_queries.get_way_ref(elem_val)
                current_role = way_queries.get_role(elem_val)
                previous_current = PreviousCurrentMultipolygon(first_node_previous=first_node_previous,
                                                               first_node_current=first_node_current,
                                                               last_node_previous=last_node_previous,
                                                               last_node_current=last_node_current,
                                                               previous_role=previous_role,
                                                               previous_ref=previous_ref,
                                                               current_role=current_role,
                                                               current_ref=current_ref,
                                                               currently_sought_role_first_member_nodes=nodes_of_first_way_of_the_area,
                                                               currently_sought_role=currently_sought_role,
                                                               ref_of_first_way_of_the_area=ref_of_first_way_of_the_area)
                error_information = self.check_if_current_way_has_no_role(current_role, error_information,
                                                                          previous_current)
                error_information = self.check_if_the_only_polygon_consists_of_one_way(
                    first_node_current,
                    last_node_current,
                    index, ways_to_search_length,
                    previous_current,
                    error_information)
                error_information, currently_sought_role, nodes_of_first_way_of_the_area, ref_of_first_way_of_the_area, \
                    way_count_of_one_polygon \
                    = self.check_if_way_is_continuous_or_not(first_node_previous, last_node_previous,
                                                             first_node_current, last_node_current,
                                                             current_role, previous_current,
                                                             error_information, currently_sought_role,
                                                             nodes_of_first_way_of_the_area,
                                                             ref_of_first_way_of_the_area, way_count_of_one_polygon,
                                                             index, ways_to_search_length, elem_val)
                first_node_previous = first_node_current
                last_node_previous = last_node_current
                previous_role = current_role
                previous_ref = current_ref
        correct_ways_count = ways_to_search_length - len(error_information) - count_members_that_arent_ways
        return error_information, correct_ways_count

    def check_if_way_is_continuous_or_not(self, first_node_previous: str, last_node_previous: str,
                                          first_node_current: str,
                                          last_node_current: str, current_role: str,
                                          previous_current: PreviousCurrentMultipolygon,
                                          error_information: list, currently_sought_role: str,
                                          nodes_of_first_way_of_the_area: list,
                                          ref_of_first_way_of_the_area: str, way_count_of_one_polygon: int, index: int,
                                          ways_to_search_length: int, elem_val: dict):
        if way_count_of_one_polygon > 1:
            error_information, way_count_of_one_polygon = self.check_if_area_consists_of_more_than_one_way(
                first_node_previous, last_node_previous, first_node_current,
                last_node_current, nodes_of_first_way_of_the_area, error_information,
                way_count_of_one_polygon, previous_current, index, ways_to_search_length, currently_sought_role,
                current_role, elem_val)
        else:
            error_information, way_count_of_one_polygon = self.check_if_area_consists_of_one_way(
                first_node_previous, last_node_previous, first_node_current,
                last_node_current, nodes_of_first_way_of_the_area, error_information,
                way_count_of_one_polygon, previous_current, index, ways_to_search_length, currently_sought_role,
                current_role, elem_val)
        way_count_of_one_polygon += 1
        return error_information, currently_sought_role, nodes_of_first_way_of_the_area, ref_of_first_way_of_the_area, \
            way_count_of_one_polygon

    def check_if_area_consists_of_one_way(self, first_node_previous, last_node_previous, first_node_current,
                                          last_node_current, nodes_of_first_way_of_the_area, error_information,
                                          way_count_of_one_polygon, previous_current, index,
                                          ways_to_search_length, currently_sought_role, current_role, elem_val):
        # Check if there is no connection at all between the previous and the current area and the previous one has the gap OR both has the gap:
        if not way_queries.check_connectivity(first_node_previous, last_node_previous, first_node_current,
                                              last_node_current) and 0 < index:
            if first_node_previous != last_node_previous:
                error_information.append(ErrorMultipolygon(previous_current, "Gap in an area consisting of one way"))
            if index == ways_to_search_length - 1 and first_node_current != last_node_current:
                error_information.append(
                    ErrorMultipolygon(previous_current, "Gap in an area consisting of one way at the end"))
            way_count_of_one_polygon = 0
        # Check if the previous way connects but the current one doesn't and it's at the end of the relation.
        elif first_node_previous == last_node_previous and first_node_current != last_node_current and \
                index == ways_to_search_length - 1 > 0:
            error_information.append(
                ErrorMultipolygon(previous_current, "Gap in an area consisting of one way at the end"))
        # Check if the way area consists of two ways only
        elif not self.check_way_closedness_for_two_ways(first_node_previous, last_node_previous, first_node_current,
                                                        last_node_current) and index == ways_to_search_length - 1 > 0:
            error_information.append(
                ErrorMultipolygon(previous_current, "Gap in multi way multipolygon at the end"))
        return error_information, way_count_of_one_polygon

    def check_if_area_consists_of_more_than_one_way(self, first_node_previous, last_node_previous, first_node_current,
                                                    last_node_current, nodes_of_first_way_of_the_area,
                                                    error_information,
                                                    way_count_of_one_polygon, previous_current, index,
                                                    ways_to_search_length, currently_sought_role, current_role,
                                                    elem_val):
        # If we're at the second way, which is basically after the first two, check if those two connect together:
        if not way_queries.check_connectivity(first_node_previous, last_node_previous, first_node_current,
                                              last_node_current) and 1 < index < ways_to_search_length - 1:
            way_count_of_one_polygon, nodes_of_first_way_of_the_area = self.check_if_previous_area_is_not_connecting(
                error_information, first_node_previous, index, elem_val, last_node_previous,
                nodes_of_first_way_of_the_area,
                previous_current, way_count_of_one_polygon)
        # Check if we're at the last way. if the polygon's last item isn't connecting to the first item,
        # then it's an error.
        elif index == ways_to_search_length - 1 > 0 and way_count_of_one_polygon == 1 and not self.check_way_closedness_for_two_ways(
                nodes_of_first_way_of_the_area[0],
                nodes_of_first_way_of_the_area[-1],
                first_node_current, last_node_current) and current_role == currently_sought_role:
            error_information.append(ErrorMultipolygon(previous_current, "Gap in multi way multipolygon at the end"))
        elif index == ways_to_search_length - 1 > 0 and way_count_of_one_polygon > 1 and not self.check_way_closedness_for_more_than_two_ways(
                nodes_of_first_way_of_the_area[0],
                nodes_of_first_way_of_the_area[-1],
                first_node_current, last_node_current) and current_role == currently_sought_role:
            error_information.append(ErrorMultipolygon(previous_current, "Gap in multi way multipolygon at the end"))
        return error_information, way_count_of_one_polygon

    def check_if_previous_area_is_not_connecting(self, error_information, first_node_previous,
                                                 index, elem_val,
                                                 last_node_previous,
                                                 nodes_of_first_way_of_the_area,
                                                 previous_current, way_count_of_one_polygon):
        # If the previous two ways aren't connecting to each other:
        if way_count_of_one_polygon == 2 and not self.check_way_closedness_for_two_ways(
                nodes_of_first_way_of_the_area[0],
                nodes_of_first_way_of_the_area[-1],
                first_node_previous, last_node_previous) and index > 1:
            way_count_of_one_polygon = 0
            nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
            error_information.append(ErrorMultipolygon(previous_current, "Gap in multi way multipolygon"))
        # If the series of ways(# of ways greater than 2) don't make a closed polygon:
        elif way_count_of_one_polygon > 2 and not self.check_way_closedness_for_more_than_two_ways(
                nodes_of_first_way_of_the_area[0],
                nodes_of_first_way_of_the_area[-1],
                first_node_previous, last_node_previous) and index > 1:
            way_count_of_one_polygon = 0
            nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
            error_information.append(ErrorMultipolygon(previous_current, "Gap in multi way multipolygon"))
        # If the series of ways are connecting (#of ways > 2, and now we are detecting another polygon:
        elif way_count_of_one_polygon > 2 and self.check_way_closedness_for_more_than_two_ways(
                nodes_of_first_way_of_the_area[0],
                nodes_of_first_way_of_the_area[-1],
                first_node_previous, last_node_previous) and index > 2:
            way_count_of_one_polygon = 0
            nodes_of_first_way_of_the_area = way_queries.get_nodes(
                elem_val)
        return way_count_of_one_polygon, nodes_of_first_way_of_the_area

    def check_if_the_only_polygon_consists_of_one_way(self, first_node_current,
                                                      last_node_current,
                                                      index, ways_to_search_length, previous_current,
                                                      error_information):
        if index == ways_to_search_length - 1 == 0 and first_node_current != last_node_current:
            error_information.append(ErrorMultipolygon(previous_current, "Gap in multipolygon"))
        return error_information

    def check_way_closedness_for_two_ways(self, first_node_previous: str, last_node_previous: str,
                                          first_node_current: str,
                                          last_node_current: str):
        """
        This method checks if the two ways(areas) aren't closed, so they go in a continuous unclosed line.
        (not a circle to be precise but like an arrow or something)

        :param first_node_previous: Previous way's first node.
        :param last_node_previous: Previous way's last node.
        :param first_node_current: Current way's first node.
        :param last_node_current: Current way's last node.
        :return:
        """
        return ((first_node_current == last_node_previous and first_node_previous == last_node_current) or
                (first_node_previous == last_node_previous and first_node_current == last_node_current) or
                (first_node_current == last_node_current and first_node_previous == last_node_previous) or
                (first_node_previous == last_node_current and first_node_current == last_node_previous))

    def check_way_closedness_for_more_than_two_ways(self, first_node_previous: str, last_node_previous: str,
                                                    first_node_current: str,
                                                    last_node_current: str):
        """
        This method checks if the two end ways(areas) aren't closed, so they go in a continuous unclosed line.
        (not a circle to be precise but like an arrow or something)

        :param first_node_previous: Previous way's first node.
        :param last_node_previous: Previous way's last node.
        :param first_node_current: Current way's first node.
        :param last_node_current: Current way's last node.
        :return:
        """
        return ((first_node_current == last_node_previous and first_node_previous != last_node_current) or
                (first_node_previous == last_node_previous and first_node_current != last_node_current) or
                (first_node_current == last_node_current and first_node_previous != last_node_previous) or
                (first_node_previous == last_node_current and first_node_current != last_node_previous))

    def check_if_current_way_has_no_role(self, current_role: str, error_information: ErrorMultipolygon,
                                         previous_current: PreviousCurrentMultipolygon):
        if current_role == "":
            error_information.append(ErrorMultipolygon(previous_current, "No role"))
            # JOSM doesn't say anything if there is no role, just if you assigned the wrong role
            # - although that requires a geometry analyzing tool, to determine if the outer or inner is swapped
        return error_information
