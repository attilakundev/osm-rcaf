def get_nodes(array):
    return [node["@ref"] for node in array["nd"]]


def get_start_node(array):
    return array["nd"][0]["@ref"]


def get_end_node(array):
    return array["nd"][len(array["nd"]) - 1]["@ref"]


def is_roundabout(array):
    if "tag" in array:
        for tag in array["tag"]:
            if tag["@k"] == "junction" and tag["@v"] == "roundabout":
                return True
    return False


def is_oneway(array):
    if "tag" in array:
        for tag in array["tag"]:
            if tag["@k"] == "oneway" and tag["@v"] == "yes":
                return True
    return False


def remove_tag(array, tag_key, value_of_key):
    if type(array["tag"]) == list:
        for key_value_pair in array["tag"]:
            if key_value_pair["@k"] == tag_key and key_value_pair["@v"] == value_of_key:
                array["tag"].remove(key_value_pair)
    else:
        array["tag"] = []  # since there was only just one dictionary here, we empty this
    return array


def modify_role(array, role):
    array["@role"] = role
    return array


def get_role(array):
    if "@role" in array:
        return array["@role"]
    return ""


# in case we are dealing with route=road (or cycling etc.)
def get_highway(array):
    if "tag" in array:
        for key_value_pair in array["tag"]:
            if key_value_pair["@k"] == "highway":
                return key_value_pair["@v"]
    return ""


# in case we are dealing with route=railway
def get_railway(array):
    if "tag" in array:
        for key_value_pair in array["tag"]:
            if key_value_pair["@k"] == "railway":
                return key_value_pair["@v"]
    return ""


def get_highway_ref(array):
    if "tag" in array:
        for key_value_pair in array["tag"]:
            if key_value_pair["@k"] == "ref":
                return key_value_pair["@v"]
    return ""  # if empty, it means that the ref is not set, which is a problem. We need to put that from the way of the relation


def put_ref_from_relation_to_highway_way(array):  # this requires enumerate when for looping
    ref = get_ref_of_the_route(array)
    for index, element in enumerate(array["ways"]):
        if element["@type"] == "way":
            for key_value_pair in element["tag"]:
                if key_value_pair["@k"] == "highway":
                    array["ways"][index]["tag"].append({
                        "@k": "ref",
                        "@v": ref
                    })


def get_ref_of_the_route(array):
    if "ref" in array:
        return array["ref"]
    return ""


def get_relation_type(array):
    if "type" in array:
        return array["type"]
    return ""


def get_way_ref(array):
    """:returns: The id of the way."""
    if "@ref" in array:
        return array["@ref"]
    return ""


def get_id_of_the_relation_members(array):
    return [member["@ref"] for member in array]


def get_the_refs_of_ways_in_the_relation(array):
    return [member["@ref"] for member in array if member["@type"] == "way"]


# input: nodes of the roundabout and the node sought that we want to search its connection.
def roundabout_checker(nodes_of_roundabout, nodes_of_previous_way):
    for node_of_roundabout in nodes_of_roundabout:
        for node_of_previous_way in nodes_of_previous_way:
            if node_of_roundabout == node_of_previous_way:
                return True
    return False


def check_connectivity(first_node_way1, last_node_way1, first_node_way2, last_node_way2):
    return (first_node_way1 == last_node_way2 or first_node_way2 == last_node_way1 or
            first_node_way1 == first_node_way2 or last_node_way1 == last_node_way2 or
            first_node_way1 == last_node_way1 or first_node_way2 == last_node_way2)


def check_if_directional(way_role):
    return way_role == "north" or way_role == "south" or way_role == "west" or way_role == "east"


def get_network(array):
    if "network" in array:
        return array["network"]
    return ""


def determine_if_country_has_MUTCD_or_similar(array):
    network = get_network(array)
    return True if ("US" or "CA" or "AU" or "NZ") in network else False
