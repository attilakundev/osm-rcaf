from osm_data_parser import OSMDataParser
import model.previous_current as previous_current
import way_queries


class Analyzer:
    pieces_of_roundabout = 1  # this will mark how many pieces does the roundabout consist of
    no_current_way = 0  # number of the currently checked way
    number_of_forward_way_series = 0
    # I would need the first "forward" way's first node number in a row, because sometimes some forward ways connect
    # back to the first way's nodes
    first_node_of_first_forward_way = -1
    last_node_of_first_forward_way = -1
    role_of_first_way = ""
    motorway_split_way = False  # this variable comes in handy when we deal with motorways and they go in one direction
    # from start to endpoint
    last_roundabout_nodes = []
    last_forward_way_before_backward_direction = []  # we need it when we have relation beginning with forward ways

    # (separated highway) connecting to a point
    def relation_checking(self, loaded_relation):
        data_parser = OSMDataParser()
        relation_info = data_parser.collect_information_about_the_relation(loaded_relation)  # generalized function
        # so it'll take whatever relation it is
        if way_queries.get_relation_type(relation_info) != "public_transport":
            self.role_of_first_way = way_queries.get_role(relation_info["ways_to_search"][0])
            if "route" in relation_info and (
                    relation_info["route"] == "railway" or relation_info.get["route"] == "train"):
                return self.railway_checking(relation_info)
            elif "route" in relation_info:
                return self.highway_checking(relation_info)
            else:
                return self.multipolygon_checking(relation_info)
        return "OutOfScope"

    def railway_checking(self, relation_info):
        error_information = []
        first_node_previous = ""
        last_node_previous = ""
        previous_ref = ""
        for elem_val in relation_info["ways_to_search"]:
            first_node_current = way_queries.get_start_node(elem_val)
            last_node_current = way_queries.get_end_node(elem_val)
            current_ref = way_queries.get_way_ref(elem_val)
            # just check, if the way is connected to the other
            if first_node_previous != "" and last_node_previous != "" and previous_ref != "":
                prev_curr = previous_current.PreviousCurrentHighway(first_node_previous=first_node_previous,
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
        return error_information, correct_ways_count  # the number of errors could be calculated from len(error_information)

    def check_rails_if_the_ways_are_not_connected(self, first_node_previous, last_node_previous,
                                                  first_node_current, last_node_current):
        if first_node_previous != "" and last_node_previous != "" and not way_queries.check_connectivity(
                first_node_previous, last_node_previous, first_node_current, last_node_current):
            return True
        return False

    def highway_checking(self, relation_info):
        return ""

    def multipolygon_checking(self, relation_info):
        return ""
