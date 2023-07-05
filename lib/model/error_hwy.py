from dataclasses import dataclass, field
from src.lib.model.previous_current import PreviousCurrentHighway, PreviousCurrentMultipolygon


@dataclass
class ErrorHighway:
    prev_curr: PreviousCurrentHighway = field(default_factory=PreviousCurrentHighway)
    error_type: str = ""
    type: str = "Route"

@dataclass
class ErrorMultipolygon:
    prev_curr: PreviousCurrentMultipolygon = field(default_factory=PreviousCurrentMultipolygon)
    error_type: str = ""
    type: str = "Multipolygon"
