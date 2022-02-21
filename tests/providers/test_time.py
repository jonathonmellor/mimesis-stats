import datetime

import numpy as np
import pytest
from mimesis_stats.providers.time import TimeDistribution


@pytest.mark.parametrize(
    "input, format, return_value",
    [
        (datetime.datetime(1985, 10, 20), None, datetime.datetime(1985, 10, 20)),
        ("20/10/1985", "%d/%m/%Y", datetime.datetime(1985, 10, 20)),
    ],
)
def test_load_time(input, format, return_value):
    """Test conversion approach for datetime target"""

    generator = TimeDistribution()

    assert generator._load_time(input, format) == return_value


@pytest.mark.parametrize(
    "start, end, distribution, return_value",
    [
        (
            datetime.datetime(1985, 10, 20),
            datetime.datetime(1985, 10, 20),
            np.random.uniform,
            datetime.datetime(1985, 10, 20),
        ),
        (datetime.datetime(1985, 10, 20), datetime.datetime(1985, 10, 22), lambda: 0, datetime.datetime(1985, 10, 20)),
        (datetime.datetime(1985, 10, 20), datetime.datetime(1985, 10, 22), lambda: 1, datetime.datetime(1985, 10, 22)),
        (
            datetime.datetime(1985, 10, 20),
            datetime.datetime(1985, 10, 22),
            lambda: 0.5,
            datetime.datetime(1985, 10, 21),
        ),
    ],
)
def test_sample_time(start, end, distribution, return_value):
    """Test sampling of datetime"""

    generator = TimeDistribution()

    assert generator._sample_time(start, end, distribution) == return_value
