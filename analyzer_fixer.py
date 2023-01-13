import sys
import click
from pathlib import Path

project_path = Path(__file__).resolve().parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib/analyzer")
from analyzer import Analyzer
from osm_data_parser import OSMDataParser
from osm_error_messages import OSMErrorMessages


@click.command()
@click.option("--relation", required=True, help="Enter one or more relations separated by comma.")
@click.option("--email", help="The email address you want to send the results, if you want to do that.\n"
                              "Set USERNAME and PASSWORD environment variables with some value, do use this as "
                              "the sender.\t")
@click.option("--source", show_default=True, default="",
              help="The source of the file you want to analyze.")
@click.option("--relationcfg", default=True, help="The relation config file which you want to use.(to be implemented) ")
@click.option("--output", show_default=True, default=".",
              help="The output folder where you want the logs and xml files.")
@click.option("--verbose", is_flag=True, show_default=False, default=False, help="Get detailed log results.")
#@click.option("--language", show_default=True, default="en", help="Available languages: en, hu")
def program(relation: str, email: str, source: str, relationcfg: str, output: str, verbose: str):
    analyzer = Analyzer()
    osm_data_parser = OSMDataParser()
    osm_error_messages = OSMErrorMessages()
    amount_of_relations = relation.split(",")
    # make this runnable in parallel
    for relation_id in amount_of_relations:
        data = osm_data_parser.retrieve_XML_from_API(relation_id)
        error_information, correct_ways_count = analyzer.relation_checking(data, relation_id)
        error_messages = osm_error_messages.return_messages(error_information, correct_ways_count, relation_id, source,
                                                            verbose)
        for message in error_messages:
            print(message)


if __name__ == "__main__":
    program()
