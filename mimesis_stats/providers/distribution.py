"""Provides a random choice from a given distribution"""
import random
from typing import Any
from typing import Callable
from typing import List

import numpy as np
from mimesis.providers.base import BaseDataProvider


class Distribution(BaseDataProvider):
    """
    Class for generating data from a distribution as a mimesis provider.

    All methods replace values with None by given probability.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

    def _replace(self, value: Any, proportion: float, replacement: Any = None) -> Any:
        """
        Replace value with given probability.
        Normally used with a None replacement.
        """
        if not proportion:
            return value

        if random.random() < proportion:
            return replacement
        else:
            return value

    def generic_dist(self, func: Callable, null_prop: float = 0, null_value: Any = None, **kwargs: Any) -> Any:
        """
        Draw from any distribution passed by a function.
        Replace a proportion with None values.
        """
        return self._replace(func(**kwargs), null_prop, replacement=null_value)

    def discrete_dist(
        self, population: List[Any], weights: List[float], null_prop: float = 0, null_value: Any = None
    ) -> Any:
        """
        Draw from discrete fix-proportion distribution.
        Replace a proportion with null_value.
        """
        return self._replace(np.random.choice(population, size=None, p=weights), null_prop, replacement=null_value)
