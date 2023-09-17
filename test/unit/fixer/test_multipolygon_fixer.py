from src.lib.fixer.multipolygon_fixer import MultipolygonFixer

fixer = MultipolygonFixer()


def test_fixing_function():
    relation_info = {}
    corrected_ways_to_search = fixer.fixing(relation_info)
    assert corrected_ways_to_search is None
