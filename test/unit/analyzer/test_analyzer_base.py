from src.lib.analyzer.analyzer_base import AnalyzerBase


def test_abstract_checking():
    AnalyzerBase.__abstractmethods__ = set()
    dummy_analyzer_base = AnalyzerBase()
    checking = dummy_analyzer_base.checking(None,None)
    assert checking is None
