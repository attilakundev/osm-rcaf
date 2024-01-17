from abc import ABC, abstractmethod


class FixerBase(ABC):

    @abstractmethod
    def fixing(self, relation_info: dict, first_way: str = "", is_from_api: bool = True):
        pass
