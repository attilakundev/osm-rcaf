import os
import time

import click
import xmltodict

from src.lib.analyzer.analyzer import Analyzer
from src.lib.osm_data_parser import retrieve_xml_from_api
from src.lib.osm_error_messages import return_messages
from src.webserver import project_path

RELATION_NO_ERROR_AT_ALL = "This relation has no errors and gaps at all."


def get_result_of_one_relation(relation_id, outdir, source, verbose):
    analyzer = Analyzer()
    data = {}
    multiplier = 1
    timer = 1
    tries = 1
    while not data:
        time_to_wait = 10 if timer * multiplier > 10 else timer * multiplier
        print(f"Trying to get relation {relation_id}, try #{tries}, waiting {time_to_wait}s"
              f" before retrieval")
        time.sleep(timer * multiplier)
        data = retrieve_xml_from_api(relation_id)
        tries += 1
        multiplier *= 2
    if data:
        error_information, correct_ways_count, amount_to_decrease_from_errors = \
            analyzer.relation_checking(data, relation_id)
        error_messages = return_messages(error_information, correct_ways_count,
                                         amount_to_decrease_from_errors, relation_id,
                                         source,
                                         verbose)
        display_errors(error_messages, len(error_information), amount_to_decrease_from_errors,
                       outdir, \
            relation_id)
    else:
        error_messages = []
        print(f"Data unavailable for {relation_id}")
    return error_messages


def display_errors(error_messages, error_length, amount_to_decrease_from_errors, outdir,
                   relation_id):
    if outdir != "":
        try:
            os.mkdir(f"{project_path}/{outdir}")
        except FileExistsError:
            pass  # we then don't create a folder
        with open(f"{project_path}/{outdir}/{relation_id}.txt", "w") as file:
            for message in error_messages:
                file.write(message + "\n")
            file.close()
        with open(f"{project_path}/{outdir}/results.txt", "a") as file:
            if len(error_messages) == 2 and error_messages[1] == RELATION_NO_ERROR_AT_ALL or (len(
                error_messages) == 4 and error_messages[3] == RELATION_NO_ERROR_AT_ALL):
                file.write(f"[OK] {relation_id}: {RELATION_NO_ERROR_AT_ALL}\n")
            else:
                errors = error_length - amount_to_decrease_from_errors
                file.write(f"[ERROR] {relation_id} has {errors}"
                           " problem(s)\n")
            file.close()
    else:
        for message in error_messages:
            print(message)


@click.command()
@click.option("--relation", "-r", default="", help="Enter one or more relations separated by " \
                                                   "comma.")
@click.option("--source", "-s", show_default=True, default="",
              help="The source of the file you want to analyze.")
@click.option("--relationcfg", "-rc", default="", help="The relation config file which you want "
                                                       "to use. ")
@click.option("--outdir", "-o", show_default=True, default="",
              help="The output folder where you want the logs and xml files.")
@click.option("--verbose", "-v", is_flag=True, show_default=False, default=False,
              help="Get detailed log results.")
def program(relation: str, source: str, relationcfg: str, outdir: str, verbose: str):
    if relation == "" and source == "" and relationcfg == "":
        raise Exception("No input was entered. Please input a relation "
                        "(optionally: output file for the log) or a relation config file.")
    elif relation != "" and relationcfg == "" and source == "":
        relation_ids = relation.split(",")
        relations = []
        for relation_id in relation_ids:
            relations.append(get_result_of_one_relation(relation_id, outdir, source, verbose))

    elif relation == "" and relationcfg != "" and source == "":
        # This is the batch processing. Unfortunately it is one threaded when you read it from OSM
        # API.
        file = open(relationcfg, "r")
        relation_ids = [relation_id[:-1] if "\n" in relation_id else relation_id for relation_id in
                        file.readlines()]
        relations = []
        for relation_id in relation_ids:
            relations.append(get_result_of_one_relation(relation_id, outdir, source, verbose))
    elif relation != "" and relationcfg == "" and source != "":
        # This is when you read a file.
        analyzer = Analyzer()
        file = open(source, "r").read()
        data = xmltodict.parse(file)
        if data:
            error_information, correct_ways_count, amount_to_decrease_from_errors = \
                analyzer.relation_checking(
                data, relation)
            error_messages = return_messages(error_information, correct_ways_count,
                                             amount_to_decrease_from_errors, relation,
                                             False,
                                             verbose)
            display_errors(error_messages,  len(error_information),
                           amount_to_decrease_from_errors, outdir,
                           relation)
        else:
            print(f"Data unavailable for {relation}")

    else:
        raise Exception("Error: Either you haven't supplied relation ID when analyzing single "
                        "file, or you supplied both relationcfg and source.")


if __name__ == "__main__":
    program()
