from dataclasses import dataclass
from previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon


@dataclass
class ErrorHighway:
    prev_curr: PreviousCurrentHighway = PreviousCurrentHighway()
    error_type: str = ""

@dataclass
class ErrorMultipolygon:
    prev_curr: PreviousCurrentMultipolygon = PreviousCurrentMultipolygon()
    error_type: str = ""
