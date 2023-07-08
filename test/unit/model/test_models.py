#!/usr/bin/python3

from src.lib.model.previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon
from src.lib.model.error_hwy import ErrorHighway, ErrorMultipolygon


def test_previous_curr_hwy():
    prev_curr_hwy = PreviousCurrentHighway(
        currently_checked_ref="33",
        previous_role="forward", previous_roundabout=True)
    error_hwy = ErrorHighway(prev_curr=prev_curr_hwy, error_type="asdf")

    assert error_hwy.prev_curr.currently_checked_ref == "33"
    assert error_hwy.prev_curr.previous_role == "forward"
    assert error_hwy.prev_curr.first_node_previous == ""
    assert error_hwy.prev_curr.previous_roundabout is True
    assert error_hwy.error_type == "asdf"


def test_previous_curr_multi():
    prev_curr_multi = PreviousCurrentMultipolygon(
        currently_sought_role="outer",
        previous_role="inner")
    error_multi = ErrorMultipolygon(prev_curr=prev_curr_multi, error_type="asdf")
    assert error_multi.prev_curr.currently_sought_role == "outer"
    assert error_multi.prev_curr.previous_role == "inner"
    assert error_multi.prev_curr.first_node_previous == ""
    assert error_multi.error_type == "asdf"
