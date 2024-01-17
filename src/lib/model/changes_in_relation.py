from dataclasses import dataclass


@dataclass
class ChangesInRelation:
    index: int = 0
    old_id: str = ""
    old_role: str = ""
    new_id: str = ""
    new_role: str = ""
@dataclass
class DeletedItem:
    index: int = 0
    old_id: str = ""
    old_role: str = ""