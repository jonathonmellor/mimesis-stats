"""Provides a random choice from a given distribution"""
from typing import Any
from typing import Callable
from typing import List

import numpy as np

from mimesis_stats.providers.base_stats import BaseStatsDataProvider


class Distribution(BaseStatsDataProvider):
    """ """

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

    def generic_distribution(self, func: Callable, null_prop: float = 0, null_value: Any = None, **kwargs: Any) -> Any:
        """
        Draw from any distribution passed by a function.
        Replace a proportion with None values.

        Parameters
        ----------
        func
            Function defining the distribution
            Expected to return a single value
        null_prop
            Proportion of values to replace as null
        null_value
            The (null) value to replace a sample with
        **kwargs
            Keyword arguments needed for func distribution

        Returns
        -------
        Single value from func call with kwargs

        Examples
        --------
        >>>Distribution.generic_distribution(func=np.random.normal, loc=1, null_prop=0.0)
        1.06

        >>>Distribution.generic_distribution(func=stats.bernoulli.rvs, p=0.3, loc=2)
        2
        """
        return self._replace(func(**kwargs), null_prop, replacement=null_value)

    def discrete_distribution(
        self, population: List[Any], weights: List[float], null_prop: float = 0, null_value: Any = None
    ) -> Any:
        """
        Draw from discrete fix-proportion distribution.
        Replace a proportion with null_value.

        Parameters
        ----------
        population
            The values to sample from
        weights
            Probabilities to weight the sampling, index matched with population
        null_prop
            Proportion of values to replace as null
        null_value
            The (null) value to replace a sample with

        Returns
        -------
        Single element from population or null_value

        Examples
        --------
        >>>Distribution.distrete_distribution(population=["one", "two", "three"], weights=[0.01, 0.01, 0.98])
        "three"
        """
        return self._replace(np.random.choice(population, size=None, p=weights), null_prop, replacement=null_value)
