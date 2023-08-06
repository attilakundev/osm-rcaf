import xmltodict
from src.lib.analyzer.analyzer import Analyzer

analyzer = Analyzer()
def add_tag_to_item(key, value, array: dict):
    """
    This function adds a tag to an item, let it be a node or a way.
    it gets a key value pair and assigns it to the proper place.
    """
    tag = {
        "@k": key,
        "@v": value
    }
    if type(array["tag"]) is dict:
        array["tag"] = [array["tag"]]
    array["tag"].append(tag)
    return array


def swap_items(items, first_index, second_index):
    """
    This is a simple swapping function, where the ways are swapped in the fixing function
    """
    temp = items[first_index]
    items[first_index] = items[second_index]
    items[second_index] = temp
    return items


def search_for_tag(array, key, value):
    """
    This function checks if the given key-value pair exists.
    """
    if type(array["tag"]) is dict:
        if array["tag"]["@k"] == key and array["tag"]["@v"] == value:
            return True
    else:
        for tag in array["tag"]:
            if tag["@k"] == key and tag["@v"] == value:
                return True
    return False

def get_relation_info(file_path):
    """
    This function reads the relation file, then parses it and returns data that is used inside
    this application.
    """
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    return relation_info
