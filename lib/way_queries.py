def get_nodes(array):
    return [node["@ref"] for node in array["nd"]]


def get_start_node(array):
    return array["nd"][0]["@ref"]


def get_end_node(array):
    return array["nd"][len(array["nd"]) - 1]["@ref"]


def is_roundabout(array):
    for value in array["tag"]:
        if value["@k"] == "junction" and value["@v"] == "roundabout":
            return True
    return False


def is_oneway(array):
    for value in array["tag"]:
        if value["@k"] == "oneway" and value["@v"] == "yes":
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
    return array["@role"]


# in case we are dealing with route=road (or cycling etc.)
def get_highway(array):
    for key_value_pair in array["tag"]:
        if key_value_pair["@k"] == "highway":
            return key_value_pair["@v"]
    return ""


# in case we are dealing with route=railway
def get_railway(array):
    for key_value_pair in array["tag"]:
        if key_value_pair["@k"] == "railway":
            return key_value_pair["@v"]
    return ""


def get_highway_ref(array):
    for key_value_pair in array["tag"]:
        if key_value_pair["@k"] == "ref":
            return key_value_pair["@v"]
    return ""  # if empty, it means that the ref is not set, which is a problem. We need to put that from the way of the relation


def put_ref_from_relation_to_highway_way(array):  # this requires enumerate when for looping
    ref = get_ref_of_the_route(array)
    for index, way in enumerate(array["ways"]):
        for key_value_pair in way["tag"]:
            if key_value_pair["@k"] == "highway":
                array["ways"][index]["tag"].append({
                    "@k": "ref",
                    "@v": ref
                })


def get_ref_of_the_route(array):
    return array["ref"]


def get_id_of_the_relation_members(array):
    return [member["@ref"] for member in array]


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