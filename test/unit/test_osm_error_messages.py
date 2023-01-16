import sys

from pathlib import Path

project_path = Path(__file__).parents[2].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/test/files")

from osm_error_messages import OSMErrorMessages

error_messages = OSMErrorMessages()
def test_remote_relation():
    relation_id=23099
    source_empty = ""
    source_file = "file.xml"
    when_source_has_nothing = error_messages.remote_relation(relation_id,source_empty)
    when_source_has_content = error_messages.remote_relation(relation_id,source_file)
    assert when_source_has_nothing == "https://osm.org/relation/23099"
    assert when_source_has_content == 23099

def test_remote_way():
    way_id=1
    source_empty = ""
    source_file = "file.xml"
    when_source_has_nothing = error_messages.remote_way(way_id,source_empty)
    when_source_has_content = error_messages.remote_way(way_id,source_file)
    assert when_source_has_nothing == "https://osm.org/way/1"
    assert when_source_has_content == 1
