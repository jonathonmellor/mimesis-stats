import pytest

from mimesis_stats.providers.base_stats import BaseStatsDataProvider


@pytest.mark.parametrize(
    "value, proportion, null_value, return_value",
    [(1, 0, None, 1), ("A", 1, None, None), ({"A": 1}, 0, None, {"A": 1}), (1, 1, "NULL", "NULL")],
)
def test_base_stats_replace(value, proportion, null_value, return_value):
    """Test does not require seed setting for deterministic results"""

    generator = BaseStatsDataProvider()

    assert generator._replace(value=value, proportion=proportion, replacement=null_value) == return_value


@pytest.mark.parametrize(
    "values, proportions, null_values, return_value",
    [
        ((1, 2, 3), [0, 0, 0], [None, None, None], (1, 2, 3)),
        ((1, 2, 3), [0, 1, 0], [None, None, None], (1, None, 3)),
    ],
)
def test_base_stats_replace_multiple(values, proportions, null_values, return_value):
    """Test does not require seed setting for deterministic results"""

    generator = BaseStatsDataProvider()

    assert generator._replace_multiple(values=values, proportions=proportions, replacements=null_values) == return_value
