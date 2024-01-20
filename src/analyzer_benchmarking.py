import logging
import os
import random
import sys
import time
import xml

import click
import pandas as pd

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
            logging.FileHandler(f"{log_path}"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_result_of_one_relation(relation_id, outdir, source, verbose):
    analyzer = Analyzer()
    data = {}
    multiplier = 1
    timer = 1
    tries = 1
    start_time_api = 0
    while not data:
        time_to_wait = 2 if timer * multiplier > 2 else timer * multiplier
        print(f"Trying to get relation {relation_id}, try #{tries}, waiting {time_to_wait}s"
              f" before retrieval")
        time.sleep(timer * multiplier)
        try:
            start_time_api = time.time()
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
        error_messages = return_messages(error_information, correct_ways_count,
                                         amount_to_decrease_from_errors, relation_id,
                                         source,
                                         verbose)
        display_errors(error_messages, len(error_information), amount_to_decrease_from_errors,
                       outdir, relation_id)
    else:
        start_time_checking, start_time_error_display = 0, 0
        end_time_checking, end_time_error_display = 0, 0
        error_messages = []
        print(f"Data unavailable for {relation_id}")

    time_passed_api = end_time_api - start_time_api
    time_passed_checking = end_time_checking - start_time_checking
    return error_messages, time_passed_api, time_passed_checking


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


def draw_chart(all_data, filename):
    list_of_data = [[str(key), value["time_passed_api"], value["time_passed_checking"]] for key, value in all_data.items()]
    df = pd.DataFrame(list_of_data, columns=["Amount of relations", "Time passed loading from API",
                                             "Time passed checking"])
    print(df)
    ax = df.plot(x='Amount of relations', kind='bar', stacked=True,
                 title='Performance of Analyzer based on amount of relations')
    ax.set(ylabel="Time (s)")
    ax.get_figure().savefig(filename)


@click.command()
@click.option("--source", "-s", required=True, default="", help="The source file which is used "
                                                                "for taking relations from for "
                                                                "benchmarking.")
@click.option("--relationamounts", "-ra", default="", required=True,
              help="The amounts to take from the relation list file. Separated with a comma. (10,"
                   "20)")
@click.option("--outdir", "-o", show_default=True, required=True, default="",
              help="The output folder where you want the logs and xml files.")
@click.option("--logfile", "-l", required=True, help="The logfile location where you want the "
                                                     "output to be saved.")
def benchmarking(source: str, relationamounts: str, outdir: str, logfile: str):
    logging_setup_cli(log_path=logfile)
    stats = {}
    file = open(source, "r")
    amounts = relationamounts.split(",")
    relation_ids = [relation_id[:-1] if "\n" in relation_id else relation_id for relation_id in
                    file.readlines()]
    for amount in amounts:
        logging.info("Waiting 20 seconds, so the API calms down.")
        time.sleep(20)
        random.shuffle(relation_ids)
        logging.info(f"Contains {amount} relation IDs")
        stats[amount] = {"time_passed_api": 0, "time_passed_checking": 0}
        for relation_id in relation_ids[0:int(amount)]:
            error_messages, time_passed_api, time_passed_checking = \
                get_result_of_one_relation(relation_id, outdir, True, False)
            stats[amount]["time_passed_api"] += time_passed_api
            stats[amount]["time_passed_checking"] += time_passed_checking
        total_time = stats[amount]['time_passed_api'] + \
                     stats[amount]['time_passed_checking']
        logging.info(f"Script ran for {amount} relations. Took {total_time} seconds.")
    draw_chart(stats, outdir + "chart.png")

entry_point.add_command(benchmarking)

if __name__ == '__main__':
    entry_point()
