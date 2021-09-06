import random
from typing import Any

import numpy as np
from mimesis.providers.base import BaseDataProvider


class BaseStatsDataProvider(BaseDataProvider):
    """ """

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
