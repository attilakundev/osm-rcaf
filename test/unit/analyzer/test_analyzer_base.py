import sys
from dataclasses import dataclass

import xmltodict
from pathlib import Path

project_path = Path(__file__).parents[3].absolute()
sys.path.append(f"{project_path}")
sys.path.append(f"{project_path}/lib")
sys.path.append(f"{project_path}/lib/analyzer")
from analyzer_base import AnalyzerBase
def test_abstract_checking():
    AnalyzerBase.__abstractmethods__ = set()
    dummy_analyzer_base = AnalyzerBase()
    checking = dummy_analyzer_base.checking(None)
    assert checking is None
