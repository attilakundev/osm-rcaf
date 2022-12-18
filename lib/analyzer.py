from osm_data_parser import OSMDataParser
from model.previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon
from model.error_hwy import ErrorHighway, ErrorMultipolygon
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
        pieces_of_roundabout = 1  # this will mark how many pieces does the roundabout consist of
        index_of_current_way = count_of_forward_ways_in_the_same_series = 0
        motorway_split_way = previous_oneway = previous_roundabout = has_directional_roles = is_mutcd_country = False
        last_forward_way_before_backward_direction = current_nodes = []
        first_role_previous = last_node_previous = previous_role = previous_ref = previous_highway \
            = first_node_of_first_forward_way = last_node_of_first_forward_way = ""
        # (separated highway) connecting to a point
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
                                                      first_node_previous=first_role_previous,
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
            first_node_current, last_node_current = self.is_role_backward(first_node_current, last_node_current,
                                                                          current_role)

            last_roundabout_nodes = self.is_way_roundabout(current_roundabout, current_role, elem_val["nd"])

            first_node_of_first_forward_way, last_node_of_first_forward_way, count_of_forward_ways_in_the_same_series = \
                self.is_the_way_in_forward_way_series(
                    index_of_current_way, previous_role, current_role, count_of_forward_ways_in_the_same_series,
                    role_of_first_way, first_node_current, last_node_current, first_node_of_first_forward_way,
                    last_node_of_first_forward_way)
            # Checking for the gaps.
            has_directional_roles, error_information = self.check_if_there_is_gap_at_the_beginning(index_of_current_way,
                                                                                                   count_of_forward_ways_in_the_same_series,
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
                                                                                 count_of_forward_ways_in_the_same_series,
                                                                                 last_node_previous,
                                                                                 last_node_current)

            has_directional_roles, error_information = self.check_if_way_connects_continuously(
                relation_info["ways_to_search"],
                index_of_current_way, first_role_previous,
                last_node_previous, first_node_current, last_node_current, previous_role, current_role, previous_oneway,
                previous_roundabout, current_oneway, is_mutcd_country, role_of_first_way, has_directional_roles,
                error_information, previous_current)

            index_of_current_way += 1
        pass

    def is_role_backward(self, first_node_current: str, last_node_current: str, current_role: str):
        """Is it a backward way? if yes, just replace the first and last node. (so we won't touch original array)

        **Returns** either first_node_current, last_node_current or last_node_current, first_node_current depending on role.
        """
        if current_role == "backward":
            return last_node_current, first_node_current
        return first_node_current, last_node_current

    def is_way_roundabout(self, current_roundabout: bool, current_role: str, nodes: list):
        """Is the current way a roundabout? if yes, collect all its nodes' reference number

        **Returns**: last_roundabout_nodes
        """
        last_roundabout_nodes = []
        if current_role == "" and current_roundabout is True:
            for node in nodes:
                last_roundabout_nodes.append(node["@ref"])
        return last_roundabout_nodes

    def is_the_way_in_forward_way_series(self, index_of_current_way: int, previous_role: str, current_role: str,
                                         count_of_forward_ways_in_the_same_series: int,
                                         role_of_first_way: str, first_node_current: str, last_node_current: str,
                                         first_node_of_first_forward_way: str, last_node_of_first_forward_way: str):
        """Is the current way going into a series of forward ways or
        does it start with a forward way?

        If yes, mark its first node
        and increase the number of the forward ways in the same series

        **Returns**: first_node_of_first_forward_way, last_node_of_first_forward_way, count_of_forward_ways_in_the_same_series
        """
        if index_of_current_way > 0 and previous_role == "" and current_role == "forward" or \
                (count_of_forward_ways_in_the_same_series == 0 and role_of_first_way == "forward"):
            count_of_forward_ways_in_the_same_series += 1
            return first_node_current, last_node_current, count_of_forward_ways_in_the_same_series
        elif previous_role == "forward" and current_role == "forward":
            count_of_forward_ways_in_the_same_series += 1
        return first_node_of_first_forward_way, last_node_of_first_forward_way, count_of_forward_ways_in_the_same_series

    def check_if_there_is_gap_at_the_beginning(self, index_of_current_way: int,
                                               count_of_forward_ways_in_the_same_series: int,
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

        if (index_of_current_way > 0 and count_of_forward_ways_in_the_same_series == 1 and (
                role_of_first_way == "forward"
                or (is_mutcd_country and way_queries.check_if_directional(role_of_first_way))) and (
                previous_role == "forward" or (is_mutcd_country and way_queries.check_if_directional(previous_role))
                and current_role == "" and len(last_forward_way_before_backward_direction) > 0)):
            return self.__check_last_forward_way_to_connection_with_current_way__(
                last_forward_way_before_backward_direction, first_node_previous, first_node_current, last_node_previous,
                last_node_current, is_mutcd_country, role_of_first_way, previous_role, has_directional_roles,
                error_information, previous_current)
        return has_directional_roles, error_information

    def __check_last_forward_way_to_connection_with_current_way__(self,
                                                                  last_forward_way_before_backward_direction: list,
                                                                  first_node_previous: str, first_node_current: str,
                                                                  last_node_previous: str, last_node_current: str,
                                                                  is_mutcd_country: bool, role_of_first_way: str,
                                                                  previous_role: str, has_directional_roles: bool,
                                                                  error_information: list,
                                                                  previous_current: PreviousCurrentHighway):

        """This is a helper function to determine that there's a gap at the beginning especially with ways that are
        supposed to be forward.
        
        **Returns**:has_directional_roles, error_information"""
        if (last_forward_way_before_backward_direction[-1] == last_node_current and (
                last_node_previous == last_node_current
                or first_node_previous == last_node_current)) or (last_forward_way_before_backward_direction[-1]
                                                                  == first_node_current) and (
                first_node_previous == first_node_current or last_node_previous == first_node_current):
            return self.check_if_mutcd_country_and_directional(has_directional_roles, is_mutcd_country,
                                                               role_of_first_way, previous_role, error_information)
        else:
            error_information.append(ErrorHighway(prev_curr=previous_current, error_type="Gap at the beginning"))
            return has_directional_roles, error_information

    def check_if_mutcd_country_and_directional(self, has_directional_roles, is_mutcd_country, role_of_first_way,
                                               previous_role, error_information):
        if is_mutcd_country and (
                way_queries.check_if_directional(role_of_first_way)
                or way_queries.check_if_directional(previous_role)):
            # we'll notify the user at the end that this relation can be reorganized by splitting it into
            # # two halves. eg: west-east, north-south (this is how they go in the US) - we don't know where
            # the relation starts
            has_directional_roles = True
            # we say that those directional routes are good but in fact not, so we mark this way that
            # we have to reconstruct the route
            return has_directional_roles, error_information
        return has_directional_roles, error_information

    # FOR THIS PARTICULAR METHOD, 3 UNIT TESTS HAVE TO BE CREATED.
    def check_roundabout_gaps(self, index_of_current_way: int, previous_roundabout: bool, current_roundabout: bool,
                              previous_current: PreviousCurrentHighway,
                              error_information: list, pieces_of_roundabout: int,
                              count_of_forward_ways_in_the_same_series: int, last_node_previous: str,
                              last_node_current: str):
        if index_of_current_way > 0 and not previous_roundabout and current_roundabout:
            pieces_of_roundabout = 1
            if count_of_forward_ways_in_the_same_series == 1:
                error_information.append(
                    ErrorHighway(previous_current, "Only one forward way before closed roundabout"))
            if last_node_previous == last_node_current:
                # this means that the roundabout would go in a weird way, this is not good!! it's a gap
                error_information.append(
                    ErrorHighway(previous_current, "Roundabout gap"))
            return pieces_of_roundabout, error_information
        elif index_of_current_way > 0 and previous_roundabout and current_roundabout:
            pieces_of_roundabout += 1
            return pieces_of_roundabout, error_information

    def check_if_way_connects_continuously(self, ways_to_search: list, index_of_current_way: int,
                                           first_node_previous: str, last_node_previous: str, first_node_current: str,
                                           last_node_current: str, previous_role: str, current_role: str,
                                           previous_oneway: bool, previous_roundabout: bool, current_oneway: bool,
                                           is_mutcd_country: bool, role_of_first_way: str, has_directional_roles: bool,
                                           error_information: list, previous_current: PreviousCurrentHighway):
        """This checks if the way connects continuously.
        
        **Returns**: has_directional_roles, error_information
        """
        if current_role == "" and not current_oneway:
            # This way is a normal way, but then we need to check its pattern
            # Since if it's oneway, it's not correct (there are chances though that it's alright, ex. it starts with a
            # oneway road due to road works but in this case NO)
            return self.condition_forward_oneway_in_forward_non_oneway_series(ways_to_search, index_of_current_way,
                                                                              first_node_previous, last_node_previous,
                                                                              first_node_current, last_node_current,
                                                                              previous_role, current_role,
                                                                              previous_oneway, previous_roundabout,
                                                                              current_oneway, is_mutcd_country,
                                                                              role_of_first_way, has_directional_roles,
                                                                              error_information, previous_current)
        elif current_role == "forward":
            pass

    def condition_forward_oneway_in_forward_non_oneway_series(self, ways_to_search: list, index_of_current_way: int,
                                                              first_node_previous: str, last_node_previous: str,
                                                              first_node_current: str, last_node_current: str,
                                                              previous_role: str, current_role: str,
                                                              previous_oneway: bool, previous_roundabout: bool,
                                                              current_oneway: bool, is_mutcd_country: bool,
                                                              role_of_first_way: str, has_directional_roles: bool,
                                                              error_information: list,
                                                              previous_current: PreviousCurrentHighway):
        """Case: FFFF but in the case of oneway it's NNON - that caase is bad because

        F = Forward O = Oneway N = Not oneway
        """
        if index_of_current_way > 2 and (
                previous_role == "forward" or (is_mutcd_country and way_queries.check_if_directional(previous_role))
                and not previous_oneway and ways_to_search[index_of_current_way - 2]["@role"] == ""
                and not way_queries.is_oneway(
                ways_to_search[index_of_current_way - 2]) and way_queries.get_role(
                ways_to_search[index_of_current_way - 3]) == "" and not way_queries.is_oneway(
                ways_to_search[index_of_current_way - 3])):
            return self.check_if_mutcd_country_and_directional(has_directional_roles,
                                                               is_mutcd_country, role_of_first_way, previous_role,
                                                               error_information)
        else:
            # This checks if before the current way there is a forward way without oneway, and before that there are
            # two ways without any role and oneway, if this is true then it's a bad way.
            error_information.append(ErrorHighway(prev_curr=previous_current, error_type="Forward but not oneway"))
            return has_directional_roles, error_information

    def multipolygon_checking(self, relation_info):
        return ""
