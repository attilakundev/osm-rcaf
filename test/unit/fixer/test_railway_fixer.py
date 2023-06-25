import sys
from pathlib import Path

NOT_SUPPORTED = "not supported"

NOT_IMPLEMENTED_YET = "Not implemented yet"

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/fixer")
from fixer import RailwayFixer
fixer = RailwayFixer()

def test_fixing_function():
    relation_info = {}
    corrected_ways_to_search = fixer.fixing(relation_info)
    assert corrected_ways_to_search is None