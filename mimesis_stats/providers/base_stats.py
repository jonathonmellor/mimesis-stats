from typing import Any

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

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

        if np.random.uniform(size=None) < proportion:
            return replacement
        else:
            return value
