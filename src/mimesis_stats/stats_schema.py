from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List

from mimesis.schema import Field
from mimesis_stats.providers.distribution import Distribution
from mimesis_stats.providers.multivariable import MultiVariable


class StatsField(Field):
    """ """

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)
        self._gen.add_providers(*[Distribution, MultiVariable])


class StatsSchema:
    """ """

    def __init__(self, schema: Callable = lambda: {}, *args: Any, **kwargs: Any) -> None:
        """
        Parameters
        ----------
        schema
            mimesis schema definition.
            lambda: {variable_name: field(provider_method, **kwargs)}
        """
        self.schema = schema

    def _unnest(self, generated_results: Dict, exclude: List[str] = []) -> Dict:
        """
        For multi-variable generation unest the defined sub-variables

        Unnests nested dicts if they are nested.
        """
        # make more performant, can nested-ness be checked?
        d = {}
        for k, v in generated_results.items():
            if isinstance(v, dict) and k not in exclude:
                d.update(v)
            elif k not in d:
                d[k] = v
            else:
                raise KeyError(f"{k} variable name already in variable dictionary")
        return d

    def create(self, iterations: int = 1, exclude_from_unnesting: List[str] = []) -> List[Any]:
        """
        Creates a list of a fulfilled schemas.

        """
        return [self._unnest(self.schema(), exclude=exclude_from_unnesting) for _ in range(iterations)]

    def iterator(self, iterations: int = 1, exclude_from_unnesting: List[str] = []) -> Iterator[Any]:
        """
        Fulfills schema in a lazy way.

        """

        if iterations < 1:
            raise ValueError("The number of iterations must be greater than 0.")

        for item in range(iterations):
            yield self._unnest(self.schema(), exclude=exclude_from_unnesting)
