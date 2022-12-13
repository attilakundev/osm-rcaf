#!/usr/bin/python3
import pytest
import sys

from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib/model")
from previous_current import PreviousCurrentHighway
from previous_current import PreviousCurrentMultipolygon


def test_previous_curr_hwy():
    prev_curr_hwy = PreviousCurrentHighway(
        currently_checked_ref="33",
        previous_role="forward")
    assert prev_curr_hwy.currently_checked_ref == "33"
    assert prev_curr_hwy.previous_role == "forward"
    assert prev_curr_hwy.first_node_previous == ""


def test_previous_curr_multi():
    prev_curr_multi = PreviousCurrentMultipolygon(
        currently_sought_role="outer",
        previous_role="inner")
    assert prev_curr_multi.currently_sought_role == "outer"
    assert prev_curr_multi.previous_role == "inner"
    assert prev_curr_multi.first_node_previous == ""
