#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")

from osm_data_parser import OSMDataParser
from previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon
from error_hwy import ErrorHighway, ErrorMultipolygon
import way_queries


class Analyzer:
    def relation_checking(self, loaded_relation):
        data_parser = OSMDataParser()
        error_information = []
        relation_info = data_parser.collect_information_about_the_relation(loaded_relation)  # generalized function
        # so it'll take whatever relation it is
        if way_queries.get_relation_type(relation_info) != "public_transport":
            role_of_first_way = way_queries.get_role(relation_info["ways_to_search"][0])
            if "route" in relation_info and (
                    relation_info["route"] == "railway" or relation_info.get["route"] == "train"):
                return self.railway_checking(relation_info, error_information)
            elif "route" in relation_info:
                return self.highway_checking(relation_info, error_information, role_of_first_way)
            else:
                return self.multipolygon_checking(relation_info)
        return "OutOfScope"

    def railway_checking(self, relation_info, error_information):
        first_node_previous = ""
        last_node_previous = ""
        previous_ref = ""
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

    # good for highway=* tags (primary, secondary, etc. and even trails and cycle routes)
    def highway_checking(self, relation_info, error_information, role_of_first_way):
        """Highway checking. This is where the gaps for a highway is checked. For unit tests, this should be only
        used if a complete relation is about to be tested."""
        currently_checked_ref = way_queries.get_ref_of_the_route(relation_info)
        network = way_queries.get_network(relation_info)
        pieces_of_roundabout = 1  # this will mark how many pieces does the roundabout consist of
        index_of_current_way = count_of_forward_roled_way_series = 0
        motorway_split_way = previous_oneway = previous_roundabout = has_directional_roles = False
        is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(relation_info)
        last_forward_way_before_backward_direction = current_nodes = previous_nodes = []
        # last_forward_way_before_backward_direction:  when we have relation beginning with forward ways
        # (separated highway) connencting to a point
        first_node_previous = last_node_previous = previous_role = previous_ref = previous_highway \
            = first_node_of_first_forward_way_in_the_series = last_node_of_first_forward_way_in_the_series = ""
        for elem_val in relation_info["ways_to_search"]:
            # current = current way, previous = previous way
            first_node_current = way_queries.get_start_node(elem_val)
            last_node_current = way_queries.get_end_node(elem_val)
            current_roundabout = way_queries.is_roundabout(elem_val)
            current_highway = way_queries.get_highway(elem_val)
            current_oneway = way_queries.is_oneway(elem_val)
            current_ref = way_queries.get_way_ref(elem_val)
            current_role = way_queries.get_role(elem_val)
            current_nodes = way_queries.get_nodes(elem_val)
            previous_current = PreviousCurrentHighway(currently_checked_ref=currently_checked_ref,
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

            last_roundabout_nodes = self.is_way_roundabout(current_roundabout, current_role, current_nodes)

            first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series, count_of_forward_roled_way_series = \
                self.is_the_way_in_forward_way_series(
                    index_of_current_way, previous_role, current_role, count_of_forward_roled_way_series,
                    first_node_current, last_node_current,
                    first_node_of_first_forward_way_in_the_series,
                    last_node_of_first_forward_way_in_the_series)
            # Checking for the gaps.
            error_information = self.check_if_there_is_gap_at_the_beginning(index_of_current_way,
                                                                                                   count_of_forward_roled_way_series,
                                                                                                   role_of_first_way,
                                                                                                   is_mutcd_country,
                                                                                                   previous_role,
                                                                                                   current_role,
                                                                                                   first_role_previous,
                                                                                                   first_node_current,
                                                                                                   last_node_previous,
                                                                                                   last_node_current,
                                                                                                   last_forward_way_before_backward_direction,
                                                                                                   has_directional_roles,
                                                                                                   error_information,
                                                                                                   previous_current)

            pieces_of_roundabout, error_information = self.check_roundabout_gaps(index_of_current_way,
                                                                                 previous_roundabout,
                                                                                 current_roundabout, previous_current,
                                                                                 error_information,
                                                                                 pieces_of_roundabout,
                                                                                 count_of_forward_roled_way_series,
                                                                                 last_node_previous,
                                                                                 last_node_current)

            last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information = self.check_if_way_connects_continuously(
                relation_info["ways_to_search"], previous_nodes, current_nodes, index_of_current_way,
                first_role_previous, last_node_previous, first_node_current, last_node_current, previous_role,
                current_role,
                previous_oneway, previous_roundabout, current_roundabout, current_oneway, is_mutcd_country,
                role_of_first_way, has_directional_roles, error_information, previous_current,
                first_node_of_first_forward_way_in_the_series, last_node_of_first_forward_way_in_the_series,
                motorway_split_way, count_of_forward_roled_way_series, current_highway, current_highway,
                currently_checked_ref, network, previous_ref, last_roundabout_nodes)
            first_role_previous = first_node_current
            last_node_previous = last_node_current
            previous_roundabout = current_roundabout
            previous_nodes = current_nodes
            previous_oneway = previous_oneway
            previous_role = current_role
            previous_highway = current_highway
            previous_ref = current_ref
            index_of_current_way += 1
            error_information = self.check_if_motorway_not_split(motorway_split_way, index_of_current_way,
                                                                 len(relation_info["ways_to_search"]),
                                                                 current_highway, currently_checked_ref, network,
                                                                 current_role, error_information, previous_current)
        correct_ways_count = len(relation_info["ways_to_search"]) - len(error_information)
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
                          last_roundabout_nodes: list):
        """Is the current way a roundabout? if yes, collect all its nodes' reference number

        **Returns**: last_roundabout_nodes
        """
        if current_role == "" and current_roundabout is True:
            return current_nodes
        return last_roundabout_nodes  # we don't change its value.

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

    # FOR THIS PARTICULAR METHOD, 3 UNIT TESTS HAVE TO BE CREATED.
    def check_roundabout_gaps(self, index_of_current_way: int, previous_roundabout: bool, current_roundabout: bool,
                              previous_current: PreviousCurrentHighway,
                              error_information: list, pieces_of_roundabout: int,
                              count_of_forward_roled_way_series: int, last_node_previous: str,
                              last_node_current: str):
        if index_of_current_way > 0 and not previous_roundabout and current_roundabout:
            pieces_of_roundabout = 1
            if count_of_forward_roled_way_series == 1:
                error_information.append(
                    ErrorHighway(previous_current, "Only one forward way before closed roundabout"))
            if last_node_previous == last_node_current:
                # this means that the roundabout would go in a weird way, this is not good!! it's a gap
                error_information.append(ErrorHighway(previous_current, "Roundabout gap"))
            return pieces_of_roundabout, error_information
        elif index_of_current_way > 0 and previous_roundabout and current_roundabout:
            pieces_of_roundabout += 1
            return pieces_of_roundabout, error_information

    # This is a massive method. You should test it only whenever the methods in it had been thoroughly tested.
    def check_if_way_connects_continuously(self, ways_to_search: list, previous_nodes: list, current_nodes: list,
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
                                           currently_checked_ref: str, network: str, previous_ref: str,
                                           last_roundabout_nodes: list):
        """This checks if the way connects continuously, if yes then check if there are issues with the roling. If
        it's not continuous, then check if it's a roundabout. if it's not a roundabout but a weirdly connected

        **Returns**: last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles,
        error_information

        The returned data may have the same value as before, it depends on the evaluation of the currently checked
        way."""
        if index_of_current_way > 0 and (
                first_node_previous == first_node_current or first_node_previous == last_node_current
                or last_node_previous == first_node_current or last_node_previous == last_node_current):
            has_directional_roles, error_information = self.check_role_issues_in_continuous_way(ways_to_search,
                                                                                                index_of_current_way,
                                                                                                previous_role,
                                                                                                current_role,
                                                                                                previous_oneway,
                                                                                                current_oneway,
                                                                                                is_mutcd_country,
                                                                                                role_of_first_way,
                                                                                                has_directional_roles,
                                                                                                error_information,
                                                                                                previous_current)
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        # If the way is not continuous, because the end and starting nodes are different of the two ways, let's try it
        # at roundabouts, and find the node in it (this only works if the roundabout is coming right after
        # (or right before) in order of relation):
        elif index_of_current_way > 0 and (
                previous_roundabout and not current_roundabout or (not previous_roundabout and current_roundabout)):
            good_roundabout = way_queries.roundabout_checker(current_nodes,
                                                             previous_nodes)
            if not good_roundabout:
                error_information.append(ErrorHighway(previous_current, "Roundabout gap"))
                return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        # Special case, when there are a bunch of oneway roads connecting in weird order in the relation (2x2 lane road
        # to 2x2 separate highway, opposite of the starting 2x2 separate to 2x2 merged)
        elif index_of_current_way > 0 and (previous_role == "forward"
                                           or (is_mutcd_country and way_queries.check_if_directional(current_role))):
            has_directional_roles_local = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                      is_mutcd_country, previous_role,
                                                                                      current_role)
            last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information = self.check_the_situation_with_2_by_2_highways(
                is_mutcd_country, has_directional_roles_local,
                last_node_previous, first_node_current, last_node_current,
                first_node_of_first_forward_way_in_the_series,
                last_node_of_first_forward_way_in_the_series, role_of_first_way,
                count_of_forward_roled_way_series, last_forward_way_before_backward_direction, current_highway,
                currently_checked_ref, network, motorway_split_way, error_information, previous_current, previous_ref,
                last_roundabout_nodes, current_nodes)
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        elif index_of_current_way > 0:
            # It's definitely a gap
            error_information.append(ErrorHighway(previous_current, "Gap"))
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information
        else:
            # default case, when we are at the first way.. we don't change anything
            return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information

    def check_role_issues_in_continuous_way(self, ways_to_search: list, index_of_current_way: int, previous_role: str,
                                            current_role: str, previous_oneway: bool, current_oneway: bool,
                                            is_mutcd_country: bool, role_of_first_way: str, has_directional_roles: bool,
                                            error_information: list, previous_current: PreviousCurrentHighway):
        """This checks if the way has issues with the roles or determine if the way is in a country which uses
        NORTH / SOUTH / WEST / EAST on the signs (cardinal direction).

        **Returns**: has_directional_roles, error_information
        """
        if current_role == "" and not current_oneway:
            # This way is a normal way, but then we need to check its pattern
            # Since if it's oneway, it's not correct (there are chances though that it's alright, ex. it starts with a
            # oneway road due to road works but in this case NO)
            return self.condition_forward_oneway_in_forward_non_oneway_series(ways_to_search, index_of_current_way,
                                                                              previous_role,
                                                                              previous_oneway, is_mutcd_country,
                                                                              role_of_first_way, has_directional_roles,
                                                                              error_information, previous_current)
        elif current_role == "forward" and (
                is_mutcd_country and way_queries.check_if_directional(current_role) and current_oneway):
            # We know all oneways are forward
            has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                is_mutcd_country, current_role,
                                                                                current_role)
            return has_directional_roles, error_information
        elif current_role == "forward" and (
                is_mutcd_country and way_queries.check_if_directional(current_role) and not current_oneway):
            # If we didn't run into the issue above, then it means the way is probably at a roundabout or
            # something, so it's not a big problem
            has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                is_mutcd_country, current_role,
                                                                                current_role)
            return has_directional_roles, error_information
        else:
            error_information.append(ErrorHighway(previous_current, "Wrong role setup"))
            return has_directional_roles, error_information

    def condition_forward_oneway_in_forward_non_oneway_series(self, ways_to_search: list, index_of_current_way: int,
                                                              previous_role: str,
                                                              previous_oneway: bool, is_mutcd_country: bool,
                                                              role_of_first_way: str, has_directional_roles: bool,
                                                              error_information: list,
                                                              previous_current: PreviousCurrentHighway):
        """Case: NNON - this is a bad case because then there's a consistency issue (cars can't go both ways)

        O = Oneway N = Not oneway
        """
        if index_of_current_way > 2 and (
                previous_role == "forward" or (is_mutcd_country and way_queries.check_if_directional(previous_role))
                and not previous_oneway
                and way_queries.get_role(ways_to_search[index_of_current_way - 2]) == ""
                and not way_queries.is_oneway(ways_to_search[index_of_current_way - 2])
                and way_queries.get_role(ways_to_search[index_of_current_way - 3]) == ""
                and not way_queries.is_oneway(ways_to_search[index_of_current_way - 3])):
            has_directional_roles = self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                                                is_mutcd_country, role_of_first_way,
                                                                                previous_role)
            return has_directional_roles, error_information
        else:
            # This checks if before the current way there is a forward way without oneway, and before that there are
            # two ways without any role and oneway, if this is true then it's a bad way.
            error_information.append(ErrorHighway(prev_curr=previous_current, error_type="Forward but not oneway"))
            return has_directional_roles, error_information

    def check_the_situation_with_2_by_2_highways(self, is_mutcd_country: bool,
                                                 has_directional_roles: bool, last_node_previous: str,
                                                 first_node_current: str,
                                                 last_node_current: str,
                                                 first_node_of_first_forward_way_in_the_series: str,
                                                 last_node_of_first_forward_way_in_the_series: str,
                                                 role_of_first_way: str,
                                                 count_of_forward_roled_way_series: int,
                                                 last_forward_way_before_backward_direction: list,
                                                 current_highway: str,
                                                 currently_checked_ref: str,
                                                 network: str,
                                                 motorway_split_way: bool,
                                                 error_information: list,
                                                 previous_current: PreviousCurrentHighway,
                                                 previous_ref: str,
                                                 last_roundabout_nodes: list,
                                                 current_nodes: list):
        # shouldn't we check it for the last node? technically that should be done too.
        if last_node_current == first_node_of_first_forward_way_in_the_series or \
                first_node_current == first_node_of_first_forward_way_in_the_series or \
                last_node_current == last_node_of_first_forward_way_in_the_series or \
                first_node_current == last_node_of_first_forward_way_in_the_series:
            # just go on, since this is good (because it connects...)
            pass
        # now we are getting gaps, but we have to first investigate if this is a case with a motorway / trunk road:
        elif role_of_first_way == "forward" or (
                is_mutcd_country and way_queries.check_if_directional(
            role_of_first_way)) and count_of_forward_roled_way_series == 1:
            last_forward_way_before_backward_direction = [previous_ref, last_node_previous]
            if current_highway == "motorway" or current_highway == "trunk" or (currently_checked_ref.startswith("M")
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
            # or the way is just connecting to a roundabout. I mean, that there was a roundabout like 2+ ways ago and
            # then we find a way connecting to it. This may happen in very special cases.
            good_roundabout = way_queries.roundabout_checker(last_roundabout_nodes,
                                                             current_nodes)
            if not good_roundabout:
                error_information.append(ErrorHighway(previous_current, "Gap in forward series"))
        return last_forward_way_before_backward_direction, motorway_split_way, has_directional_roles, error_information

    def check_if_motorway_not_split(self, motorway_split_way: bool, index_of_current_way: int,
                                    length_of_ways_to_search: int,
                                    current_highway: str,
                                    currently_checked_ref: str, network: str, current_role: str,
                                    error_information: list, previous_current: PreviousCurrentHighway):
        if motorway_split_way == False and index_of_current_way == length_of_ways_to_search - 1 and (
                (current_highway == "motorway" or current_highway == "trunk") or (
                currently_checked_ref.startswith("M") and network.startswith("HU"))) and current_role == "forward":
            error_information.append([previous_current, "Motorway not split"])
        return error_information

        def multipolygon_checking(self, relation_info):
            return ""
