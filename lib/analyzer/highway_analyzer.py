#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from previous_current import PreviousCurrentHighway
from error_hwy import ErrorHighway
from analyzer_base import AnalyzerBase
import way_queries


class HighwayAnalyzer(AnalyzerBase):
    # good for highway=* tags (primary, secondary, etc. and even trails and cycle routes)
    def checking(self, relation_info: dict, error_information: list):
        """Highway checking. This is where the gaps for a highway is checked. For unit tests, this should be only
        used if a complete relation is about to be tested."""
        role_of_first_way = way_queries.get_role(relation_info["ways_to_search"][0])
        route_number = way_queries.get_ref_of_the_route(relation_info)
        network = way_queries.get_network(relation_info)
        index_of_current_way = 0
        count_of_forward_roled_way_series = 0
        pieces_of_roundabout = 0
        the_amount_to_be_decreased_from_length_of_error_information = 0
        motorway_split_way = previous_oneway = previous_roundabout = has_directional_roles = False
        is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation_info)
        last_forward_way_before_backward_direction = previous_nodes = last_roundabout_nodes = []
        roundabout_ways = []
        # last_forward_way_before_backward_direction:  when we have relation beginning with forward ways
        # (separated highway) connencting to a point
        first_node_previous = last_node_previous = previous_role = previous_ref = previous_highway \
            = first_node_of_first_forward_way_in_the_series = last_node_of_first_forward_way_in_the_series = ""
        for elem_val in relation_info["ways_to_search"]:
            if "nd" in elem_val and "tag" in elem_val:
                length_of_error_information_at_the_beginning_of_iteration = len(error_information)
                # current = current way, previous = previous way
                first_node_current = way_queries.get_start_node(elem_val)
                last_node_current = way_queries.get_end_node(elem_val)
                current_roundabout = way_queries.is_roundabout(elem_val)
                current_highway = way_queries.get_highway(elem_val)
                current_oneway = way_queries.is_oneway(elem_val)
                current_ref = way_queries.get_way_ref(elem_val)
                current_role = way_queries.get_role(elem_val)
                current_nodes = way_queries.get_nodes(elem_val)
                previous_current = PreviousCurrentHighway(currently_checked_ref=route_number,
                                                          last_forward_way_before_backward_direction=last_forward_way_before_backward_direction,
                                                          first_node_previous=first_node_previous,
                                                          first_node_current=first_node_current,
                                                          last_node_previous=last_node_previous,
                                                          last_node_current=last_node_current,
                                                          previous_role=previous_role,
                                                          previous_roundabout=previous_roundabout,
                                                          previous_oneway=previous_oneway, previous_ref=previous_ref,
                                                          previous_highway=previous_highway, current_role=current_role,
                                                          current_roundabout=current_roundabout,
                                                          current_oneway=current_oneway, current_ref=current_ref,
                                                          current_highway=current_highway)

                # This is where swaps and other stuff happen firstly.
                first_node_current, last_node_current, current_role, current_nodes = self.is_role_backward(
                    first_node_current, last_node_current,
                    current_role, current_nodes)

                last_roundabout_nodes, roundabout_ways, error_information = self.is_way_roundabout(current_roundabout,
                                                                                                   current_role,
                                                                                                   current_nodes,
                                                                                                   current_ref,
                                                                                                   roundabout_ways,
                                                                                                   last_roundabout_nodes,
                                                                                                   error_information,
                                                                                                   previous_current)
                error_information = self.determine_role_errors_at_the_beginning_highway(index_of_current_way, current_role,
                                                                                        current_oneway,
                                                                                        current_highway, current_roundabout,
                                                                                        error_information, previous_current)

                first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, count_of_forward_roled_way_series = \
                    self.is_the_way_in_forward_way_series(
                        index_of_current_way, previous_role, current_role, count_of_forward_roled_way_series,
                        first_node_current, last_node_current,
                        first_node_of_first_forward_way_in_the_series,
                        last_node_of_first_forward_way_in_the_series)
                # Checking for the gaps.
                has_directional_roles, error_information = self.check_if_there_is_gap_at_the_beginning(index_of_current_way,
                                                                                                       count_of_forward_roled_way_series,
                                                                                                       role_of_first_way,
                                                                                                       is_mutcd_country,
                                                                                                       previous_role,
                                                                                                       current_role,
                                                                                                       first_node_previous,
                                                                                                       first_node_current,
                                                                                                       last_node_previous,
                                                                                                       last_node_current,
                                                                                                       last_forward_way_before_backward_direction,
                                                                                                       has_directional_roles,
                                                                                                       error_information,
                                                                                                       previous_current)

                pieces_of_roundabout, error_information = self.determine_roundabout_errors_and_number(index_of_current_way,
                                                                                                      previous_roundabout,
                                                                                                      current_roundabout,
                                                                                                      current_role,
                                                                                                      previous_current,
                                                                                                      error_information,
                                                                                                      pieces_of_roundabout,
                                                                                                      count_of_forward_roled_way_series,
                                                                                                      last_node_previous,
                                                                                                      last_node_current,
                                                                                                      first_node_current)

                last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information = self.check_if_way_connects_continuously(
                    relation_info["ways_to_search"], previous_highway, previous_nodes, current_nodes, index_of_current_way,
                    first_node_previous, last_node_previous, first_node_current, last_node_current, previous_role,
                    current_role,
                    previous_oneway, previous_roundabout, current_roundabout, current_oneway, is_mutcd_country,
                    role_of_first_way, has_directional_roles, error_information, previous_current,
                    first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
                    motorway_split_way, count_of_forward_roled_way_series, current_highway, current_highway,
                    route_number, network, previous_ref, last_roundabout_nodes)
                first_node_previous = first_node_current
                last_node_previous = last_node_current
                previous_roundabout = current_roundabout
                previous_nodes = current_nodes
                previous_oneway = current_oneway
                previous_role = current_role
                previous_highway = current_highway
                previous_ref = current_ref
                index_of_current_way += 1
                error_information = self.check_if_motorway_not_split(motorway_split_way, index_of_current_way,
                                                                     len(relation_info["ways_to_search"]),
                                                                     current_highway, route_number, network,
                                                                     current_role, error_information, previous_current)
                if len(error_information) - length_of_error_information_at_the_beginning_of_iteration > 1:
                    the_amount_to_be_decreased_from_length_of_error_information += 1
        correct_ways_count = len(relation_info["ways_to_search"]) - len(
            error_information) + the_amount_to_be_decreased_from_length_of_error_information
        return error_information, correct_ways_count

    def is_role_backward(self, first_node_current: str, last_node_current: str, current_role: str, current_nodes: list):
        """Is it a backward way? if yes, just replace the first and last node, and make it "believe" that
         it's a forward way due to the replacement. (so we won't touch original array)

        **Returns** either first_node_current, last_node_current or last_node_current, first_node_current depending on role.
        """
        if current_role == "backward":
            current_role = "forward"
            nodes = current_nodes[::-1]
            return last_node_current, first_node_current, current_role, nodes
        return first_node_current, last_node_current, current_role, current_nodes

    def is_way_roundabout(self, current_roundabout: bool, current_role: str, current_nodes: list,
                          current_ref: str, roundabout_ways: list, last_roundabout_nodes: list, error_information: list,
                          prev_curr: PreviousCurrentHighway):
        """Is the current way a roundabout? if yes, collect all its nodes' reference number

        **Returns**: last_roundabout_nodes
        """
        if current_roundabout:
            if current_ref in roundabout_ways:
                error_information.append(ErrorHighway(prev_curr, "Duplicated roundabout ways"))
            roundabout_ways.append(current_ref)
        if current_role == "" and current_roundabout is True:
            return current_nodes, roundabout_ways, error_information
        return last_roundabout_nodes, roundabout_ways, error_information  # we don't change its value.

    def is_the_way_in_forward_way_series(self, index_of_current_way: int, previous_role: str, current_role: str,
                                         count_of_forward_roled_way_series: int, first_node_current: str,
                                         last_node_current: str,
                                         first_node_of_first_forward_way_in_the_series: str,
                                         last_node_of_first_forward_way_in_the_series: str):
        """Is the current way going into a series of forward ways or
        does it start with a forward way?

        If yes, save its first and last node
        and increase the count of the forward ways

        **Returns**: first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, count_of_forward_roled_way_series
        """
        if (index_of_current_way > 0 and previous_role == "" and current_role == "forward") or \
                (index_of_current_way == 0 and current_role == "forward"):
            first_node_of_first_forward_way_in_the_series = first_node_current
            last_node_of_first_forward_way_in_the_series = last_node_current
            count_of_forward_roled_way_series += 1
        elif previous_role == "forward" and current_role == "forward":
            count_of_forward_roled_way_series += 1
        return first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, count_of_forward_roled_way_series

    def check_if_there_is_gap_at_the_beginning(self, index_of_current_way: int,
                                               count_of_forward_roled_way_series: int,
                                               role_of_first_way: str, is_mutcd_country: bool, previous_role: str,
                                               current_role: str, first_node_previous: str, first_node_current: str,
                                               last_node_previous: str, last_node_current: str,
                                               last_forward_way_before_backward_direction: list,
                                               has_directional_roles: bool, error_information: list,
                                               previous_current: PreviousCurrentHighway):
        """
        Is the following way in the first forward way series, the first way is a forward way,
        the previous one is forward too, but the current one isn't a forward way?

        If yes, does the last forward way before going to backward direction have its last point not equal to the
        current way's last node,  even if the last or first nodes previous way(that is member the backward series') is
        equal to the current way's last of first.

        Well if this applies, then the way connection is broken and it means it should be fixed.
        (The other case is not checked when the backward way connects to the rest of the nodes,
        since we know then there's a gap, it's checked a few if statements later)
        """

        if (index_of_current_way > 0 and count_of_forward_roled_way_series == 1 and (
                role_of_first_way == "forward"
                or (is_mutcd_country and way_queries.check_if_directional(role_of_first_way))) and (
                previous_role == "forward" or (is_mutcd_country and way_queries.check_if_directional(previous_role))
                and current_role == "" and len(last_forward_way_before_backward_direction) > 0)):
            return self.__check_last_forward_way_to_connection_with_current_way__(
                last_forward_way_before_backward_direction, first_node_previous, first_node_current, last_node_previous,
                last_node_current, is_mutcd_country, role_of_first_way, previous_role, has_directional_roles,
                error_information, previous_current)
        return has_directional_roles, error_information

    def check_if_mutcd_country_and_directional(self, has_directional_roles, is_mutcd_country, role_of_first_way,
                                               role_of_second_way):

        """MUTCD = Manual on Uniform Traffic Control Devices"""
        if is_mutcd_country and (
                way_queries.check_if_directional(role_of_first_way)
                or way_queries.check_if_directional(role_of_second_way)):
            # we'll notify the user at the end that this relation can be reorganized by splitting it into
            # # two halves. eg: west-east, north-south (this is how they go in the US) - we don't know where
            # the relation starts
            has_directional_roles = True
            # we say that those directional routes are good but in fact not, so we mark this way that
            # we have to reconstruct the route
            return has_directional_roles
        return has_directional_roles

    def __check_last_forward_way_to_connection_with_current_way__(self,
                                                                  last_forward_way_before_backward_direction: list,
                                                                  first_node_previous: str, first_node_current: str,
                                                                  last_node_previous: str, last_node_current: str,
                                                                  is_mutcd_country: bool, role_of_first_way: str,
                                                                  previous_role: str, has_directional_roles: bool,
                                                                  error_information: list,
                                                                  previous_current: PreviousCurrentHighway):

        """This is a helper function to determine that there's a gap at the beginning especially with ways that are
        supposed to be forward would connect to a non-roled way but that way doesn't connect to them at all.

        **Returns**:has_directional_roles, error_information"""
        # Regardless if there is a connection or not, check if the ways have directional roles.
        has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles, is_mutcd_country,
                                                                            role_of_first_way, previous_role)
        if (last_forward_way_before_backward_direction[-1] == last_node_current and (
                last_node_previous == last_node_current
                or first_node_previous == last_node_current)) or (last_forward_way_before_backward_direction[-1]
                                                                  == first_node_current) and (
                first_node_previous == first_node_current or last_node_previous == first_node_current):
            return has_directional_roles, error_information
        else:
            error_information.append(ErrorHighway(prev_curr=previous_current, error_type="Gap at the beginning"))
            return has_directional_roles, error_information

    def determine_roundabout_errors_and_number(self, index_of_current_way: int, previous_roundabout: bool,
                                               current_roundabout: bool, current_role: str,
                                               previous_current: PreviousCurrentHighway,
                                               error_information: list, pieces_of_roundabout: int,
                                               count_of_forward_roled_way_series: int, last_node_previous: str,
                                               last_node_current: str, first_node_current: str):
        if current_roundabout and current_role == "" and first_node_current != last_node_current:
            error_information.append(
                ErrorHighway(previous_current, "Forward role missing at roundabout"))
        if index_of_current_way > 0 and not previous_roundabout and current_roundabout:
            pieces_of_roundabout = 1
            if count_of_forward_roled_way_series == 1:
                error_information.append(
                    ErrorHighway(previous_current, "Only one forward way before closed roundabout"))
            if last_node_previous == last_node_current:
                # this means that the roundabout would go in a weird way (causing an endless loop in the analyzer),
                # this is not good!! It's a gap
                error_information.append(ErrorHighway(previous_current, "Roundabout gap"))
            return pieces_of_roundabout, error_information
        elif index_of_current_way > 0 and previous_roundabout and current_roundabout:
            pieces_of_roundabout += 1
            return pieces_of_roundabout, error_information
        elif index_of_current_way > 0 and previous_roundabout and not current_roundabout:
            pieces_of_roundabout = 0  # this is an important thing, especially at testing
        return pieces_of_roundabout, error_information

    # This is a massive method. You should test it only whenever the methods in it had been thoroughly tested.
    def check_if_way_connects_continuously(self, ways_to_search: list, previous_highway: str, previous_nodes: list,
                                           current_nodes: list,
                                           index_of_current_way: int, first_node_previous: str, last_node_previous: str,
                                           first_node_current: str, last_node_current: str, previous_role: str,
                                           current_role: str, previous_oneway: bool, previous_roundabout: bool,
                                           current_roundabout: bool, current_oneway: bool,
                                           is_mutcd_country: bool, role_of_first_way: str, has_directional_roles: bool,
                                           error_information: list, previous_current: PreviousCurrentHighway,
                                           first_node_of_first_forward_way_in_the_series: str,
                                           last_node_of_first_forward_way_in_the_series: str, motorway_split_way: bool,
                                           count_of_forward_roled_way_series: int,
                                           last_forward_way_before_backward_direction: list, current_highway: str,
                                           route_number: str, network: str, previous_ref: str,
                                           last_roundabout_nodes: list):
        """This checks if the way connects continuously, if yes then check if there are issues with the roling. If
        it's not continuous, then check if it's a roundabout. if it's not a roundabout but a weirdly connected

        **Returns**: last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles,
        error_information

        The returned data may have the same value as before, it depends on the evaluation of the currently checked
        way."""
        # Check if the roundabout's entry way is in wrong order.
        if 0 < index_of_current_way < len(
                ways_to_search) - 2 and last_node_previous == last_node_current and way_queries.is_roundabout(
            ways_to_search[index_of_current_way + 2]):
            error_information.append(ErrorHighway(previous_current, "Wrong order of roundabout entries"))
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        if index_of_current_way > 0 and (
                first_node_previous == first_node_current or first_node_previous == last_node_current
                or last_node_previous == first_node_current or last_node_previous == last_node_current or (
                        previous_roundabout and not current_roundabout and way_queries.roundabout_checker(current_nodes,
                                                                                                          previous_nodes))):
            has_directional_roles, error_information = self.check_role_issues_in_continuous_way(index_of_current_way,
                                                                                                previous_highway,
                                                                                                previous_role,
                                                                                                current_role,
                                                                                                previous_oneway,
                                                                                                current_oneway,
                                                                                                is_mutcd_country,
                                                                                                role_of_first_way,
                                                                                                has_directional_roles,
                                                                                                last_forward_way_before_backward_direction,
                                                                                                previous_nodes,
                                                                                                error_information,
                                                                                                previous_current,
                                                                                                count_of_forward_roled_way_series)
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        # If the way is not continuous, because the end and starting nodes are different of the two ways, let's try it
        # at roundabouts, and find the node in it (this only works if the roundabout is coming right after
        # (or right before) in order of relation):
        elif index_of_current_way > 0 and (
                previous_roundabout and not current_roundabout or (not previous_roundabout and current_roundabout)):
            good_roundabout = way_queries.roundabout_checker(current_nodes,
                                                             previous_nodes)
            if not good_roundabout and not (previous_role != "forward" and not previous_oneway and not previous_roundabout):
                error_information.append(
                    ErrorHighway(previous_current, "Roundabout gap"))
            elif not good_roundabout:
                error_information.append(
                    ErrorHighway(previous_current, "Roundabout gap"))  # this exists - coverage increases
            # this case is not covered yet when good_roundabout is true..
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        # Special case, when there are a bunch of oneway roads connecting in weird order in the relation (2x2 lane road
        # to 2x2 separate highway, opposite of the starting 2x2 separate to 2x2 merged)
        elif index_of_current_way > 0 and (previous_role == "forward"
                                           or (is_mutcd_country and way_queries.check_if_directional(current_role))):
            has_directional_roles_local = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                      is_mutcd_country, previous_role,
                                                                                      current_role)
            last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information = self.check_the_situation_with_2_by_2_highways(
                is_mutcd_country, has_directional_roles_local, first_node_current, last_node_current,
                first_node_of_first_forward_way_in_the_series,
                last_node_of_first_forward_way_in_the_series, role_of_first_way,
                count_of_forward_roled_way_series, last_forward_way_before_backward_direction, current_highway,
                route_number, network, motorway_split_way, error_information, previous_current, previous_ref,
                last_roundabout_nodes, current_nodes, previous_nodes)
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        elif index_of_current_way > 0:
            # It's definitely a gap
            error_information.append(ErrorHighway(previous_current, "Gap"))
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        else:
            # default case, when we are at the first way.. we don't change anything
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information

    def check_role_issues_in_continuous_way(self, index_of_current_way: int, previous_highway: str, previous_role: str,
                                            current_role: str, previous_oneway: bool, current_oneway: bool,
                                            is_mutcd_country: bool, role_of_first_way: str, has_directional_roles: bool,
                                            last_forward_way_before_backward_direction: list, previous_nodes: list,
                                            error_information: list, previous_current: PreviousCurrentHighway,
                                            count_of_forward_roled_way_series):
        """This checks if the way has issues with the roles or determine if the way is in a country which uses
        NORTH / SOUTH / WEST / EAST on the signs (cardinal direction).

        **Returns**: has_directional_roles, error_information
        """
        if current_role == "" and not current_oneway:
            # This way is a normal way, but then we need to check its pattern
            # Since if it's oneway, it's not correct (there are chances though that it's alright, ex. it starts with a
            # oneway road due to road works but in this case NO)
            return self.condition_forward_no_oneway_in_non_forward_series(index_of_current_way, previous_highway,
                                                                          previous_role,
                                                                          previous_oneway, is_mutcd_country,
                                                                          role_of_first_way, has_directional_roles,
                                                                          last_forward_way_before_backward_direction,
                                                                          previous_nodes,
                                                                          error_information, previous_current,
                                                                          count_of_forward_roled_way_series)
        elif ((current_role == "forward" or (
                is_mutcd_country and way_queries.check_if_directional(current_role)))) and current_oneway:
            # We know all oneways are forward
            has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                is_mutcd_country, current_role,
                                                                                current_role)
            return has_directional_roles, error_information
        elif (current_role == "forward" or (
                is_mutcd_country and way_queries.check_if_directional(current_role))) and not current_oneway:
            # If we didn't run into the issue above, then it means the way is probably at a roundabout or
            # something, so it's not a big problem
            has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                is_mutcd_country, current_role,
                                                                                current_role)
            return has_directional_roles, error_information
        else:
            # it runs whenever there's no role for oneway OR it's oneway but its role is not forward / cardinal role.
            error_information.append(ErrorHighway(previous_current, "Wrong role setup"))
            return has_directional_roles, error_information

    def condition_forward_no_oneway_in_non_forward_series(self, index_of_current_way: int, previous_highway: str,
                                                          previous_role: str,
                                                          previous_oneway: bool, is_mutcd_country: bool,
                                                          role_of_first_way: str, has_directional_roles: bool,
                                                          last_forward_way_before_backward_direction: list,
                                                          previous_nodes: list,
                                                          error_information: list,
                                                          previous_current: PreviousCurrentHighway,
                                                          count_of_forward_roled_way_series=int):
        """Case: NNFN - this is a bad case because in the case of 2x1 lane motorways there's no ability to go backwards
        (or can be FFFN etc - since you can't traverse backwards then in the case of 2x1 - or if the forward series consists of only 1 members
         - worst case! then it's an error for sure, no ability to return, this is for all types of roads)

        The roundabout checker shouldn't deceive you, I don't want to rename that method since it's used for roundabout connection from multiple nodes.
        F= Forward N = Not oneway
        """
        if index_of_current_way > 1 \
                and ((previous_role == "forward" or
                      (is_mutcd_country and way_queries.check_if_directional(previous_role))) and (
                             previous_highway == "motorway" or count_of_forward_roled_way_series == 1)
                     and not previous_oneway and (len(last_forward_way_before_backward_direction)
                                                  == 0 or (len(
                            last_forward_way_before_backward_direction) > 1 and not
                                                           way_queries.roundabout_checker(
                                                               last_forward_way_before_backward_direction[-1],
                                                               previous_nodes)))):
            has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                is_mutcd_country, role_of_first_way,
                                                                                previous_role)
            # This checks if before the current way there is a forward way without oneway, and before that there are
            # two ways without any role and oneway, if this is true then it's a bad way.
            error_information.append(ErrorHighway(prev_curr=previous_current,
                                                  error_type="Forward and non-oneway without ability to move backward"))
            return has_directional_roles, error_information
        elif index_of_current_way < 2:
            # there is no problem with the way since the pattern only happens if it's the case mentioned
            #  in this method's pydoc.
            return has_directional_roles, error_information
        return has_directional_roles, error_information

    def check_the_situation_with_2_by_2_highways(self, is_mutcd_country: bool,
                                                 has_directional_roles: bool,
                                                 first_node_current: str,
                                                 last_node_current: str,
                                                 first_node_of_first_forward_way_in_the_series: str,
                                                 last_node_of_first_forward_way_in_the_series: str,
                                                 role_of_first_way: str,
                                                 count_of_forward_roled_way_series: int,
                                                 last_forward_way_before_backward_direction: list,
                                                 current_highway: str,
                                                 route_number: str,
                                                 network: str,
                                                 motorway_split_way: bool,
                                                 error_information: list,
                                                 previous_current: PreviousCurrentHighway,
                                                 previous_ref: str,
                                                 last_roundabout_nodes: list,
                                                 current_nodes: list,
                                                 previous_nodes: list):
        """Checks if the ways are either splitting or they are totally independent from each other.

        **Returns:** last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information"""
        # shouldn't we check it for the last way? technically that should be done too.
        # Case: unified route tries to be split..
        if last_node_current == first_node_of_first_forward_way_in_the_series or \
                first_node_current == first_node_of_first_forward_way_in_the_series or \
                last_node_current == last_node_of_first_forward_way_in_the_series or \
                first_node_current == last_node_of_first_forward_way_in_the_series:
            # just go on, since this is good (because it connects...)
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        # now we are getting gaps, but we have to first investigate if this is a case with a motorway / trunk road:
        elif role_of_first_way == "forward" or (
                is_mutcd_country and way_queries.check_if_directional(
            role_of_first_way)) and count_of_forward_roled_way_series == 1:
            last_forward_way_before_backward_direction = [previous_ref, previous_nodes]
            if current_highway == "motorway" or current_highway == "trunk" or (route_number.startswith("M")
                                                                               and network.startswith("HU")):
                # this means the motorway goes again from the start point to the endpoint via another way
                # We need M because of Hungary's motorways, in other countries this issue is escalated pretty well that
                # motorway ways or trunk ways are included only
                motorway_split_way = True
                has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                    is_mutcd_country, role_of_first_way,
                                                                                    role_of_first_way)  # we only need one way to check
                return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        else:
            # or the way is just connecting to a one-piece roundabout. I mean, that there was a roundabout like 2+ ways
            # ago, and then we find a way connecting to it. This may happen in very special cases.
            good_roundabout = way_queries.roundabout_checker(last_roundabout_nodes,
                                                             current_nodes)
            last_forward_way_before_backward_direction = [previous_ref, previous_nodes]
            if not good_roundabout:
                error_information.append(ErrorHighway(previous_current, "Gap in forward series"))
        return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information

    def check_if_motorway_not_split(self, motorway_split_way: bool, index_of_current_way: int,
                                    length_of_ways_to_search: int,
                                    current_highway: str,
                                    route_number: str, network: str, current_role: str,
                                    error_information: list, previous_current: PreviousCurrentHighway):
        if motorway_split_way is False and index_of_current_way == length_of_ways_to_search and (
                (current_highway == "motorway" or current_highway == "trunk") or (
                route_number.startswith("M") and network.startswith("HU"))) and current_role == "forward":
            error_information.append(ErrorHighway(previous_current, "Motorway not split"))
        return error_information

    def determine_role_errors_at_the_beginning_highway(self, index_of_current_way: int, current_role: str,
                                                       current_oneway: bool, current_highway: str,
                                                       current_roundabout: bool,
                                                       error_information: ErrorHighway,
                                                       previous_current: PreviousCurrentHighway):
        if index_of_current_way == 0:
            if (current_role == "" and ((current_oneway or (
                    current_roundabout and previous_current.first_node_current != previous_current.last_node_current)
                                         or (current_oneway and current_highway == "motorway"))
            )):
                error_information.append(ErrorHighway(previous_current, "Wrong role setup"))
        return error_information
