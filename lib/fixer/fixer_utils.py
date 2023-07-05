import sys
from pathlib import Path

import xmltodict
project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/analyzer")
from analyzer import Analyzer

analyzer = Analyzer()
def add_tag_to_item(key, value, array: dict):
    tag = {
        "@k": key,
        "@v": value
    }
    if type(array["tag"]) is dict:
        array["tag"] = [array["tag"]]
    array["tag"].append(tag)
    return array


def swap_items(items, first_index, second_index):
    temp = items[first_index]
    items[first_index] = items[second_index]
    items[second_index] = temp
    return items


def search_for_tag(array, key, value):
    if type(array["tag"]) is dict:
        if array["tag"]["@k"] == key and array["tag"]["@v"] == value:
            return True
    else:
        for tag in array["tag"]:
            if tag["@k"] == key and tag["@v"] == value:
                return True
    return False

def get_relation_info(file_path):
    file = open(file_path, "r").read()
    data = xmltodict.parse(file)
    relation_info = analyzer.get_relation_info(loaded_relation_file=data)
    return relation_info
