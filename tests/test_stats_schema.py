import pytest

from mimesis_stats.stats_schema import GenerationVariable
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
def test_unnest(dummy_field, dummy_blueprint, input, exclude, expected_result):

    s_schema = StatsSchema(field=dummy_field, blueprint=dummy_blueprint)

    assert s_schema._unnest(input, exclude=exclude) == expected_result


@pytest.mark.parametrize(
    "blueprint, iterations, expected_result",
    [
        ([GenerationVariable(name="dummy_number", provider_method="dummy.one")], 1, [{"dummy_number": 1}]),
        (
            [GenerationVariable(name="dummy_number", provider_method="dummy.one")],
            2,
            [{"dummy_number": 1}, {"dummy_number": 1}],
        ),
        ([GenerationVariable(name="dummy_dict", provider_method="dummy.dictionary")], 1, [{"collins": "defines"}]),
        (
            [
                GenerationVariable(name="dummy_number", provider_method="dummy.one"),
                GenerationVariable(name="dummy_string", provider_method="dummy.characters"),
            ],
            1,
            [{"dummy_number": 1, "dummy_string": "ABC"}],
        ),
    ],
)
def test_stats_schema_create(dummy_field, blueprint, iterations, expected_result):

    s_schema = StatsSchema(field=dummy_field, blueprint=blueprint)

    result = s_schema.create(iterations=iterations)

    assert result == expected_result


def test_nested_generation(dummy_field):
    blueprint = [GenerationVariable(name="nest", provider_method="choice", items=["hard", dummy_field("dummy.one")])]
    s_schema = StatsSchema(field=dummy_field, blueprint=blueprint)

    # not technically deterministic
    n = 10000
    # p FN = (0.5)^n, n~10,000, p~0, beyond floating point recording discrepency
    result = s_schema.create(iterations=n)

    values = [variable["nest"] for variable in result]

    assert set(values) == set([1, "hard"])


def test_standard_schema(dummy_field):

    schema = lambda: {"basic": dummy_field("dummy.one")}  # noqa: E731
    s_schema = StatsSchema(field=dummy_field, standard_schema=schema)

    assert s_schema.create(iterations=1) == [{"basic": 1}]
