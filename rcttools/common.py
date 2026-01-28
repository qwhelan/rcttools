from decimal import Decimal
from math import atan2, cos, degrees, radians, sin
from typing import Literal, Optional, Tuple

import numpy as np

FRAME_HEIGHT = Literal[40]
FRAME_WIDTH = Literal[1150]
FRAME_CHANNELS = Literal[3]
# Typically 902 frames for 30s clips, but can be shorter
VIDEO_LENGTH = int

FRAME_TYPE = np.ndarray[
    Tuple[FRAME_HEIGHT, FRAME_WIDTH, FRAME_CHANNELS], np.dtype[np.uint8]
]
FLOAT_FRAME_TYPE = np.ndarray[
    Tuple[FRAME_HEIGHT, FRAME_WIDTH, FRAME_CHANNELS], np.dtype[np.float32]
]
VIDEO_TYPE = np.ndarray[
    Tuple[VIDEO_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, FRAME_CHANNELS], np.dtype[np.uint8]
]
FLOAT_VIDEO_TYPE = np.ndarray[
    Tuple[VIDEO_LENGTH, FRAME_HEIGHT, FRAME_WIDTH, FRAME_CHANNELS], np.dtype[np.float64]
]

CHAR_WIDTHS = {str(x): 19 for x in range(10)}
CHAR_WIDTHS["/"] = 14
CHAR_WIDTHS[" "] = 8
CHAR_WIDTHS[":"] = 14
CHAR_WIDTHS["."] = 14
CHAR_WIDTHS["-"] = 14
CHAR_WIDTHS[""] = 0

DECIMAL_ONE = Decimal(1)
DECIMAL_SIXTY = Decimal(60)
DECIMAL_SIXTY_SQUARED = Decimal(3600)
DECIMAL_SECOND_PRECISION = Decimal("0.000001")


def dec_to_dms(gps_decimal: Decimal) -> Tuple[Decimal, Decimal, Decimal]:
    whole = gps_decimal.copy_abs() // DECIMAL_ONE
    fraction = gps_decimal.copy_abs() % DECIMAL_ONE
    minutes = (fraction * DECIMAL_SIXTY) // DECIMAL_ONE
    fraction -= minutes / DECIMAL_SIXTY
    seconds = fraction * DECIMAL_SIXTY_SQUARED

    return whole, minutes, seconds.quantize(DECIMAL_SECOND_PRECISION)


def calc_bearing(
    lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal
) -> Optional[Decimal]:
    """Calculate the bearing from point 1 to point 2.

    All inputs and outputs are in decimal degrees.
    """
    if lat1 == lat2 and lon1 == lon2:
        return None

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lon_rad = radians(lon2 - lon1)

    x = sin(delta_lon_rad) * cos(lat2_rad)
    y = cos(lat1_rad) * sin(lat2_rad) - (
        sin(lat1_rad) * cos(lat2_rad) * cos(delta_lon_rad)
    )

    initial_bearing = atan2(x, y)
    initial_bearing_deg = degrees(initial_bearing)
    compass_bearing = (initial_bearing_deg + 360) % 360

    return Decimal(compass_bearing).quantize(DECIMAL_SECOND_PRECISION)
