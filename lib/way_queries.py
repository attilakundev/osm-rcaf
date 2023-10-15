def get_nodes(data):
    return [node["@ref"] for node in data["nd"]]


def get_start_node(data):
    return data["nd"][0]["@ref"]


def get_end_node(data):
    return data["nd"][len(data["nd"]) - 1]["@ref"]


def is_roundabout(data):
    if "tag" in data:
        for tag in data["tag"]:
            if tag["@k"] == "junction" and tag["@v"] == "roundabout":
                return True
    return False


def is_oneway(data):
    if "tag" in data:
        for tag in data["tag"]:
            if tag["@k"] == "oneway" and tag["@v"] == "yes":
                return True
    return False


def remove_tag(data, tag_key):
    if type(data["tag"]) == list:
        for key_value_pair in data["tag"]:
            if key_value_pair["@k"] == tag_key:
                data["tag"].remove(key_value_pair)
    else:
        data["tag"] = []  # since there was only just one dictionary here, we empty this
    return data


def modify_role(data, role):
    data["@role"] = role
    return data


def get_role(data):
    if "@role" in data:
        return data["@role"]
    return ""


def __get_tag_value__(data, tag):
    if "tag" in data:
        for key_value_pair in data["tag"]:
            if key_value_pair["@k"] == tag:
                return key_value_pair["@v"]
    return ""


def get_highway(data):
    return __get_tag_value__(data, "highway")

def get_index_of_way(array, ref_number):
    index = 0
    while index < len(array):
        if "@ref" in array[index] and array[index]["@ref"] == ref_number:
            return index
        index += 1
    return -1


def put_ref_from_relation_to_highway_way(data):
    ref = get_ref_of_the_route(data)
    for index, element in enumerate(data["ways"]):
        if element["@type"] == "way":
            for key_value_pair in element["tag"]:
                if key_value_pair["@k"] == "highway":
                    data["ways"][index]["tag"].append({
                        "@k": "ref",
                        "@v": ref
                    })


def __get_value_of_relation_or_way__(data, to_look_for):
    if to_look_for in data:
        return data[to_look_for]
    return ""


def get_ref_of_the_route(data):
    return __get_value_of_relation_or_way__(data, "ref")


def get_relation_type(data):
    return __get_value_of_relation_or_way__(data, "type")

def get_relation_member_type(data):
    return __get_value_of_relation_or_way__(data, "@type")


def get_way_ref(data):
    """:returns: The id of the way."""
    return __get_value_of_relation_or_way__(data, "@ref")


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
            first_node_way1 == last_node_way1)
def check_connectivity_between_two_ways(first_node_way1, last_node_way1, first_node_way2,
                                   last_node_way2):
    return (first_node_way1 == last_node_way2 or first_node_way2 == last_node_way1 or
            first_node_way1 == first_node_way2 or last_node_way1 == last_node_way2)

def check_if_directional(way_role):
    return way_role == "north" or way_role == "south" or way_role == "west" or way_role == "east"


def get_network(data):
    if "network" in data:
        return data["network"]
    return ""


# MUTCD stands for Manual on Uniform Traffic Control Devices (it's in the USA), and in this system
# the route signs are usually signed with cardinal directions like: US 60 EAST
# (https://www.aaroads.com/guides/us-060-az/). Canada, New Zealand and Australia
# follow similar routing system.
def determine_if_country_has_MUTCD_or_similar(data):
    network = get_network(data)
    return True if ("US" or "CA" or "AU" or "NZ") in network else False


def get_coordinates_of_relation(data) -> list[list[list[str]]]:
    nodes_of_relation_per_way = []
    coordinates = []
    try:
        for way in data["ways_to_search"]:
            nodes_of_relation_per_way.append([node["@ref"] for node in way["nd"]])
        for way in nodes_of_relation_per_way:
            coordinates.append(get_coordinates_of_a_way(way, data))
    except KeyError:
        coordinates = get_coordinates_of_nodes(
            data)  # use case: relation #67103 (it has only nodes)
    return coordinates


def get_coordinates_of_a_way(way, data):
    way_coordinates = []
    for node_to_search in way:
        for node in data["nodes"]:
            if node["@id"] == node_to_search and "@lat" in node and "@lon" in node:
                way_coordinates.append([node["@lat"], node["@lon"]])
    return way_coordinates


def get_coordinates_of_nodes(data):
    way_coordinates = []
    for node in data["nodes"]:
        if "@lat" in node and "@lon" in node:
            way_coordinates.append([node["@lat"], node["@lon"]])
    return way_coordinates


def get_relation(relation_id, data):
    if type(data["osm"]["relation"]) is list:
        for relation in data["osm"]["relation"]:
            if relation["@id"] == relation_id:
                return relation
    return data["osm"]["relation"]


def get_relation_ids(loaded_data):
    relations_list = loaded_data["osm"]["relation"]
    if type(relations_list) is dict:
        return relations_list["@id"]
    else:
        # We know it's a list
        return [relation["@id"] for relation in relations_list]
