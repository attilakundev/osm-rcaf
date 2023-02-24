import json
import os
import sys
from dataclasses import asdict
import time
from pathlib import Path

import xmltodict
import datetime

project_path = Path(__file__).resolve().parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/models")
sys.path.append(f"{project_path}/lib/analyzer")
sys.path.append(f"{project_path}/lib/fixer")

import webserver_utils
import uvicorn
import logging

from fastapi import FastAPI, Request, Response, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from osm_data_parser import OSMDataParser
from osm_error_messages import OSMErrorMessages
from analyzer import Analyzer
from fixer import RelationFixer

project_path = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory=str(Path(project_path, "templates")))

app = FastAPI()
data_parser = OSMDataParser()
osm_error_messages = OSMErrorMessages()
analyzer = Analyzer()
fixer = RelationFixer()

app.mount(
    "/static",
    StaticFiles(directory=f"{project_path}/static"),
    name="static",
)
app.add_middleware(SessionMiddleware, secret_key="someSecretKey")


# The secret key is just a dummy key, we don't use any user information
# But the session is used for storing the current user's language, title(based on it),
# the stored relation, corrected relation
def check_session_variables(request):
    if request.session.get("debug_mode") is None:
        request.session["debug_mode"] = False
    if request.session.get("loaded_relation") is None:
        request.session["loaded_relation"] = []
    if request.session.get("error_messages") is None:
        request.session["error_messages"] = []  # contains errors about the classes
    if request.session.get("uploaded_files") is None:
        request.session["uploaded_files"] = []  # contains errors about the classes
    return request


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    request = check_session_variables(request)
    request.session["error_messages"] = []  # empty it because we're not supposed to have results on the main route
    context = {"request": request, "debug_mode": request.session["debug_mode"],
               "error_messages": request.session["error_messages"], "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    context = {"request": request, "active_page": "about"}
    return templates.TemplateResponse("about.html", context=context)


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_url(request: Request, relation_id: str = Form(...)):
    request = check_session_variables(request)
    relation_data = data_parser.retrieve_XML_from_API(relation_id)
    if relation_data != {}:

        error_information, correct_ways_count = analyzer.relation_checking(relation_data, relation_id)
        error_messages = osm_error_messages.return_messages(error_information, correct_ways_count, relation_id, "",
                                                            request.session["debug_mode"])
        error_messages = webserver_utils.split_messages_between_newlines(error_messages)
        error_messages = [[len(message), message] for message in error_messages]
    else:
        not_existing = [[0, "This relation doesn't exist."]]
        error_messages = [[len(not_existing), not_existing]]
    request.session["error_messages"] = error_messages
    # do something here to store the relation
    context = {"request": request, "debug_mode": request.session["debug_mode"],
               "error_messages": request.session["error_messages"], "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.post("/analyze_file", response_class=HTMLResponse)
async def analyze_file(request: Request, relation_file: UploadFile = File(...), relation_id: str = Form(...)):
    request = check_session_variables(request)
    xml_data = await relation_file.read()
    relation_data = xmltodict.parse(xml_data)

    current_time = datetime.datetime.now()
    formatted_date = current_time.strftime("%Y%m%d-%H%M%S")
    upload_file_location = f"{project_path}/uploads/{relation_file.filename.split('.')[0]}_{formatted_date}.json"

    # Analyzing
    error_information, correct_ways_count = analyzer.relation_checking(relation_data, relation_id)
    relation_info = analyzer.get_relation_info(relation_data, relation_id)
    error_messages = osm_error_messages.return_messages(error_information, correct_ways_count, relation_id,
                                                        upload_file_location,
                                                        request.session["debug_mode"])
    error_messages = webserver_utils.split_messages_between_newlines(error_messages)
    all_messages = [[len(message), message] for message in error_messages]

    if not (len(error_messages) == 1 and error_messages[0][0][1] == "This relation has no errors and gaps at all."):
        ways_to_choose_from = [int(x["@ref"]) for x in relation_info["ways_to_search"]]
        sorted_list = list(sorted(ways_to_choose_from))
    else:
        sorted_list = []
    request.session["error_messages"] = all_messages

    parent_of_upload_file = Path(upload_file_location).resolve().parent
    if not Path.exists(parent_of_upload_file):
        os.mkdir(f"{project_path}/uploads")
    with open(upload_file_location, "w+") as file:
        file.write(json.dumps(relation_data, indent=4))
    request.session["uploaded_files"].append(upload_file_location)
    context = {"request": request, "debug_mode": request.session["debug_mode"],
               "error_messages": request.session["error_messages"], "sorted_ways_list": sorted_list, "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.post("/fix")
async def fix_relation(request: Request, first_way: str = Form(...)):
    request = check_session_variables(request)
    if request.session["uploaded_files"]:
        file = open(request.session["uploaded_files"][-1]).read()
        data = json.loads(file)
        relation_info = analyzer.get_relation_info(loaded_relation_file=data)
        corrected_ways_to_search, already_added_members = fixer.fixing(relation_info=relation_info, first_way=first_way,
                                                                       is_from_api=False)
        data = fixer.detect_differences_in_original_and_repaired_relation_and_return_relation_dictionary_accordingly(
            data, relation_info, corrected_ways_to_search)
        xml_to_return = data_parser.unparse_data_to_xml_prettified(data)
        for file in request.session["uploaded_files"]:
            os.remove(file)
        request.session["uploaded_files"] = []
    else:
        xml_to_return = '<?xml version="1.0" encoding="utf-8"?>' \
                        '<error>No files found to fix.</error>'
    return Response(content=xml_to_return, media_type="application/xml")


@app.get("/debug_mode", response_class=RedirectResponse)
async def debug_mode_switch(request: Request):
    request = check_session_variables(request)
    request.session["debug_mode"] = False if request.session["debug_mode"] is True else True
    return "/"


if __name__ == "__main__":
    uvicorn.run(app, port=5000, log_level="info")
