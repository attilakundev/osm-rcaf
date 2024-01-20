import logging
import os
import sys
import time
import xml
from pathlib import Path

import click
import xmltodict

from src.lib.analyzer.analyzer import Analyzer
from src.lib.osm_data_parser import retrieve_xml_from_api
from src.lib.osm_error_messages import return_messages
from src.lib.way_queries import get_relation_ids

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


@click.command()
@click.option("--path", "-p", show_default=True, default="",
              help="Path of the folder containing the XML files.",
              required=True)
@click.option("--outdir", "-o", show_default=True, default="",
              help="The output folder where you want the logs, it shows how accurate the routes "
                   "are.")
@click.option("--verbose", "-v", is_flag=True, show_default=False, default=False,
              help="Get detailed log results.")
@click.option("--logfile", "-l", required=False, help="The logfile location where you want the "
                                                     "output to be saved. This file is basically "
                                                     "the console output's log file.")
def analyzer(path: str, outdir: str, verbose: str, logfile: str):
    try:
        os.mkdir(f"{outdir}")
        logging_setup_cli(log_path=logfile)
    except FileExistsError:
        logging_setup_cli(log_path=logfile)
    files = Path(path).glob('*.xml')
    analyzer = Analyzer()
    for file in files:
        start_time = time.time()
        text = open(file, "r").read()
        data = xmltodict.parse(text)
        relation_id = get_relation_ids(data)
        if data:
            error_information, correct_ways_count, amount_to_decrease_from_errors = \
                analyzer.relation_checking(
                    data,relation_id)
            error_messages = return_messages(error_information, correct_ways_count,
                                             amount_to_decrease_from_errors, relation_id,
                                             False,
                                             verbose)
            display_errors(error_messages, len(error_information),
                           amount_to_decrease_from_errors, outdir,
                           relation_id)
            end_time = time.time()
            logging.info(f"The script took {end_time - start_time} seconds")
        else:
            print(f"Data unavailable for {relation_id}")


entry_point.add_command(analyzer)

if __name__ == '__main__':
    entry_point()
