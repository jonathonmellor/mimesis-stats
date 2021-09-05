"""Provides a random choice from a given distribution"""
import random
from typing import Any
from typing import Callable
from typing import List

import numpy as np
from mimesis.providers.base import BaseDataProvider


class Distribution(BaseDataProvider):
    """
    Mimesis provider for generating data from non-uniform and uniform distributions.

    All methods replace values with None by given probability.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        random.seed(self.seed)
        np.random.seed(self.seed)

    def _replace(self, value: Any, proportion: float = 0.0, replacement: Any = None) -> Any:
        """
        Replace value with given probability.
        Normally used with a None replacement.

        Parameters
        ----------
        value
            Value that may be replaced with Null value
        proportion
            Probability of individual replacement with null
            Matches overall proportion null desired at large sample size
        replacement
            The null or otherwise value that with replace the input given
            the probability.

        Returns
        -------
        value or null

        Notes
        -----
        Defaults cause no replacement
        """
        if not proportion:
            return value

        if random.random() < proportion:
            return replacement
        else:
            return value

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
            Key word arguments needed for func distribution

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
        """
        return self._replace(np.random.choice(population, size=None, p=weights), null_prop, replacement=null_value)
