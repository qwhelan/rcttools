import os
from datetime import datetime
from decimal import Decimal
from typing import Dict

import numpy as np
import pandas as pd
from PIL import Image
from PIL.Image import Image as ImageType

from ..rct2gpx import (
    FLOAT_FRAME_TYPE,
    EmbeddedData,
    StateMachine,
    parsed_stacked_frames,
)


def load_example(file_name: str) -> ImageType:
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "parse_stacked_frames", file_name)
    return Image.open(file_path)


def test_parsed_stacked_frames() -> None:
    state_machine = StateMachine()
    dir = "v0_20230311_205904"
    stacked_frames: Dict[int, FLOAT_FRAME_TYPE] = {}
    for i, f in enumerate(["data_0.png", "data_6.png"]):
        img = load_example(f"{dir}/{f}")
        stacked_frames[i] = np.array(img).astype(float)
    selected_y = 0
    result, summary_stats = parsed_stacked_frames(
        state_machine, selected_y, stacked_frames
    )
    assert isinstance(result, dict)
    assert isinstance(summary_stats, pd.Series)

    assert result[0] == EmbeddedData(
        datetime=datetime(2023, 3, 11, 12, 59, 2),
        latitude=Decimal("47.64850"),
        longitude=Decimal("-122.16449"),
    )

    assert result[1] == EmbeddedData(
        datetime=datetime(2023, 3, 11, 12, 59, 3),
        latitude=Decimal("47.64858"),
        longitude=Decimal("-122.16449"),
    )
