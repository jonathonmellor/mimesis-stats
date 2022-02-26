"""Provides a random choice from a datetime type"""
import datetime
from typing import Any
from typing import Callable
from typing import Union

import numpy as np
from mimesis_stats.providers.distribution import Distribution


class TimeDistribution(Distribution):
    """ """

    class Meta:
        name = "time"

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)

    def _load_time(self, dt: Union[str, datetime.datetime], frmt=None) -> datetime.datetime:

        if isinstance(dt, str):
            dt = datetime.datetime.strptime(dt, frmt)
        if not isinstance(dt, datetime.datetime):
            raise TypeError(f"dt must convert to a datetime type, it is {type(dt)}")

        return dt

    def _sample_time(
        self, start: datetime.datetime, end: datetime.datetime, distribution: Callable, **kwargs: Any
    ) -> datetime.datetime:
        """
        Sample a datetime based on a range and distribution
        Distribution must be normalised (bound by [0, 1])
        """
        proportion = distribution(**kwargs)

        assert 0 <= proportion <= 1, "distribution must be a probability density function bound by [0, 1]"

        rtime = start + proportion * (end - start)

        return rtime

    def generate_time(
        self,
        start,
        end,
        input_format=None,
        output_format=None,
        output_type=datetime.datetime,
        distribution: Callable = np.random.uniform,
        **kwargs,
    ) -> Union[datetime.datetime, datetime.date, datetime.time, str]:

        sdatetime = self._load_time(start, input_format)
        edatetime = self._load_time(end, input_format)

        pdatetime = self._sample_time(start=sdatetime, end=edatetime, distribution=distribution, **kwargs)

        if output_type == datetime.datetime:
            return pdatetime
        if output_type == str:
            return pdatetime.strftime(output_format)
        if output_type == datetime.date:
            return pdatetime.date()
        if output_type == datetime.time:
            return pdatetime.time()
        else:
            raise TypeError(f"Issue with output_type as: {output_type}")
