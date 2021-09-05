import pytest

from mimesis_stats.providers.distribution import Distribution


@pytest.mark.parametrize(
    "population, weights, return_value",
    [
        (["A", "B"], [0, 1], "B"),
        (["A", "B"], [1, 0], "A"),
        ([1, 2, 3], [0, 1, 0], 2),
        ([1, 2, 3], [1, 0, 0], 1),
    ],
)
def test_discrete_distribution_fixed(population, weights, return_value):
    """Tests that do not require seed setting for deterministic results"""

    generator = Distribution()

    assert return_value == generator.discrete_distribution(population, weights)
