import dataclasses
import logging

from src.lib import way_queries
from src.lib.model.changes_in_relation import ChangesInRelation, DeletedItem


def compare_two_relation_files(old_data, new_data, relation_id):
    """
    This function compares the differences in a relation between two files.
    """
    changes = []
    deletions = []
    try:
        old_relation = way_queries.get_relation(relation_id, old_data)["member"]
        corrected_relation = way_queries.get_relation(relation_id, new_data)["member"]
        old_ids = [item["@ref"] for item in old_relation]
        new_ids = [item["@ref"] for item in corrected_relation]
        for index, item in enumerate(corrected_relation):
            if old_ids[index] != item["@ref"]:
                changes.append(dataclasses.asdict(ChangesInRelation(index, old_ids[index],
                                                                    old_relation[index]["@role"],
                                                                    new_ids[index],
                                                                    corrected_relation[index][
                                                                        "@role"])))
        for index, item in enumerate(old_ids):
            if item not in new_ids:
                deletions.append(dataclasses.asdict(DeletedItem(index, item,
                                                                old_relation[index][
                                                                    "@role"])))
    except TypeError as error:
        logging.warning(f"{error}")
    return changes, deletions
