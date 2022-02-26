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
    # consider testing **kwargs

    generator = TimeDistribution()

    assert generator._sample_time(start, end, distribution) == return_value


@pytest.mark.parametrize(
    "start, end, output_format, output_type, distribution, return_value",
    [
        (  # test datetime output
            datetime.datetime(1985, 10, 20),
            datetime.datetime(1985, 10, 20),
            None,
            datetime.datetime,
            np.random.uniform,
            datetime.datetime(1985, 10, 20),
        ),
        (  # test string output
            datetime.datetime(1985, 10, 20),
            datetime.datetime(1985, 10, 20),
            "%Y",
            str,
            np.random.uniform,
            "1985",
        ),
        (  # test date output
            datetime.datetime(1985, 10, 20),
            datetime.datetime(1985, 10, 20),
            None,
            datetime.date,
            np.random.uniform,
            datetime.date(1985, 10, 20),
        ),
        (  # test time output
            datetime.datetime(1985, 10, 20),
            datetime.datetime(1985, 10, 20),
            None,
            datetime.time,
            np.random.uniform,
            datetime.time(0),
        ),
    ],
)
def test_generate_time(start, end, output_format, output_type, distribution, return_value):
    """Test output formatting"""
    # other parts of method are all tested in this file

    generator = TimeDistribution()

    assert (
        generator.generate_time(
            start, end, output_format=output_format, output_type=output_type, distribution=distribution
        )
        == return_value
    )
