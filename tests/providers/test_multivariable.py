from mimesis_stats.providers.multivariable import MultiVariable


def test_dependent_variables():

    names = ["response", "count"]
    combinations = [("Yes", 123), ("No", None)]
    weights = [0, 1]

    provider = MultiVariable()

    expected_result = {"response": "No", "count": None}
    result = provider.dependent_variables(names, combinations, weights=weights)

    assert result == expected_result

    expected_result = {"response": "Yes", "count": 123}
    result = provider.dependent_variables(names, combinations, weights=list(reversed(weights)))

    assert result == expected_result
