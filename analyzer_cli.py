import logging
import os
import sys
import time
import xml

import click
import matplotlib.pyplot as plt
import pandas as pd
import xmltodict

from src.lib.analyzer.analyzer import Analyzer
from src.lib.osm_data_parser import retrieve_xml_from_api
from src.lib.osm_error_messages import return_messages

RELATION_NO_ERROR_AT_ALL = "This relation has no errors and gaps at all."


def logging_setup_cli(log_path: str):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f"{log_path}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_result_of_one_relation(relation_id, outdir, source, verbose):
    analyzer = Analyzer()
    data = {}
    multiplier = 1
    timer =1
    tries = 1
    start_time_api = time.time()
    while not data:
        time_to_wait = 2 if timer * multiplier > 2 else timer * multiplier
        print(f"Trying to get relation {relation_id}, try #{tries}, waiting {time_to_wait}s"
              f" before retrieval")
        time.sleep(timer * multiplier)
        try:
            data = retrieve_xml_from_api(relation_id)
        except xml.parsers.expat.ExpatError:
            tries += 1
            multiplier *= 2
    end_time_api = time.time()
    if data:
        start_time_checking = time.time()
        error_information, correct_ways_count, amount_to_decrease_from_errors = \
            analyzer.relation_checking(data, relation_id)
        end_time_checking = time.time()
        start_time_error_display = time.time()
        error_messages = return_messages(error_information, correct_ways_count,
                                         amount_to_decrease_from_errors, relation_id,
                                         source,
                                         verbose)
        display_errors(error_messages, len(error_information), amount_to_decrease_from_errors,
                       outdir, relation_id)
        end_time_error_display = time.time()
    else:
        start_time_checking, start_time_error_display = 0, 0
        end_time_checking, end_time_error_display = 0, 0
        error_messages = []
        print(f"Data unavailable for {relation_id}")

    time_passed_api = end_time_api - start_time_api
    time_passed_checking = end_time_checking - start_time_checking
    time_passed_error = end_time_error_display - start_time_error_display
    return error_messages, time_passed_api, time_passed_checking, time_passed_error


def display_errors(error_messages, error_length, amount_to_decrease_from_errors, outdir,
                   relation_id):
    if outdir != "":
        try:
            os.mkdir(f"{outdir}")
        except FileExistsError:
            pass  # we then don't create a folder
        with open(f"{outdir}/{relation_id}.txt", "w") as file:
            for message in error_messages:
                file.write(message + "\n")
            file.close()
        with open(f"{outdir}/results.txt", "a") as file:
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


@click.group()
def entry_point():
    pass


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
@click.option("--logfile", "-l", required=True, help="The logfile location where you want the "
                                                     "output to be saved.")
def analyzer(relation: str, source: str, relationcfg: str, outdir: str, verbose: str, logfile: str):
    logging_setup_cli(log_path=logfile)
    if relation == "" and source == "" and relationcfg == "":
        raise Exception("No input was entered. Please input a relation "
                        "(optionally: output file for the log) or a relation config file.")
    elif relation != "" and relationcfg == "" and source == "":
        start_time = time.time()
        relation_ids = relation.split(",")
        relations = []
        for relation_id in relation_ids:
            error_messages, _, _, _ = \
                get_result_of_one_relation(relation_id, outdir, source, verbose)
            relations.append(error_messages)
        end_time = time.time()
        logging.info(f"The script took {end_time - start_time} seconds")
    elif relation == "" and relationcfg != "" and source == "":
        # This is the batch processing. Unfortunately it is one threaded when you read it from OSM
        # API.
        start_time = time.time()
        file = open(relationcfg, "r")
        relation_ids = [relation_id[:-1] if "\n" in relation_id else relation_id for relation_id in
                        file.readlines()]
        relations = []
        for relation_id in relation_ids:
            error_messages, _, _, _ = \
                get_result_of_one_relation(relation_id, outdir, source, verbose)
            relations.append(error_messages)
        end_time = time.time()
        logging.info(f"The script took {end_time - start_time} seconds")
    elif relation != "" and relationcfg == "" and source != "":
        # This is when you read a file.
        start_time = time.time()
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
            display_errors(error_messages, len(error_information),
                           amount_to_decrease_from_errors, outdir,
                           relation)
            end_time = time.time()
            logging.info(f"The script took {end_time - start_time} seconds")
        else:
            print(f"Data unavailable for {relation}")

    else:
        raise Exception("Error: Either you haven't supplied relation ID when analyzing single "
                        "file, or you supplied both relationcfg and source.")


def draw_chart(all_data, filename):
    list_of_data = [[str(key), value["time_passed_init"], value["time_passed_api"],
                     value["time_passed_checking"], value["time_passed_error_display"]] for
                    key, value in all_data.items()]
    df = pd.DataFrame(list_of_data, columns=["Amount of relations", "Time passed since init",
                                             "Time passed loading from API", "Time passed checking",
                                             "time passed error displaying"])
    print(df)
    ax = df.plot(x='Amount of relations', kind='bar', stacked=True,
            title='Performance of Analyzer based on amount of relations')
    ax.set(ylabel="Time (s)")
    ax.get_figure().savefig(filename)


@click.command()
@click.option("--sourcefolder", "-sf", required=True, default="", help="The source folder which " \
                                                                       "contains the files.")
@click.option("--files", "-f", default="", required=True,
              help="The relation config files which you want to use for benchmarking. All must" \
                   "be in txt. Format of input: '50,100,150,200'")
@click.option("--outdir", "-o", show_default=True, required=True, default="",
              help="The output folder where you want the logs and xml files.")
@click.option("--logfile", "-l", required=True, help="The logfile location where you want the "
                                                     "output to be saved.")
def benchmarking(sourcefolder: str, files: str, outdir: str, logfile: str):
    logging_setup_cli(log_path=logfile)
    stats = {}
    relationcfg_files = files.split(",")
    for file in relationcfg_files:
        start_time_init = time.time()
        logging.info(f"Opening {file}.txt")
        file = open(sourcefolder + "/" + file + ".txt", "r")
        relation_ids = [relation_id[:-1] if "\n" in relation_id else relation_id for relation_id in
                        file.readlines()]
        logging.info(f"Contains {len(relation_ids)} relation IDs")

        relations = []
        end_time_init = time.time()
        time_passed_init = end_time_init - start_time_init
        stats[len(relation_ids)] = {"time_passed_init": time_passed_init, "time_passed_api": 0,
                                    "time_passed_checking": 0, "time_passed_error_display": 0}
        for relation_id in relation_ids:
            error_messages, time_passed_api, time_passed_checking, time_passed_error = \
                get_result_of_one_relation(relation_id, outdir, True, False)
            relations.append(error_messages)
            stats[len(relation_ids)]["time_passed_api"] += time_passed_api
            stats[len(relation_ids)]["time_passed_checking"] += time_passed_checking
            stats[len(relation_ids)]["time_passed_error_display"] += time_passed_error
        logging.info(f"Script ran for {len(relation_ids)} relations.")
    draw_chart(stats, outdir + "chart.png")


entry_point.add_command(analyzer)
entry_point.add_command(benchmarking)

if __name__ == '__main__':
    entry_point()
