# OpenStreetMap Relation Continuity Analyzer and Fixer 
This is a web application that can recognize the gaps in relations(routes, and any kind of multipolygons) in OpenStreetMap.

## How to use it?
You upload an existing relation, or you load it from a .osm/.xml file, and then when it detects problems, it will display you all of them if you turned on debug mode.

It offers you to go to the fixer page, where you can fix the relation. Then, after it fixed the relation, you can download the .osm file, and load it into JOSM,
to check if it corrected well.

If it corrected the relation well, hurray, you can upload it into OSM.

## Dependencies:
* Python 3.10
* FastAPI framework `pip install fastapi`
* uvicorn `pip install uvicorn["standard"]`
* [osm-login-python](https://github.com/kshitijrajsharma/osm-login-python) 
* pytest `pip install -U pytest`
