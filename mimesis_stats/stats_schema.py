from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional

from dataclasses import dataclass
from dataclasses import field
from mimesis.schema import Field


@dataclass
class GenerationVariable:
    name: str
    provider_method: str
    kwargs: Optional[Dict] = field(default_factory=lambda: {})


class StatsSchema:
    def __init__(self, field: Field, blueprint: List[GenerationVariable], *args: Any, **kwargs: Any) -> None:
        """
        Parameters
        ----------
        field
            mimesis field containing providers, seed and locale
        blueprint
            List of GenerationVariables defining the data to be created
        """
        self.field = field
        self.blueprint = blueprint
        self.schema = self._create_schema()

    def _create_schema(self) -> Callable:
        """
        Converts a blueprint object into a mimesis schema
        """
        return lambda: {
            variable.name: self.field(variable.provider_method, **variable.kwargs) for variable in self.blueprint
        }

    def _unnest(self, generated_results: Dict) -> Dict:
        """
        For multi-variable generation unest the defined sub-variables

        Unnests nested dicts if they are nested.
        """
        # make more performant, can nested-ness be checked?
        d = {}
        for k, v in generated_results.items():
            if isinstance(v, dict):
                d.update(v)
            else:
                d[k] = v
        return d

    def create(self, iterations: int = 1) -> List[Any]:
        """
        Creates a list of a fulfilled schemas.

        """
        return [self._unnest(self.schema()) for _ in range(iterations)]

    def iterator(self, iterations: int = 1) -> Iterator[Any]:
        """
        Fulfills schema in a lazy way.

        """

        if iterations < 1:
            raise ValueError("The number of iterations must be greater than 0.")

        for item in range(iterations):
            yield self._unnest(self.schema())
