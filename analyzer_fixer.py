import logging
import multiprocessing
import sys
import os
import time

import click
from pathlib import Path

project_path = Path(__file__).resolve().parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib/analyzer")
from analyzer import Analyzer
from osm_data_parser import OSMDataParser
from osm_error_messages import OSMErrorMessages


def get_result_of_one_relation(relation_id, outdir, source, verbose):
    analyzer = Analyzer()
    osm_data_parser = OSMDataParser()
    osm_error_messages = OSMErrorMessages()
    data = {}
    multiplier = 1
    timer = 1
    tries = 1
    while not data:
        time_to_wait = 10 if timer * multiplier > 10 else timer * multiplier
        print(f"Trying to get relation {relation_id}, try #{tries}, waiting {time_to_wait}s before retrieval")
        time.sleep(timer * multiplier)
        data = osm_data_parser.retrieve_XML_from_API(relation_id)
        tries += 1
        multiplier *= 2
    if data:
        error_information, correct_ways_count = analyzer.relation_checking(data, relation_id)
        error_messages = osm_error_messages.return_messages(error_information, correct_ways_count, relation_id,
                                                            source,
                                                            verbose)
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
                if error_messages[2] == "This relation has no errors and gaps at all.":

                    file.write(f"[OK] {relation_id}: {error_messages[2]}\n")
                else:
                    file.write(f"[ERROR] {relation_id} has problems\n")
                file.close()
        else:
            for message in error_messages:
                print(message)
    else:
        error_messages = []
        print(f"Data unavailable for {relation_id}")
    return error_messages


@click.command()
@click.option("--relation", default="", help="Enter one or more relations separated by comma.")
@click.option("--source", show_default=True, default="",
              help="The source of the file you want to analyze.")
@click.option("--relationcfg", default="", help="The relation config file which you want to use. ")
@click.option("--outdir", show_default=True, default="",
              help="The output folder where you want the logs and xml files.")
@click.option("--verbose", is_flag=True, show_default=False, default=False, help="Get detailed log results.")
def program(relation: str, source: str, relationcfg: str, outdir: str, verbose: str):
    # make this runnable in parallel
    cpu_count = multiprocessing.cpu_count()
    if relation == "" and source == "" and relationcfg == "":
        raise Exception("No input was entered. Please input a relation "
                        "(optionally: output file for the log) or a relation config file.")
    elif relation != "" and relationcfg == "" and source == "":
        relation_ids = relation.split(",")
        # pool = multiprocessing.Pool(multiprocessing.cpu_count())
        relations = []
        for relation_id in relation_ids:
            relations.append(get_result_of_one_relation(relation_id, outdir, source, verbose))
            # pool.apply_async(func=get_result_of_one_relation, args=(relation_id, outdir, source, verbose,),
            #                 callback=relations.append)
        # pool.close()
        # pool.join()

    elif relation == "" and relationcfg != "" and source == "":
        file = open(relationcfg, "r")
        relation_ids = [relation_id[:-1] if "\n" in relation_id else relation_id for relation_id in file.readlines()]
        # pool = multiprocessing.Pool(2) if multiprocessing.cpu_count() > 1 else multiprocessing.Pool(1)
        relations = []
        for relation_id in relation_ids:
            relations.append(get_result_of_one_relation(relation_id, outdir, source, verbose))
            # pool.apply_async(func=get_result_of_one_relation, args=(relation_id, outdir, source, verbose,),
            #                 callback=relations.append)
        # pool.close()
        # pool.join()

    elif relation == "" and relationcfg == "" and source != "":
        print("To be implemented")
    else:
        raise Exception("More than two types of sources were selected for retrieving results. "
                        "Please use only one switch (either relation, relationcfg or source)")


if __name__ == "__main__":
    program()
