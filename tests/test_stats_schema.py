import pandas as pd
import pytest
from scipy.stats import truncnorm

from mimesis_stats.stats_schema import StatsField
from mimesis_stats.stats_schema import StatsSchema


@pytest.mark.parametrize(
    "input, exclude, expected_result",
    [
        ({"level0": "example1"}, [], {"level0": "example1"}),
        (
            {"level0.0": "example1", "level0.1": {"level1.0": 1, "level1.1": 2}},
            [],
            {"level0.0": "example1", "level1.0": 1, "level1.1": 2},
        ),
        (
            {"level0.0": "example1", "level0.1": {"level1.0": 1, "level1.1": 2}},
            ["level0.1"],
            {"level0.0": "example1", "level0.1": {"level1.0": 1, "level1.1": 2}},
        ),
    ],
)
def test_unnest(input, exclude, expected_result):

    s_schema = StatsSchema()

    assert s_schema._unnest(input, exclude=exclude) == expected_result


@pytest.mark.parametrize(
    "inputs, iterations, expected_result",
    [
        ({"v1": {"name": "dummy_number", "provider_method": "dummy.one"}}, 1, [{"dummy_number": 1}]),
        (
            {"v1": {"name": "dummy_number", "provider_method": "dummy.one"}},
            2,
            [{"dummy_number": 1}, {"dummy_number": 1}],
        ),
        ({"v1": {"name": "dummy_dict", "provider_method": "dummy.dictionary"}}, 1, [{"collins": "defines"}]),
        (
            {
                "v1": {"name": "dummy_number", "provider_method": "dummy.one"},
                "v2": {"name": "dummy_string", "provider_method": "dummy.characters"},
            },
            1,
            [{"dummy_number": 1, "dummy_string": "ABC"}],
        ),
    ],
)
def test_stats_schema_create(dummy_field, inputs, iterations, expected_result):

    schema = lambda: {  # noqa: E731
        variable["name"]: dummy_field(variable["provider_method"]) for variable in inputs.values()
    }
    s_schema = StatsSchema(schema=schema)

    result = s_schema.create(iterations=iterations)

    assert result == expected_result


def test_nested_generation(dummy_field):
    schema = lambda: {"nest": dummy_field("choice", items=["hard", dummy_field("dummy.one")])}  # noqa: E731

    s_schema = StatsSchema(schema=schema)

    # not technically deterministic
    n = 10000
    # p FN = (0.5)^n, n~10,000, p~0, beyond floating point recording discrepency
    result = s_schema.create(iterations=n)

    values = [variable["nest"] for variable in result]

    assert set(values) == set([1, "hard"])


def test_nested_generation_deterministic(dummy_field):

    schema = lambda: {  # noqa: E731
        "nest": dummy_field("choice", items=["hard", dummy_field("choice", items=["A", "B"])])
    }

    s_schema = StatsSchema(schema=schema)

    # not technically deterministic
    n = 10000
    # p FN = (0.5)^n, n~10,000, p~0, beyond floating point recording discrepency
    result = s_schema.create(iterations=n)

    values = [variable["nest"] for variable in result]

    assert set(values) == set(["A", "B", "hard"])


def test_pandas_survey_regression(data_regression):
    """Uses example from README"""

    # Define parameters of truncated normal
    lower = 0
    upper = 10
    mu_true = 7
    mu_false = 4
    sigma = 2.5

    field = StatsField(seed=42)

    # fmt: off
    schema_blueprint = lambda: { # noqa E731
        "ID": field("random.custom_code", mask='SCHL#####', digit="#"),
        "email": field("person.email"),
        "occupation": field("person.occupation"),
        "parent_school_importance": field(
            "dependent_variables",
            variable_names=["parent", "school_importance"],
            options=[
                (True, round(truncnorm.rvs(a=(lower-mu_true)/sigma, b=(upper-mu_true)/sigma,
                                        loc=mu_true, scale=sigma))), # noqa E731
                (False, round(truncnorm.rvs(a=(lower-mu_false)/sigma, b=(upper-mu_false)/sigma,
                                        loc=mu_false, scale=sigma))) # noqa E731
            ],
            weights=[0.3, 0.7],
        )
    }
    # fmt: on
    schema = StatsSchema(schema_blueprint)
    result_df = pd.DataFrame(schema.create(iterations=50)).to_dict()

    data_regression.check(result_df)
