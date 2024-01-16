# OpenStreetMap Relation Continuity Analyzer and Fixer 
This is a web application that can recognize the gaps in relations(routes, and any kind of multipolygons) in OpenStreetMap.

## How to use it?
You upload an existing relation, or you load it from a .osm/.xml file, and then when it detects problems, it will display you all of them if you turned on debug mode.

It offers you to go to the fixer page, where you can fix the relation. Then, after it fixed the relation, you can download the .osm file, and load it into JOSM,
to check if it corrected well.

If it corrected the relation well, hurray, you can upload it into OSM.

CLI version:
`python analyzer_cli.py --relation <relation id, can be separated with commas, not required> --source <source xml file, not required> --relationcfg <path to a text file containing multiple relation IDs, not required> --outdir <the path where the results will be stored> --verbose --logfile <name of the logfile, if you want>`


Webserver:
`python webserver.py` -> it will open it on port 5000 by default, but can be modified, if needed.

## Dependencies:
For normal running:
* Python 3.11
* Install requirements: `pip install -r requirements.txt`

For testing:
* pytest with coverage `pip install -U pytest pytest-cov`
