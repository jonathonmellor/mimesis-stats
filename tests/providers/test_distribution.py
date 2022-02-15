import pytest
import sympy.stats as symstats
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

    assert generator.discrete_distribution(population, weights) == return_value


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

    assert generator.generic_distribution(func=return_max_function, population=population) == return_value


@pytest.mark.parametrize(
    "sides",
    [n for n in range(1, 6)],
)
def test_generic_expression_fixed(sides):
    """Test does not require seed setting for deterministic results"""

    expr = symstats.Die("X", sides)
    generator = Distribution()
    print(symstats.sample(expr))

    assert generator.generic_expression(expr=expr) in set(range(1, sides + 1))
