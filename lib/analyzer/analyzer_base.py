from abc import ABC, abstractmethod


class AnalyzerBase(ABC):

    @abstractmethod
    def checking(self, relation_info):
        pass
