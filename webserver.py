import sys
from pathlib import Path

import uvicorn as uvicorn
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

project_path = Path(__file__).parent.absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/templates")

logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory=str(Path(project_path, "templates")))

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=f"{project_path}/static"),
    name="static",
)
app.add_middleware(SessionMiddleware,secret_key="someSecretKey")


@app.get("/", response_class=RedirectResponse)
async def home_page(request: Request):
    # redirecting the user - since this only just creates the variables that is used during the session
    request.session["language"] = "EN"
    request.session["debug_mode"] = "OFF"
    return "/analyzer"


@app.get("/analyzer", response_class=HTMLResponse)
async def analyzer_page(request: Request):
    context = {"request": request, "title": "OSMRCA", "language": request.session["language"],
               "css_path": "style.css", "debug_mode": request.session["debug_mode"]}
    return templates.TemplateResponse("main.html", context=context)


@app.get("/language", response_class=RedirectResponse)
async def change_language(request: Request):
    request.session["language"] = "EN" if request.session["language"] == "HU" else "HU"
    return "/analyzer"


@app.get("/debug_mode", response_class=RedirectResponse)
async def debug_mode_switch(request: Request):
    request.session["debug_mode"] = "OFF" if request.session["debug_mode"] == "ON" else "ON"
    return "/analyzer"


if __name__ == "__main__":
    uvicorn.run(app, port=80, log_level="info")
