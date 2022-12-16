from dataclasses import dataclass
from previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon


@dataclass
class ErrorHighway:
    prev_curr: PreviousCurrentHighway
    error_type: str

@dataclass
class ErrorMultipolygon:
    prev_curr: PreviousCurrentMultipolygon
    error_type: str
