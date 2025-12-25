from typing import Literal, Tuple

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
