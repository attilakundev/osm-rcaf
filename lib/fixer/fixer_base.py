from abc import ABC, abstractmethod
from src.lib import way_queries


class FixerBase(ABC):

    @abstractmethod
    def fixing(self, relation_info: dict, first_way: str = "", is_from_api: bool = True):
        pass

    def detect_differences_in_original_and_repaired_relation(self,
                                                             relation_data: dict,
                                                             relation_info: dict,
                                                             corrected_ways_to_search: dict):

        """
        Detects if a relation's members or ways were changed and put the action modifier to it,
        so JOSM can interpret as modified data.
        """
        original_ways_to_search = relation_info["ways_to_search"]
        # putting action=modify where change is detected
        # check the relation based on these: the size of the corrected ways to search,the tags of that and the order of the ways.
        if len(original_ways_to_search) != len(corrected_ways_to_search):
            relation_data["osm"]["relation"]["@action"] = "modify"
        original_way_refs = list(map(lambda x: x["@ref"], original_ways_to_search))
        for original_way in original_ways_to_search:
            for index, corrected_way in enumerate(corrected_ways_to_search):
                # check if the tags aren't the same or nodes aren't the same or if it's not in the original array
                if way_queries.get_way_ref(original_way) == way_queries.get_way_ref(
                        corrected_way) and (original_way[
                                                "tag"] != corrected_way[
                                                "tag"] or way_queries.get_nodes(
                    original_way) != way_queries.get_nodes(
                    corrected_way) or way_queries.get_way_ref(
                    corrected_way) not in original_way_refs):
                    corrected_ways_to_search[index]["attributes"]["@action"] = "modify"
        # check the order and roles in the relation
        original_roles = list(map(lambda x: x["@role"], original_ways_to_search))
        corrected_roles = list(map(lambda x: x["@role"], corrected_ways_to_search))
        original_way_order = list(map(lambda x: x["@ref"], original_ways_to_search))
        corrected_way_order = list(map(lambda x: x["@ref"], corrected_ways_to_search))
        if original_roles != corrected_roles or original_way_order != corrected_way_order:
            relation_data["osm"]["relation"]["@action"] = "modify"
        # now put the relation items back to the originally read array:
        relation_members = list(map(lambda x: {
            "@type": x["@type"],
            "@ref": x["@ref"],
            "@role": x["@role"]
        }, corrected_ways_to_search))
        relation_data["osm"]["relation"]["member"] = relation_members
        # now put the edited ways back to the original data extraction:
        # make the format of the original ways array:
        if len(original_ways_to_search) == 1 and len(corrected_ways_to_search) == 1:
            ways = {}
            for key, value in corrected_ways_to_search[0]["attributes"].items():
                ways[key] = value
            ways["nd"] = corrected_ways_to_search[0]["nd"]
            ways["tag"] = corrected_ways_to_search[0]["nd"]
        else:
            ways = []
            for corrected_way in corrected_ways_to_search:
                way = {}
                for key, value in corrected_way["attributes"].items():
                    way[key] = value
                way["nd"] = corrected_way["nd"]
                way["tag"] = corrected_way["tag"]
                ways.append(way)
        # now find the existing itens in the original ways array, and merge the results:
        if type(relation_data["osm"]["way"]) is list:
            for index, original_way in enumerate(relation_data["osm"]["way"]):
                for way in ways:
                    if original_way["@id"] == way["@id"]:
                        relation_data["osm"]["way"][index] = way
        else:
            relation_data["osm"]["way"] = ways
        return relation_data
