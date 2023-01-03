import sys
from pathlib import Path
project_path = Path(__file__).resolve().parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")

import uvicorn
import logging
import starlette.status as status

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from osm_data_parser import OSMDataParser
from analyzer import Analyzer
project_path = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory=str(Path(project_path, "templates")))

app = FastAPI()
OSMXMLParser = OSMDataParser()
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
    if request.session.get("language") is None:
        request.session["language"] = "EN"
        request.session["title"] = "OpenStreetMap Relation Continuity Analyzer and Fixer"
    if request.session.get("debug_mode") is None:
        request.session["debug_mode"] = "OFF"
    if request.session.get("loaded_relation") is None:
        request.session["loaded_relation"] = []
    if request.session.get("errors") is None:
        request.session["errors"] = [] # will contain ErrorModel classes or similar to this
    if request.session.get("relationData") is None:
        request.session["relationData"] = {} #Dictionary, like: relation = 23099, number_of_ways = 1009 etc.
    return request

@app.get("/", response_class=HTMLResponse)
async def analyzer_page(request: Request):
    request = check_session_variables(request)
    context = {"request": request, "title": request.session["title"], "language": request.session["language"],
               "css_path": "style.css", "debug_mode": request.session["debug_mode"],
               "loaded_relation": request.session["loaded_relation"],
               "errors": request.session["errors"], "relationData": request.session["relationData"]}
    return templates.TemplateResponse("main.html", context=context)


@app.post("/analyze")
async def analyze_url(request: Request, relation_id: str = Form(...)):
    request = check_session_variables(request)
    #request.session["loaded_relation"] = OSMXMLParser.retrieve_XML_from_API(relation_id)
    #request.session["errors"], relation_length = analyzer.relation_checking(request.session["loaded_relation"])
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@app.post("/analyze_file")
async def analyze_file(request: Request, relation_file: UploadFile = File(...)):
    request = check_session_variables(request)
    xml_content = await relation_file.read()
    #request.session["loaded_relation"] = OSMXMLParser.parse_XML(xml_content)
    # request.session["errors"] = analyzer.analyze(request.session["loaded_relation"])
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@app.get("/language", response_class=RedirectResponse)
async def change_language(request: Request):
    request = check_session_variables(request)
    request.session["language"] = "EN" if request.session["language"] != "EN" else "HU"
    if request.session["language"] == "EN":
        request.session["title"] = "OpenStreetMap Relation Continuity Analyzer and Fixer"
    else:
        request.session["title"] = "OpenStreetMap Kapcsolat Folytonosság Elemző és Javító"
    return "/"


@app.get("/debug_mode", response_class=RedirectResponse)
async def debug_mode_switch(request: Request):
    request = check_session_variables(request)
    request.session["debug_mode"] = "OFF" if request.session["debug_mode"] == "ON" else "ON"
    return "/"


if __name__ == "__main__":
    uvicorn.run(app, port=5000, log_level="info")
