#!/usr/bin/python3
import dataclasses
import logging

from src.lib.model.previous_current import PreviousCurrentHighway
from src.lib.model.error_hwy import ErrorHighway
from src.lib.analyzer.analyzer_base import AnalyzerBase
from src.lib import way_queries



class HighwayAnalyzer(AnalyzerBase):
    # good for highway=* tags (primary, secondary, etc. and even trails and cycle routes)
    def checking(self, relation_info: dict, relation_id = ""):
        """Highway checking. This is where the gaps for a highway is checked. For unit tests, this
         should be only
        used if a complete relation is about to be tested."""
        prev_curr = PreviousCurrentHighway()
        error_information = []
        self.__determine_basic_relation_information__(prev_curr, relation_info,relation_id)
        for elem_val in relation_info["ways_to_search"]:
            if "nd" in elem_val and "tag" in elem_val:
                length_of_error_when_this_iter_begins = len(error_information)
                self.__determine_current_member__(elem_val, prev_curr)
                self.is_role_backward(prev_curr)
                self.is_way_roundabout(prev_curr, error_information)
                self.determine_role_errors_at_the_beginning_highway(prev_curr, error_information)
                prev_curr = self.is_the_way_in_forward_way_series(prev_curr)
                self.check_if_there_is_gap_at_the_beginning(prev_curr, error_information)
                prev_curr, error_information = self.check_roundabout_errors(
                    prev_curr, error_information)

                prev_curr, error_information = self.check_if_way_connects_continuously(
                    relation_info["ways_to_search"], prev_curr, error_information)
                self.__determine_previous_member__(prev_curr)

                self.check_if_motorway_not_split(prev_curr, len(relation_info["ways_to_search"]),
                                                 error_information)
                self.__determine_count_of_erroneous_ways__(error_information,
                                                           length_of_error_when_this_iter_begins,
                                                           prev_curr)
                prev_curr.index_of_current_way += 1
        correct_ways_count = len(relation_info["ways_to_search"]) - len(
            error_information) + prev_curr.amount_to_be_decreased_from_error_information_length
        amount_to_be_decreased_from_errors = \
            prev_curr.amount_to_be_decreased_from_error_information_length
        return error_information, correct_ways_count, amount_to_be_decreased_from_errors

    def __determine_count_of_erroneous_ways__(self, error_information,
                                              amount_to_be_decreased_from_error_information_length,
                                              prev_curr):
        if len(error_information) - amount_to_be_decreased_from_error_information_length > 1:
            prev_curr.amount_to_be_decreased_from_error_information_length += \
                (
                        len(error_information) -
                        amount_to_be_decreased_from_error_information_length) - 1

    def __determine_basic_relation_information__(self, prev_curr, relation_info,relation_id = ""):
        prev_curr.role_of_first_way = way_queries.get_role(relation_info["ways_to_search"][0])
        prev_curr.route_number = way_queries.get_ref_of_the_route(relation_info)
        prev_curr.network = way_queries.get_network(relation_info)
        prev_curr.is_mutcd_country = way_queries.determine_if_country_has_MUTCD_or_similar(
            relation_info)
        prev_curr.relation_id = relation_id

    def __determine_previous_member__(self, prev_curr):
        prev_curr.first_node_previous = prev_curr.first_node_current
        prev_curr.last_node_previous = prev_curr.last_node_current
        prev_curr.previous_roundabout = prev_curr.current_roundabout
        prev_curr.previous_nodes = prev_curr.current_nodes
        prev_curr.previous_oneway = prev_curr.current_oneway
        prev_curr.previous_role = prev_curr.current_role
        prev_curr.previous_highway = prev_curr.current_highway
        prev_curr.previous_ref = prev_curr.current_ref

    def __determine_current_member__(self, elem_val, prev_curr):
        prev_curr.first_node_current = way_queries.get_start_node(elem_val)
        prev_curr.last_node_current = way_queries.get_end_node(elem_val)
        prev_curr.current_roundabout = way_queries.is_roundabout(elem_val)
        prev_curr.current_highway = way_queries.get_highway(elem_val)
        prev_curr.current_oneway = way_queries.is_oneway(elem_val)
        prev_curr.current_ref = way_queries.get_way_ref(elem_val)
        prev_curr.current_role = way_queries.get_role(elem_val)
        prev_curr.current_nodes = way_queries.get_nodes(elem_val)

    def is_role_backward(self, previous_current: PreviousCurrentHighway):
        """Is it a backward way? if yes, just replace the first and last node, and make it "believe"
         that
         it's a forward way due to the replacement. (so we won't touch original array)

        **Returns** either first_node_current, last_node_current or last_node_current,
         first_node_current depending on role.
        """
        if previous_current.current_role == "backward":
            previous_current.current_role = "forward"
            previous_current.current_nodes = previous_current.current_nodes[::-1]
            previous_current.first_node_current, previous_current.last_node_current = \
                self.swap(previous_current.first_node_current, previous_current.last_node_current)

    def swap(self, item1, item2):
        tmp = item1
        item1 = item2
        item2 = tmp
        return item1, item2

    def is_way_roundabout(self, prev_curr: PreviousCurrentHighway, error_information: list):
        """Is the current way a roundabout? if yes, collect all its nodes' reference number

        **Returns**: last_roundabout_nodes
        """
        if prev_curr.current_roundabout:
            if prev_curr.current_ref in prev_curr.roundabout_ways:
                logging.info(f"Duplicated roundabout ways detected for {prev_curr.relation_id}")
                error_information.append(
                    ErrorHighway(dataclasses.replace(prev_curr), "Duplicated roundabout ways"))
            prev_curr.roundabout_ways.append(prev_curr.current_ref)
            if prev_curr.current_role == "":
                prev_curr.last_roundabout_nodes = prev_curr.current_nodes

    def is_the_way_in_forward_way_series(self, previous_current: PreviousCurrentHighway):
        """Is the current way going into a series of forward ways or
        does it start with a forward way?

        If yes, save its first and last node
        and increase the count of the forward ways

        **Returns**: first_node_of_first_forward_way_in_the_series,
         last_node_of_first_forward_way_in_the_series, count_of_forward_roled_way_series
        """
        if (previous_current.index_of_current_way > 0 and previous_current.previous_role == "" and
            previous_current.current_role == "forward") or (
                previous_current.index_of_current_way == 0 and
                previous_current.current_role == "forward"):
            previous_current.first_node_of_first_forward_way_in_the_series = previous_current. \
                first_node_current
            previous_current.last_node_of_first_forward_way_in_the_series = previous_current. \
                last_node_current
            previous_current.count_of_forward_role_way_series += 1
        elif previous_current.previous_role == "forward" and previous_current.current_role \
                == "forward":
            previous_current.count_of_forward_role_way_series += 1
        return previous_current

    def check_if_there_is_gap_at_the_beginning(self, previous_current: PreviousCurrentHighway,
                                               error_information: list):
        """
        Is the following way in the first forward way series, the first way is a forward way,
        the previous one is forward too, but the current one isn't a forward way?

        If yes, does the last forward way before going to backward direction have its last point not
         equal to the
        current way's last node,  even if the last or first nodes previous way(that is member
        the backward series') is equal to the current way's last of first.

        Well if this applies, then the way connection is broken, and it means it should be fixed.
        (The other case is not checked when the backward way connects to the rest of the nodes,
        since we know then there's a gap, it's checked a few if statements later)
        """

        if (previous_current.index_of_current_way > 0 and
                previous_current.count_of_forward_role_way_series == 1 and (
                        previous_current.role_of_first_way == "forward"
                        or (previous_current.is_mutcd_country and way_queries.check_if_directional(
                    previous_current.role_of_first_way))) and (
                        previous_current.previous_role == "forward" or (
                        previous_current.is_mutcd_country and way_queries.check_if_directional(
                    previous_current.previous_role))
                        and previous_current.current_role == "") and len(
                    previous_current.last_forward_way_ref_nodes_before_backward) > 0):
            self.__check_last_forward_way_to_connection_with_current_way__(previous_current,
                                                                           error_information)

    def check_if_mutcd_country_and_directional(self, prev_curr: PreviousCurrentHighway):

        """
        MUTCD = Manual on Uniform Traffic Control Devices - we'll notify the user at the end that
        this relation can be reorganized by splitting it into two halves. eg: west-east,
        north-south (this is how they go in the US) -
         we don't know where the relation starts. We say that those directional routes are good
         but in fact not, so we mark this way that we may have to reconstruct the route"""
        role_of_first_way_directional = way_queries.check_if_directional(
            prev_curr.role_of_first_way)
        prev_role_directional = way_queries.check_if_directional(prev_curr.previous_role)
        curr_role_directional = way_queries.check_if_directional(prev_curr.current_role)
        if prev_curr.is_mutcd_country and (
                role_of_first_way_directional or prev_role_directional or curr_role_directional):
            prev_curr.has_directional_roles = True
        return prev_curr

    def __check_last_forward_way_to_connection_with_current_way__(self,
                                                                  prev_curr: PreviousCurrentHighway,
                                                                  error_information: list):

        """This is a helper function to determine that there's a gap at the beginning especially
        with ways that are supposed to be forward would connect to a non-roled way but
        that way doesn't connect to them at all.

        **Returns**:has_directional_roles, error_information"""
        # Regardless if there is a connection or not, check if the ways have directional roles.
        prev_curr = self.check_if_mutcd_country_and_directional(prev_curr)
        # in the if part we want to check if it does connect
        if not ((prev_curr.last_forward_way_ref_nodes_before_backward[
                     -1] == prev_curr.last_node_current and (
                         prev_curr.last_node_previous == prev_curr.last_node_current
                         or prev_curr.first_node_previous == prev_curr.last_node_current)) or (
                        prev_curr.last_forward_way_ref_nodes_before_backward[-1]
                        == prev_curr.first_node_current) and (
                        prev_curr.first_node_previous == prev_curr.first_node_current or
                        prev_curr.last_node_previous == prev_curr.first_node_current)):
            logging.info(f"Gap at the beginning detected for {prev_curr.relation_id}")
            error_information.append(
                ErrorHighway(prev_curr=dataclasses.replace(prev_curr),
                             error_type="Gap at the beginning"))

    def check_roundabout_errors(self, previous_current: PreviousCurrentHighway,
                                error_information: list):
        """
        This checks if the open roundabout has missing roles, or too few forward ways before closed
        roundabout.
        Other than that if everything went well, add the number of roundabout pieces (or reset it)
        :return:
        """
        if previous_current.current_roundabout and previous_current.current_role == "" \
                and previous_current.first_node_current != previous_current.last_node_current:
            logging.info(f"Forward role missing at roundabout detect"
                         f"ed for {previous_current.relation_id}")
            error_information.append(
                ErrorHighway(dataclasses.replace(previous_current),
                             "Forward role missing at roundabout"))
        if previous_current.index_of_current_way > 0 and not \
                previous_current.previous_roundabout and previous_current.current_roundabout:
            if previous_current.count_of_forward_role_way_series == 1:
                logging.info(f"Only one forward way before closed roundabout detected for "
                             f" {previous_current.relation_id}")
                error_information.append(
                    ErrorHighway(dataclasses.replace(previous_current),
                                 "Only one forward way before closed roundabout"))
            if previous_current.last_node_previous == previous_current.last_node_current \
                    and previous_current.first_node_current != previous_current.last_node_current:
                # this means that the roundabout would go in a weird way (causing an endless loop in
                # the analyzer), this is not good!! It's a gap
                logging.info(f"Roundabout gap detected for{previous_current.relation_id}")
                error_information.append(
                    ErrorHighway(dataclasses.replace(previous_current), "Roundabout gap"))
        return previous_current, error_information

    def __is_roundabout_entry_way_in_wrong_order__(self, prev_curr: PreviousCurrentHighway,
                                                   error_information: list,
                                                   ways_to_search: list):
        if 0 < prev_curr.index_of_current_way < len(
                ways_to_search) - 2 and prev_curr.last_node_previous == \
                prev_curr.last_node_current and way_queries. \
                is_roundabout(ways_to_search[prev_curr.index_of_current_way + 2]):
            logging.info(f"Wrong order of roundabout entries detected for{prev_curr.relation_id}")
            error_information.append(
                ErrorHighway(dataclasses.replace(prev_curr), "Wrong order of roundabout entries"))
            return True
        else:
            return False

    def check_if_way_connects_continuously(self, ways_to_search: list,
                                           prev_curr: PreviousCurrentHighway,
                                           error_information: list):
        """This checks if the way connects continuously, if yes then check if there are issues with
        the roles. If it's not continuous, then check if it's a roundabout.
        if it's not a roundabout but a weirdly connected way
        The returned data may have the same value as before, it depends on the evaluation of the
        currently checked
        way.

        :returns: last_forward_way_ref_nodes_before_backward, motorway_split_way,
        has_directional_roles,
        error_information"""
        # Check if the roundabout's entryway is in wrong order.
        if self.__is_roundabout_entry_way_in_wrong_order__(prev_curr, error_information,
                                                           ways_to_search):
            return prev_curr, error_information
        if prev_curr.index_of_current_way > 0 and (
                (prev_curr.first_node_previous == prev_curr.first_node_current
                 or prev_curr.first_node_previous == prev_curr.last_node_current
                 or prev_curr.last_node_previous == prev_curr.first_node_current
                 or prev_curr.last_node_previous == prev_curr.last_node_current)
                or (prev_curr.previous_roundabout and not prev_curr.current_roundabout and
                    way_queries.roundabout_checker(prev_curr.current_nodes,
                                                   prev_curr.previous_nodes))):
            prev_curr, error_information = self. \
                check_role_issues_in_continuous_way(prev_curr,
                                                    error_information)
        # If the way is not continuous, because the end and starting nodes are different of the
        # two ways, let's try it at roundabouts, and find the node in it (this only works if the
        # roundabout is coming right after (or right before) in order of relation):
        elif prev_curr.index_of_current_way > 0 and (
                prev_curr.previous_roundabout and not prev_curr.current_roundabout or
                (not prev_curr.previous_roundabout and prev_curr.current_roundabout)):
            good_roundabout = way_queries.roundabout_checker(prev_curr.current_nodes,
                                                             prev_curr.previous_nodes)
            if not good_roundabout and not (prev_curr.previous_role == "forward"
                                            and prev_curr.previous_oneway
                                            and not prev_curr.previous_roundabout):
                logging.info(f"Roundabout gap detected for {prev_curr.relation_id}")
                error_information.append(
                    ErrorHighway(dataclasses.replace(prev_curr), "Roundabout gap"))
                # the not (previous_role == "forward" and previous_oneway and
                # not previous_roundabout) is needed, since otherwise relations 23099 (route nr 3)
                # and relation 38124 (route nr 5) would detect an unnecessary gap,
                # because they start from a common point and split apart but then merge back.
        # Special case, when there are a bunch of oneway roads connecting in weird order in the
        # relation (2x2 lane road
        # to 2x2 separate highway, opposite of the starting 2x2 separate to 2x2 merged)
        elif prev_curr.index_of_current_way > 0 \
                and (prev_curr.previous_role == "forward"
                     or (prev_curr.is_mutcd_country and
                         way_queries.check_if_directional(prev_curr.current_role))):
            prev_curr = self.check_if_mutcd_country_and_directional(prev_curr)
            prev_curr, error_information = self. \
                check_the_situation_with_2_by_2_highways(prev_curr,
                                                         error_information)
        elif prev_curr.index_of_current_way > 0:
            # It's definitely a gap
            logging.info(f"Gap detected for {prev_curr.relation_id}")
            error_information.append(ErrorHighway(dataclasses.replace(prev_curr), "Gap"))
        return prev_curr, error_information

    def check_role_issues_in_continuous_way(self, previous_current: PreviousCurrentHighway,
                                            error_information: list):
        """This checks if the way has issues with the roles or determine if the way is in a country
         which uses
        NORTH / SOUTH / WEST / EAST on the signs (cardinal direction).

        **Returns**: has_directional_roles, error_information
        """
        if previous_current.current_role == "" and not previous_current.current_oneway:
            # This way is a normal way, but then we need to check its pattern
            # Since if it's oneway, it's not correct (there are chances though that it's alright,
            # ex. it starts with a oneway road due to road works but in this case NO)
            return self.__condition_forward_no_oneway_in_non_forward_series__(previous_current,
                                                                              error_information)
        elif ((previous_current.current_role == "forward" or (
                previous_current.is_mutcd_country and
                way_queries.check_if_directional(previous_current.current_role)))) \
                and previous_current.current_oneway:
            # We know all oneways are forward
            previous_current = self.check_if_mutcd_country_and_directional(previous_current)
        elif (previous_current.current_role == "forward" or (
                previous_current.is_mutcd_country and
                way_queries.check_if_directional(previous_current.current_role))) \
                and not previous_current.current_oneway:
            # If we didn't run into the issue above, then it means the way is probably at a
            # roundabout or something, so it's not a big problem
            previous_current = self.check_if_mutcd_country_and_directional(previous_current)
        else:
            # it runs whenever there's no role for oneway OR it's oneway but its role is not forward
            # / cardinal role.
            logging.info(f"Wrong role setup detected for {previous_current.relation_id}")
            error_information.append(
                ErrorHighway(dataclasses.replace(previous_current), "Wrong role setup"))
        return previous_current, error_information

    def __condition_forward_no_oneway_in_non_forward_series__(self,
                                                              prev_curr: PreviousCurrentHighway,
                                                              error_information: list):
        """Case: NNFN - this is a bad case because in the case of 2x1 lane motorways there's no
         ability to go backwards
        (or can be FFFN etc. - since you can't traverse backwards then in the case of 2x1 - or
         if the forward series consists of only 1 members
         - worst case! then it's an error for sure, no ability to return, this is for all types of
         roads)

        The roundabout checker shouldn't deceive you, I don't want to rename that method since it's
         used for roundabout connection from multiple nodes.
        F= Forward N = Not oneway
        """
        if prev_curr.index_of_current_way > 1 \
                and ((prev_curr.previous_role == "forward" or
                      (prev_curr.is_mutcd_country and
                       way_queries.check_if_directional(prev_curr.previous_role))) and (
                             prev_curr.previous_highway == "motorway"
                             or prev_curr.count_of_forward_role_way_series == 1)
                     and not prev_curr.previous_oneway
                     and (len(prev_curr.last_forward_way_ref_nodes_before_backward) == 0 or
                          (len(prev_curr.last_forward_way_ref_nodes_before_backward) > 1
                           and not way_queries.roundabout_checker(
                                      prev_curr.last_forward_way_ref_nodes_before_backward[
                                          -1],
                                      prev_curr.previous_nodes)))):
            prev_curr = self.check_if_mutcd_country_and_directional(prev_curr)
            # This checks if before the current way there is a forward way without oneway, and
            # before that there are two ways without any role and oneway,
            # if this is true then it's a bad way.
            logging.info(f"Forward and non-oneway without ability to move backward detected for"
                         f" {prev_curr.relation_id}")
            error_information.append(
                ErrorHighway(prev_curr=dataclasses.replace(prev_curr),
                             error_type="Forward and non-oneway without ability"
                                        " to move backward"))
        elif prev_curr.index_of_current_way < 2:
            # there is no problem with the way since the pattern only happens if it's the case
            # mentioned in this method's docstring.
            return prev_curr, error_information
        return prev_curr, error_information

    def check_the_situation_with_2_by_2_highways(self, prev_curr: PreviousCurrentHighway,
                                                 error_information: list):
        """Checks if the ways are either splitting or they are totally independent from each other,
         so they don't connect.

        **Returns:** last_forward_way_ref_nodes_before_backward, motorway_split_way,
         has_directional_roles, error_information"""

        # Case: Split road connects to one of the node of the other side
        if way_queries.check_connectivity(prev_curr.first_node_current, prev_curr.last_node_current,
                                          prev_curr.first_node_of_first_forward_way_in_the_series,
                                          prev_curr.last_node_of_first_forward_way_in_the_series):
            # just go on, since this is good (because it connects...)
            return prev_curr, error_information
        # now we are getting gaps, but we have to first investigate if this is a case with a
        # motorway / trunk road:
        elif prev_curr.role_of_first_way == "forward" or (
                prev_curr.is_mutcd_country and way_queries.
                check_if_directional(prev_curr.role_of_first_way)) \
                and prev_curr.count_of_forward_role_way_series == 1:
            prev_curr.last_forward_way_ref_nodes_before_backward = [prev_curr.previous_ref,
                                                                    prev_curr.previous_nodes]
            if prev_curr.current_highway == "motorway" or \
                    prev_curr.current_highway == "trunk" or (prev_curr.route_number.startswith("M")
                                                             and prev_curr.network.startswith(
                        "HU")):
                # this means the motorway goes again from the start point to the endpoint
                # via another way
                # We need M because of Hungary's motorways, in other countries this issue
                # is escalated pretty well that
                # motorway ways or trunk ways are included only
                prev_curr.motorway_split_way = True
                prev_curr = self.check_if_mutcd_country_and_directional(
                    prev_curr)  # we only need one way to check
        else:
            # or the way is just connecting to a one-piece roundabout. I mean, that there was a
            # roundabout like 2+ ways
            # ago, and then we find a way connecting to it. This may happen in very special cases.
            good_roundabout = way_queries.roundabout_checker(prev_curr.last_roundabout_nodes,
                                                             prev_curr.current_nodes)
            prev_curr.last_forward_way_ref_nodes_before_backward = [prev_curr.previous_ref,
                                                                    prev_curr.previous_nodes]
            if not good_roundabout:
                logging.info(f"Gap in forward series detected for {prev_curr.relation_id}")
                error_information.append(
                    ErrorHighway(dataclasses.replace(prev_curr), "Gap in forward series"))
        return prev_curr, error_information

    def check_if_motorway_not_split(self, prev_curr: PreviousCurrentHighway,
                                    length_of_ways_to_search: int,
                                    error_information: list):
        """
        If the entire relation is a motorway and it didn't split all along (so there aren't two
         parallel parts), then we should mark it as wrong
        Important, it should have the forward role, otherwise this counts as an expressway with 2x1
         lanes. Then it's not wrong
        :return: error_information, which contains all the errors happened with the relation
        """
        if prev_curr.motorway_split_way is False and prev_curr.index_of_current_way == \
                length_of_ways_to_search - 1 and (
                (
                        prev_curr.current_highway == "motorway" or
                        prev_curr.current_highway == "trunk") or (
                        prev_curr.route_number.startswith("M") and
                        prev_curr.network.startswith("HU"))) and \
                prev_curr.current_role == "forward":
            logging.info(f"Motorway not split detected for {prev_curr.relation_id}")
            error_information.append(
                ErrorHighway(dataclasses.replace(prev_curr), "Motorway not split"))

    def determine_role_errors_at_the_beginning_highway(self, prev_curr: PreviousCurrentHighway,
                                                       error_information: list):
        """
        If the first road piece doesn't have a role, and is oneway / it's an open roundabout piece,
         then we should mark it as wrong
        :return: error_information, which contains all the errors happened with the relation
        """
        if prev_curr.index_of_current_way == 0:
            if (prev_curr.current_role == "" and ((prev_curr.current_oneway or (
                    prev_curr.current_roundabout and
                    prev_curr.first_node_current != prev_curr.last_node_current))
            )):
                logging.info(f"Wrong role setup detected for {prev_curr.relation_id}")
                error_information.append(ErrorHighway(dataclasses.replace(prev_curr), "Wrong role setup"))
        return prev_curr, error_information
