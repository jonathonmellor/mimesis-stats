from typing import Any
from typing import List
from typing import Tuple

import numpy as np
from mimesis.providers.base import BaseDataProvider


class BaseStatsDataProvider(BaseDataProvider):
    """
    Class for all mimesis_stats providers to inherit.

    Allows access to generic _replace() across all providers and
    consistent random seeding.


    Notes
    -----
    Sets global seed for numpy.
    """

    class Meta:
        name = "base_stats"

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

        np.random.seed(self.seed)

    @staticmethod
    def _replace(value: Any, proportion: float = 0.0, replacement: Any = None) -> Any:
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
            The null or otherwise value that will replace the input given
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

        if np.random.uniform(size=None) < proportion:
            return replacement
        else:
            return value

    def _replace_multiple(self, values: Tuple[Any], proportions: List[float], replacements: Any) -> Tuple[Any, ...]:
        """
        Adaptation of self._replace() for multiple values.

        Replace values with given probability.
        Normally used with a None replacement.

        Parameters
        ----------
        values
            Values that may be replaced with Null value
        proportion
            Probability of individual replacement with null for each element in values.
            Matches overall proportion null desired at large sample size
        replacement
            The null or otherwise value that will replace the input for the corresponding element given
            the probability.

        Returns
        -------
        Tuple[value or null for each value]

        Notes
        -----
        Defaults cause no replacements
        """
        if not proportions:
            return values

        if replacements is None:
            replacements = [None] * len(values)

        value_triplets = zip(values, proportions, replacements)
        return tuple(
            self._replace(element, proportion, replacement) for element, proportion, replacement in value_triplets
        )
