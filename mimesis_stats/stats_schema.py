from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional

from mimesis.schema import Field


class GenerationVariable:
    """
    Class defining a variable to be passed into the schema.

    Notes
    -----
    lambda used for lazy evaluation and passing to StatsSchema
    """

    class WrappedVariable:
        def __init__(self, name: str, provider_method: str, **kwargs: Any) -> None:
            self.name = name
            self.provider_method = provider_method
            self.kwargs = kwargs

    def __init__(self, name: str, provider_method: str, **kwargs: Any) -> None:
        self.stored = lambda: self.WrappedVariable(name=name, provider_method=provider_method, **kwargs)


class StatsSchema:
    def __init__(
        self,
        field: Field,
        blueprint: Optional[List[GenerationVariable]] = [],
        standard_schema: Optional[Callable] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Parameters
        ----------
        field
            mimesis field containing providers, seed and locale
        blueprint
            List of GenerationVariables defining the data to be created
        standard_schema
            mimesis original schema approach
        """
        if standard_schema is not None:
            self.schema = standard_schema
        else:
            self.field = field
            if blueprint is None:
                raise ValueError("blueprint given is None")
            self.blueprint = blueprint
            self.schema = self._create_schema()

    def _create_schema(self) -> Callable:
        """
        Converts a blueprint object into a mimesis schema
        """
        if self.blueprint is None or self.blueprint == []:
            raise ValueError("blueprint given is None")
        return lambda: {
            variable.stored().name: self.field(variable.stored().provider_method, **variable.stored().kwargs)
            for variable in self.blueprint
        }

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
            else:
                d[k] = v
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
