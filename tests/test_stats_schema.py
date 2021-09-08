import pytest

from mimesis_stats.stats_schema import StatsSchema

# from mimesis_stats.stats_schema import GenerationVariable


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
def test_unnest(dummy_field, dummy_blueprint, input, exclude, expected_result):

    s_schema = StatsSchema(field=dummy_field, blueprint=dummy_blueprint)

    assert s_schema._unnest(input, exclude=exclude) == expected_result
