import json
import os
import xmltodict
import datetime
import uvicorn
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Response, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from src.lib.osm_data_parser import unparse_data_to_xml_prettified, retrieve_xml_from_api
from src.lib import way_queries
from src.lib import webserver_utils
from src.lib.osm_data_parser import OSMDataParser
from src.lib.osm_error_messages import return_messages
from src.lib.analyzer.analyzer import Analyzer
from src.lib.fixer.fixer import RelationFixer

project_path = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory=str(Path(project_path, "templates")))

app = FastAPI()
data_parser = OSMDataParser()
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
    return request


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    request = check_session_variables(request)
    context = {"request": request, "debug_mode": request.session["debug_mode"],
               "error_messages": [], "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    context = {"request": request, "active_page": "about"}
    return templates.TemplateResponse("about.html", context=context)


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_url(request: Request, relation_id: str = Form(...)):
    request = check_session_variables(request)
    relation_data = retrieve_xml_from_api(relation_id)
    sorted_list = []
    coordinates = []
    if relation_data:
        error_information, correct_ways_count = analyzer.relation_checking(relation_data,
                                                                           relation_id)
        error_messages = return_messages(error_information, correct_ways_count,
                                         relation_id, True,
                                         request.session["debug_mode"])
        relation_info = analyzer.get_relation_info(relation_data, relation_id)
        coordinates = way_queries.get_coordinates_of_relation(relation_info)
        error_messages = webserver_utils.split_messages_between_newlines(error_messages)
        error_messages = [[len(message), message] for message in error_messages]
        # do something here to store the relation
        current_time = datetime.datetime.now()
        formatted_date = current_time.strftime("%Y%m%d-%H%M%S")

        if not (len(error_messages) == 3 and "This relation has no errors and gaps at all." in
                error_messages[2][1][0][
                    1]):
            ways_to_choose_from = [int(x["@ref"]) for x in relation_info["ways_to_search"]]
            sorted_list = list(sorted(ways_to_choose_from))
    else:
        not_existing = [[0, "This relation doesn't exist."]]
        error_messages = [[len(not_existing), not_existing]]
    context = {"request": request, "debug_mode": request.session["debug_mode"],
               "coordinates": coordinates,
               "error_messages": error_messages, "sorted_ways_list": sorted_list,
               "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.post("/analyze_file", response_class=HTMLResponse)
async def analyze_file(request: Request, relation_file: UploadFile = File(...),
                       relation_id: str = Form(...)):
    request = check_session_variables(request)
    xml_data = await relation_file.read()
    relation_data = xmltodict.parse(xml_data)

    # Analyzing
    error_information, correct_ways_count = analyzer.relation_checking(relation_data, relation_id)
    relation_info = analyzer.get_relation_info(relation_data, relation_id)
    error_messages = return_messages(error_information, correct_ways_count,
                                     relation_id,
                                     False,
                                     request.session["debug_mode"])
    error_messages = webserver_utils.split_messages_between_newlines(error_messages)
    all_messages = [[len(message), message] for message in error_messages]

    if not (len(error_messages) == 2 and "no errors and gaps" in error_messages[1][0][1]):
        ways_to_choose_from = [int(x["@ref"]) for x in relation_info["ways_to_search"]]
        sorted_list = list(sorted(ways_to_choose_from))
    else:
        sorted_list = []
    context = {"request": request, "debug_mode": request.session["debug_mode"], "coordinates": [],
               "error_messages": all_messages, "sorted_ways_list": sorted_list,
               "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.post("/fix")
async def fix_relation(request: Request, relation_file: UploadFile = File(...), first_way: str =
Form(...)):
    request = check_session_variables(request)
    xml_data = await relation_file.read()
    relation_data = xmltodict.parse(xml_data)
    if relation_data:
        relation_info = analyzer.get_relation_info(loaded_relation_file=relation_data)
        corrected_ways_to_search = fixer.fixing(relation_info=relation_info, first_way=first_way,
                                                is_from_api=False)
        if "Error" not in corrected_ways_to_search:
            corrected_ways_to_search = fixer.correct_way_roles_tags(relation_info,
                                                                    corrected_ways_to_search)
            relation_data = fixer.detect_differences_in_original_and_repaired_relation(
                relation_data, relation_info, corrected_ways_to_search)
            xml_to_return = unparse_data_to_xml_prettified(relation_data)
            return Response(content=xml_to_return, media_type="application/xml")
        else:
            errors = [1, [2, [0, corrected_ways_to_search["Error"]]]]
    else:
        errors = [1, [2, [0, "No files found to fix."]]]
    context = {"request": request, "debug_mode": request.session["debug_mode"], "coordinates": [],
               "error_messages": errors, "sorted_ways_list": [], "active_page": "home"}
    return templates.TemplateResponse("main.html", context=context)


@app.get("/debug_mode", response_class=RedirectResponse)
async def debug_mode_switch(request: Request):
    request = check_session_variables(request)
    request.session["debug_mode"] = False if request.session["debug_mode"] is True else True
    return "/"


if __name__ == "__main__":
    uvicorn.run(app, port=5000, host='0.0.0.0', log_level="info")
