"""Provides a random choice from a datetime type"""
import datetime
from typing import Any
from typing import Callable
from typing import Union

import numpy as np
from mimesis_stats.providers.distribution import Distribution


class TimeDistribution(Distribution):
    """
    Class for univariable time based distribution sampling.

    Methods
    -------
    generate_time
        Sample time in range from a defined distribution.
    """

    class Meta:
        name = "time"

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

    def _load_time(self, dt: Union[str, datetime.datetime], frmt=None) -> datetime.datetime:
        """
        Method to convert input to a datetime object.
        """
        if isinstance(dt, str):
            dt = datetime.datetime.strptime(dt, frmt)
        if not isinstance(dt, datetime.datetime):
            raise TypeError(f"dt must convert to a datetime type, it is {type(dt)}")

        return dt

    def _sample_time(
        self, start: datetime.datetime, end: datetime.datetime, distribution: Callable, **kwargs: Any
    ) -> datetime.datetime:
        """
        Method to sample a datetime based on a range and distribution.
        The distribution samples a pdf creating a proportion between the stard and end ranges.
        Distribution must be normalised (bound by [0, 1]).
        """
        proportion = distribution(**kwargs)

        assert 0 <= proportion <= 1, "distribution must be a probability density function bound by [0, 1]"

        rtime = start + proportion * (end - start)

        return rtime

    def generate_time(
        self,
        start: Union[str, datetime.datetime],
        end: Union[str, datetime.datetime],
        input_format: str = None,
        output_format: str = None,
        output_type: Union[datetime.datetime, datetime.date, datetime.time, str] = datetime.datetime,  # type: ignore
        distribution: Callable = np.random.uniform,
        null_prop: float = 0,
        null_value: Any = None,
        **kwargs,
    ) -> Union[datetime.datetime, datetime.date, datetime.time, str]:
        """
        Draw from a datetime range defined by a start and end period and probability distribution.

        Parameters
        ----------
        start
            Earliest time point to sample above of (inclusive).
        end
            Final time point to sample below from (inclusive).
        input_format
            For string start, end types what format to parse to datetime.
        output_format
            For string sample outputs types what format to provide output.
            Can be used to control granularity.
        output_type
            Which data type to output the sampled value as.
            Can be used to control granularity.
        distribution
            Function defining the distribution of dates, must be bound by [0, 1].
        null_prop
            Proportion of values to replace as null
        null_value
            The (null) value to replace a sample with
        **kwargs
            Keyword arguments needed for func distribution

        Returns
        -------
        Single date time formatted value within defined range

        Examples
        --------
        >>>TimeDistribution.generate_time(
            start=datetime.datetime(1985, 10, 20),
            end=datetime.datetime(1985, 10, 25),
            output_type=datetime.date,
            distribution=np.random.uniform
        )
        datetime.date(1985, 10, 23)
        """
        # convert to datetime
        sdatetime = self._load_time(start, input_format)
        edatetime = self._load_time(end, input_format)

        # sample value
        pdatetime = self._sample_time(start=sdatetime, end=edatetime, distribution=distribution, **kwargs)

        # add missingness
        pdatetime = self._replace(pdatetime, null_prop, null_value)

        # convert to desired output
        if output_type == datetime.datetime:
            return pdatetime
        if output_type == str:
            return pdatetime.strftime(output_format)  # type: ignore
        if output_type == datetime.date:
            return pdatetime.date()
        if output_type == datetime.time:
            return pdatetime.time()
        else:
            raise TypeError(f"Issue with output_type as: {output_type}")
