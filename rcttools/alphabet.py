import os
from typing import Dict, Tuple

import numpy as np
from PIL import Image

from .common import FLOAT_FRAME_TYPE, FLOAT_VIDEO_TYPE, VIDEO_LENGTH

BASE_PATH = os.path.dirname(__file__)


class Character:
    def __init__(self, char: str) -> None:
        self.path = os.path.join(BASE_PATH, "data", f"{char}.png")
        self.array = np.array(Image.open(self.path))
        self.mask = (1 - 1.0 * self.array / 255) > 0.5
        self.mask_4d = self.mask[np.newaxis, :]

    def score_frame(self, frame: FLOAT_FRAME_TYPE) -> float:
        union_mask: np.ndarray[Tuple[int], np.dtype[np.bool_]] = np.logical_or(
            self.mask, frame
        )
        return 1.0 * int(frame[self.mask].sum()) / int(union_mask.sum())

    def score_video(
        self, frame: FLOAT_VIDEO_TYPE
    ) -> np.ndarray[Tuple[VIDEO_LENGTH], np.dtype[np.float32]]:
        mask_4d = np.tile(self.mask_4d, (frame.shape[0], 1, 1, 1))
        union_mask = np.logical_or(mask_4d, frame)
        return (  # type: ignore[no-any-return]
            1.0 * (frame * mask_4d).sum(axis=(1, 2, 3)) / union_mask.sum(axis=(1, 2, 3))
        )


class FixedScore(Character):
    def __init__(self, score: float) -> None:
        self.score = score

    def score_frame(self, frame: FLOAT_FRAME_TYPE) -> float:
        return self.score

    def score_video(
        self, frame: FLOAT_VIDEO_TYPE
    ) -> np.ndarray[Tuple[VIDEO_LENGTH], np.dtype[np.float32]]:
        return np.full(frame.shape[0], self.score, dtype=np.float32)


NUMBERS = {str(x): Character(str(x)) for x in range(10)}

_number_shapes = {k: v.array.shape for k, v in NUMBERS.items()}
if len(set(_number_shapes.values())) > 1:
    formatted_output = "\n".join(f"{k} = {v}" for k, v in _number_shapes.items())
    raise ValueError(
        f"Numerical characters are not a consistent shape:\n{formatted_output}"
    )

NUMBERS_SHAPE = list(set(_number_shapes.values()))[0]

NEGATIVE = Character("-")
NEGATIVE_OR_NUMBER: Dict[str, Character] = {
    **NUMBERS,
    "-": NEGATIVE,
    " ": FixedScore(0.8),
}
NEGATIVE_OR_NOTHING: Dict[str, Character] = {
    "-": NEGATIVE,
    "": FixedScore(0.8),
}
