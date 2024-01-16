# OpenStreetMap Relation Continuity Analyzer and Fixer 
This is a web application that can recognize the gaps in relations(routes, and any kind of multipolygons) in OpenStreetMap.

## How to use it?
Analyzing process: enter a relation ID / upload an .osm/xml file and then when it detects problems, it will display you all of them if you turned on debug mode.

It offers you to fix the relation from a given point which you select from a dropdown list. Then, after it fixed the relation, you can download the .osm/xml file, and load it into JOSM,
to check if it corrected well.

If it corrected the relation well, hurray, you can upload it into OSM.

CLI version:
`python analyzer_cli.py --relation <relation id, can be separated with commas, not required> --source <source xml file, not required> --relationcfg <path to a text file containing multiple relation IDs, not required> --outdir <the path where the results will be stored> --verbose --logfile <name of the logfile, if you want>`

Webserver:
`python webserver.py` -> it will open it on port 5000 by default, but can be modified, if needed. Then you just enter localhost:5000 (or 127.0.0.1:5000) and then you can use it.

For now, it can both analyze and fix route=* relations mostly, but for railroads, multipolygons it's limited to analyzing. There are a lot of deficiencies.

## Dependencies:
For normal running:
* Python 3.11
* Install requirements: `pip install -r requirements.txt`

For testing:
* pytest with coverage `pip install -U pytest pytest-cov`
