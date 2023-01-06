from dataclasses import dataclass, field


@dataclass
class PreviousCurrentHighway:
    currently_checked_ref: str = ""
    last_forward_way_before_backward_direction: list = field(default_factory=list)

    first_node_previous: str = ""
    first_node_current: str = ""
    last_node_previous: str = ""
    last_node_current: str = ""

    previous_role: str = ""
    previous_roundabout: bool = ""
    previous_oneway: bool = ""
    previous_ref: str = ""
    previous_highway: str = ""

    current_role: str = ""
    current_roundabout: bool = ""
    current_oneway: bool = ""
    current_ref: str = ""
    current_highway: str = ""


@dataclass
class PreviousCurrentMultipolygon:
    first_node_previous: str = ""
    first_node_current: str = ""
    last_node_previous: str = ""
    last_node_current: str = ""

    previous_ref: str = ""
    previous_role: str = ""
    current_ref: str = ""
    current_role: str = ""

    currently_sought_role_first_member_nodes: list = field(default_factory=list)
    currently_sought_role: str = ""
    ref_of_first_way_of_the_area: str = ""
