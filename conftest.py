from typing import Any

import pytest
from mimesis.schema import Field

from mimesis_stats.providers.base_stats import BaseStatsDataProvider
from mimesis_stats.stats_schema import GenerationVariable


@pytest.fixture
def common_seed():
    return 42


@pytest.fixture
def dummy_field(dummy_provider):
    return Field(seed=42, providers=[dummy_provider])


@pytest.fixture
def dummy_blueprint():

    bp = [
        GenerationVariable(name="dummy_number", provider_method="dummy.one"),
        GenerationVariable(name="dummy_string", provider_method="dummy.characters"),
        GenerationVariable(name="dummy_dict", provider_method="dummy.dictionary"),
    ]

    return bp


@pytest.fixture
def dummy_provider():
    class DummyProvider(BaseStatsDataProvider):
        """
        Basic provider used for testing

        Methods
        -------
        one
            returns 1
        characters
            returns "ABC"
        dictionary
            returns {"collins": "defines"}
        """

        class Meta:
            name = "dummy"

        def __init__(self, *args: Any, **kwargs: Any) -> None:

            super().__init__(*args, **kwargs)

        @staticmethod
        def one():
            return 1

        @staticmethod
        def characters():
            return "ABC"

        @staticmethod
        def dictionary():
            return {"collins": "defines"}

    return DummyProvider
