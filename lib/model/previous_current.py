from dataclasses import dataclass, field, asdict


@dataclass
class PreviousCurrentHighway:
    """
    This class contains everything that a relation's item would contain or during the lifecycle of
    checking
    """
    currently_checked_ref: str = ""
    first_node_of_first_forward_way_in_the_series: str = "0"
    last_node_of_first_forward_way_in_the_series: str = "0"

    first_node_previous: str = ""
    first_node_current: str = ""
    last_node_previous: str = ""
    last_node_current: str = ""

    previous_role: str = ""
    previous_roundabout: bool = False
    previous_oneway: bool = False
    previous_ref: str = ""
    previous_highway: str = ""

    current_role: str = ""
    current_roundabout: bool = False
    current_oneway: bool = False
    current_ref: str = ""
    current_highway: str = ""

    route_number: str = ""
    network: str = ""
    role_of_first_way: str = ""

    motorway_split_way: bool = False
    has_directional_roles: bool = False
    is_mutcd_country: bool = False

    count_of_forward_role_way_series: int = 0
    index_of_current_way: int = 0
    the_amount_to_be_decreased_from_length_of_error_information: int = 0
    pieces_of_roundabout: int = 0

    last_forward_way_ref_nodes_before_backward: list = field(default_factory=list)
    previous_nodes: list = field(default_factory=list)
    current_nodes: list = field(default_factory=list)
    last_roundabout_nodes: list = field(default_factory=list)
    roundabout_ways: list = field(default_factory=list)

    def as_dict(self):
        return asdict(self)


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
