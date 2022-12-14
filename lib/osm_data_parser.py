import requests
import xmltodict
from string import Template

OSM_API_RELATION_URL_TEMPLATE = Template(f"https://www.openstreetmap.org/api/0.6/relation/$relation/full")


class OSMDataParser:

    def retrieve_XML_from_API(self, relation_number):
        url = OSM_API_RELATION_URL_TEMPLATE.substitute(relation=relation_number)
        relation_file = requests.get(url).content
        dictionary = xmltodict.parse(relation_file)
        return dictionary

    # pull way and relation info to separate arrays (so they can be copied back)
    def gather_way_and_relation_info(self, data):
        relation_info: dict = {"nodes": [], "ways": [], "ways_to_search": []}
        for osmkey, osmvalue in data["osm"].items():
            if osmkey == "node":
                relation_info["nodes"] = list(map(lambda x: x, osmvalue))
            if osmkey == "way" and type(osmvalue) is list:
                relation_info["ways"] = list(map(lambda x: x, osmvalue))
            elif osmkey =="way" and type(osmvalue) is dict:
                relation_info["ways"] = [osmvalue]
            if osmkey == "relation" and type(osmvalue) is list:
                # we always go through the very first array, because we're NOT interested in the rest relations,
                # eg. Hungary's relation has 8 relations with itself, because it's member of other relations
                # but the very first is what WE need. We don't want to edit other relations.
                relation_info = self.__gather_relation_info__(osmvalue[0].items(), relation_info)
            elif osmkey == "relation" and type(osmvalue) is dict:
                # then do this for just one relation
                relation_info = self.__gather_relation_info__(osmvalue.items(), relation_info)
        return relation_info
    def __gather_relation_info__(self, relation, relation_info):
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
                        if key_value_pair["@k"] == "network":
                            relation_info["network"] = key_value_pair["@v"]
                            relation_info["isMUTCDcountry"] = \
                                "US" in key_value_pair["@v"] or "CA" in key_value_pair["@v"] or \
                                "AU" in key_value_pair["@v"] or "NZ" in key_value_pair["@v"]
                        else:
                            relation_info[key_value_pair["@k"]] = key_value_pair["@v"]
                else:
                    if value["@k"] == "network":
                        relation_info["network"] = value["@v"]
                        relation_info["isMUTCDcountry"] = \
                            "US" in value["@v"] or "CA" in value["@v"] or \
                            "AU" in value["@v"] or "NZ" in value["@v"]
                    else:
                        relation_info[value["@k"]] = value["@v"]
        # copy the ways to a separate array so the final result can be copied back there.
        return relation_info

    def append_ways_to_search_with_useful_info(self, relation_info):
        for i in range(0, len(relation_info["ways_to_search"])):
            for j in range(0, len(relation_info["ways"])):
                if relation_info["ways"][j]["@id"] == relation_info["ways_to_search"][i]["@ref"]:
                    relation_info["ways_to_search"][j]["attributes"] = self.__copy_attributes__(
                        relation_info["ways"][i])
                    relation_info["ways_to_search"][j]["nd"] = relation_info["ways"][i]["nd"]
                    if "tag" in relation_info["ways_to_search"][j]:
                        relation_info["ways_to_search"][j]["tag"] = relation_info["ways"][i]["tag"]
        return relation_info
    def __copy_attributes__(self, attributes):
        attributes = {key: value for key, value in attributes.items() if "@" in key}
        return attributes
    def collect_information_about_the_relation(self, data):
        return_value: dict = self.append_ways_to_search_with_useful_info(self.gather_way_and_relation_info(data))
        return return_value
