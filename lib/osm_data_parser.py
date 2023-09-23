import requests
import xmltodict
from string import Template

OSM_API_RELATION_URL_TEMPLATE = Template(f"https://www.openstreetmap.org/api/0.6/relation/"
                                         f"$relation/full")


def retrieve_xml_from_api(relation_number):
    url = OSM_API_RELATION_URL_TEMPLATE.substitute(relation=relation_number)
    relation_file = requests.get(url)
    dictionary = xmltodict.parse(relation_file.content)
    return dictionary


def unparse_data_to_xml_prettified(data):
    return xmltodict.unparse(data, pretty=True, short_empty_elements=True, encoding="utf-8")


def check_way_attributes_id(relation_info):
    result = []
    for i in range(len(relation_info["ways_to_search"])):
        try:
            result.append(relation_info["ways_to_search"][i]["attributes"]["@id"])
        except KeyError:
            currently_checked_way = relation_info['ways_to_search'][i]['@ref']
            raise KeyError(
                f"The relation's way ({currently_checked_way}) doesn't exist in the <way> tags,"
                f" this is mostly a unit-testing issue, please fix it.")
    return result


def __copy_attributes__(way):
    attributes = {key: value for key, value in way.items() if "@" in key}
    return attributes


def append_ways_to_search_with_useful_info(relation_info):
    for i in range(0, len(relation_info["ways_to_search"])):
        for j in range(0, len(relation_info["ways"])):
            if relation_info["ways"][j]["@id"] == relation_info["ways_to_search"][i]["@ref"]:
                relation_info["ways_to_search"][i]["attributes"] = __copy_attributes__(
                    relation_info["ways"][j])
                relation_info["ways_to_search"][i]["nd"] = relation_info["ways"][j]["nd"]
                if "tag" in relation_info["ways"][j]:
                    if type(relation_info["ways"][j]["tag"]) is dict:
                        relation_info["ways_to_search"][i]["tag"] = []
                        relation_info["ways_to_search"][i]["tag"].append(
                            relation_info["ways"][j]["tag"])
                    else:
                        relation_info["ways_to_search"][i]["tag"] = relation_info["ways"][j][
                            "tag"]
    return relation_info


def __gather_relation_info__(relation, relation_info):
    for key, value in relation:
        if key == "member":
            if type(value) is list:
                for member in value:
                    relation_info["ways_to_search"].append(member)
            else:
                relation_info["ways_to_search"].append(value)
        elif key == "tag":
            if type(value) is list:
                for key_value_pair in value:
                    relation_info[key_value_pair["@k"]] = key_value_pair["@v"]
                    if key_value_pair["@k"] == "network":
                        relation_info["isMUTCDcountry"] = \
                            "US" in key_value_pair["@v"] or "CA" in key_value_pair["@v"] or \
                            "AU" in key_value_pair["@v"] or "NZ" in key_value_pair["@v"]
            else:
                relation_info[value["@k"]] = value["@v"]
                if value["@k"] == "network":
                    relation_info["isMUTCDcountry"] = \
                        "US" in value["@v"] or "CA" in value["@v"] or \
                        "AU" in value["@v"] or "NZ" in value["@v"]
    # copy the ways to a separate array so the final result can be copied back there.
    return relation_info


def get_relation_ids(loaded_data):
    relations_list = loaded_data["osm"]["relation"]
    if type(relations_list) is dict:
        return relations_list["@id"]
    else:
        # We know it's a list
        return [relation["@id"] for relation in relations_list]


def gather_way_and_relation_info(data, relation_id: str = ""):
    """
    pull way and relation info to separate arrays (so they can be copied back)
    """
    # ways_to_search is they way the ways are ordered in the relation.
    relation_info: dict = {"nodes": [], "ways": [], "ways_to_search": []}
    for osmkey, osmvalue in data["osm"].items():
        if osmkey == "node":
            relation_info["nodes"] = list(map(lambda x: x, osmvalue))
        if osmkey == "way" and type(osmvalue) is list:
            relation_info["ways"] = list(map(lambda x: x, osmvalue))
        elif osmkey == "way" and type(osmvalue) is dict:
            relation_info["ways"] = [osmvalue]
        if osmkey == "relation" and type(osmvalue) is list:
            if relation_id != "":
                index = \
                    [index for index, relation in enumerate(osmvalue) if
                     relation["@id"] == relation_id][0]  # deal with only the 1st relation
                relation_info = __gather_relation_info__(osmvalue[index].items(),
                                                         relation_info)
            else:
                relation_info = __gather_relation_info__(osmvalue[0].items(),
                                                         relation_info)
            return relation_info
        if osmkey == "relation" and type(osmvalue) is dict:
            # then do this for just one relation
            relation_info = __gather_relation_info__(osmvalue.items(), relation_info)
            return relation_info


def collect_information_about_the_relation(data, relation_id):
    return_value: dict = append_ways_to_search_with_useful_info(
        gather_way_and_relation_info(data, relation_id))
    return return_value
