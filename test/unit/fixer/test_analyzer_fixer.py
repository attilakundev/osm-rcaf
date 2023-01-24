#!/usr/bin/python3
import sys
from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/fixer")
sys.path.append(f"{project_path}/lib/model")
sys.path.append(f"{project_path}/test/files")
from highway_fixer import HighwayFixer
import analyzer_dicts
import way_queries

highway_fixer = HighwayFixer()


def test_search_for_connection_exiting_from_closed_roundabout_if_exit_split():
    # Arrange
    # Act
    # Assert
    pass
def test_search_for_connection_exiting_from_closed_roundabout_if_exit_not_split():
    # Arrange
    # Act
    # Assert
    pass