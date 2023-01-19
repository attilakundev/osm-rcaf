import sys
from dataclasses import asdict
import time
from pathlib import Path

import xmltodict

project_path = Path(__file__).resolve().parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/models")
sys.path.append(f"{project_path}/lib/analyzer")

import webserver_utils
import uvicorn
import logging

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from osm_data_parser import OSMDataParser
from osm_error_messages import OSMErrorMessages
from analyzer import Analyzer

project_path = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory=str(Path(project_path, "templates")))

app = FastAPI()
data_parser = OSMDataParser()
osm_error_messages = OSMErrorMessages()
analyzer = Analyzer()

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
    return request


@app.get("/", response_class=HTMLResponse)
async def analyzer_page(request: Request):
    request = check_session_variables(request)
    request.session["error_messages"] = []  # empty it because we're not supposed to have results on the main route
    context = {"request": request,
               "css_path": "style.css", "debug_mode": request.session["debug_mode"],
               "error_messages": request.session["error_messages"]}
    return templates.TemplateResponse("main.html", context=context)


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
    context = {"request": request,
               "css_path": "style.css", "debug_mode": request.session["debug_mode"],
               "error_messages": request.session["error_messages"]}
    return templates.TemplateResponse("main.html", context=context)


@app.post("/analyze_file", response_class=HTMLResponse)
async def analyze_file(request: Request, relation_file: UploadFile = File(...)):
    request = check_session_variables(request)
    xml_data = await relation_file.read()

    relation_data = xmltodict.parse(xml_data)
    relation_ids = data_parser.get_relation_ids(relation_data)
    all_messages = []
    if type(relation_ids) == list:
        for relation_id in relation_ids:
            error_information, correct_ways_count = analyzer.relation_checking(relation_data,relation_id)
            error_messages = osm_error_messages.return_messages(error_information, correct_ways_count, relation_id,
                                                                "dummy_source",
                                                                request.session["debug_mode"])
            error_messages = webserver_utils.split_messages_between_newlines(error_messages)
            for message in error_messages:
                all_messages.append([len(message), message])
    else:
        print("AAA")
        error_information, correct_ways_count = analyzer.relation_checking(relation_data)
        error_messages = osm_error_messages.return_messages(error_information, correct_ways_count, relation_ids,
                                                            "dummy_source",
                                                            request.session["debug_mode"])
        error_messages = webserver_utils.split_messages_between_newlines(error_messages)
        all_messages = [[len(message), message] for message in error_messages]

    request.session["error_messages"] = all_messages
    request.session["xml_data"] = xml_data.decode("utf-8")
    context = {"request": request,
               "css_path": "style.css", "debug_mode": request.session["debug_mode"],
               "error_messages": request.session["error_messages"]}
    return templates.TemplateResponse("main.html", context=context)


@app.get("/fix")
async def analyze_file(request: Request):
    request = check_session_variables(request)
    return "/"


@app.get("/debug_mode", response_class=RedirectResponse)
async def debug_mode_switch(request: Request):
    request = check_session_variables(request)
    request.session["debug_mode"] = False if request.session["debug_mode"] is True else True
    return "/"


if __name__ == "__main__":
    uvicorn.run(app, port=5000, log_level="info")
