"""Provides dependent variables"""
from typing import Any
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
from mimesis_stats.providers.base_stats import BaseStatsDataProvider


class MultiVariable(BaseStatsDataProvider):
    """
    Class for producing multiple variables that are related to one another.

    Returns a dictionary of name: value pairs, for later unpacking.
    """

    class Meta:
        name = "multi_variable"

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

    def dependent_variables(
        self,
        variable_names: List[str],
        options: List[Tuple[Any]],
        weights: List[float],
        null_props: Union[List[float], int] = 0,
        null_values: List[Any] = None,
    ) -> dict:
        """
        Make a discrete sample from possible variable combinations.
        The elements within `options` can be provider methods themselves.

        Parameters
        ----------
        variable_names
            Name of each variable corresponding element-wise to each option.
            Becomes the keys in returned dictionary.
        options
            Possible combinations of variable values.
        weights
            Weighting of probability for each combination of variables.
        null_props
            Proportion of each element to be nulled
        null_value
            Value to replace if value nulled

        Notes
        -----
        Combinations can contain null values, for a more strictly missing value regime
        Combination elements can be other mimesis-like provider methods.

        Examples
        --------
        # Example survey with two questions:
        # "Do you consent" + "How many biscuits did you eat?"
        >>>names = ["response", "count"]
        >>>combinations = [("Yes", "Sometimes"), ("No", None)]
        >>>MultiVariable.dependent_variables(names, combinations, weights=[0, 1])
        {"response": "No", "count": None}

        >>>MultiVariable.dependent_variables(names, combinations, weights=[1, 0])
        {"response": "Yes", "count": "Sometimes"}
        """
        random_index = np.random.choice(len(options), p=weights, size=None, replace=False)

        selection = options[random_index]

        selection_nulled = self._replace_multiple(selection, null_props, null_values)

        return dict(zip(variable_names, selection_nulled))
