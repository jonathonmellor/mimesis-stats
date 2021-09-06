import pytest

from mimesis_stats.providers.distribution import Distribution


@pytest.mark.parametrize(
    "population, weights, return_value",
    [
        (["A", "B"], [0, 1], "B"),
        ([1, 2, 3], [1, 0, 0], 1),
    ],
)
def test_discrete_distribution_fixed(population, weights, return_value):
    """Test does not require seed setting for deterministic results"""

    generator = Distribution()

    assert return_value == generator.discrete_distribution(population, weights)


@pytest.fixture
def return_max_function(population):
    def _(population):
        return max(population)

    return _


@pytest.mark.parametrize(
    "population, return_value",
    [
        ([1, 2, 3], 3),
        (["a", "b", "c"], "c"),
    ],
)
def test_generic_distribution_fixed(population, return_value, return_max_function):
    """Test does not require seed setting for deterministic results"""

    generator = Distribution()

    assert return_value == generator.generic_distribution(func=return_max_function, population=population)
