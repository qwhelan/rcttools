import datetime as dt
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, TypedDict

from .alphabet import NEGATIVE_OR_NOTHING, NEGATIVE_OR_NUMBER, NUMBERS, Character
from .common import CHAR_WIDTHS


class EmbeddedData(TypedDict):
    datetime: dt.datetime
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]


class ValueStateMachine:
    def __init__(self) -> None:
        self.chars: List[str] = []
        self.alphabet_by_position: List[str] = []
        self.position = 0
        self.offset = 0
        self.offset_history: List[int] = []
        self.force_numbers = False

    def reset(self) -> None:
        self.chars = []
        self.position = 0
        self.offset = 0
        self.offset_history = []
        self.force_numbers = False

    def __repr__(self) -> str:
        return f"<{type(self).__name__} chars={self.chars} position={self.position} offset={self.offset}>"

    def __str__(self) -> str:
        return "".join(self.chars)

    def append(self, char: str, offset: int) -> None:
        if char.isdigit() or char == "-":
            self.force_numbers = True
        self.chars.append(char)
        self.position += 1
        if self.position > len(self.alphabet_by_position):
            raise ValueError(f"Unexpected character: {char} {type(self)}")
        self.offset += offset
        if char in NUMBERS:
            self.offset_history.append(self.offset)
        if CHAR_WIDTHS[char] > 0:
            self.offset += CHAR_WIDTHS[char] + 2

    def is_complete(self) -> bool:
        return self.position >= len(self.alphabet_by_position)

    def get_alphabet(self) -> Dict[str, Character]:
        while True:
            if self.position >= len(self.alphabet_by_position):
                return {}
            alphabet = self.alphabet_by_position[self.position]
            if alphabet == "NUMBER":
                return NUMBERS
            elif alphabet == "NEGATIVE_OR_NUMBER":
                if self.force_numbers:
                    return NUMBERS
                return NEGATIVE_OR_NUMBER
            elif alphabet == "NEGATIVE_OR_NOTHING":
                return NEGATIVE_OR_NOTHING
            elif alphabet == "PERIOD":
                self.append(".", 0)
            elif alphabet == "SLASH":
                self.append("/", 0)
            elif alphabet == "COLON":
                self.append(":", 0)
            elif alphabet == "SPACE":
                self.append(" ", 0)
            else:
                raise Exception("Unexpected alphabet")


class DateTime(ValueStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.alphabet_by_position = [
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "SLASH",
            "NUMBER",
            "NUMBER",
            "SLASH",
            "NUMBER",
            "NUMBER",
            "SPACE",
            "NUMBER",
            "NUMBER",
            "COLON",
            "NUMBER",
            "NUMBER",
            "COLON",
            "NUMBER",
            "NUMBER",
            "SPACE",
        ]

    def result(self) -> dt.datetime:
        assert self.is_complete()
        return dt.datetime.strptime(str(self), "%Y/%m/%d %H:%M:%S ")


class Coordinate(ValueStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.alphabet_by_position = [
            "NEGATIVE_OR_NOTHING",
            "NEGATIVE_OR_NUMBER",
            "NEGATIVE_OR_NUMBER",
            "NEGATIVE_OR_NUMBER",
            "PERIOD",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "NUMBER",
            "SPACE",
        ]

    def result(self) -> Decimal:
        assert self.is_complete()
        return Decimal(str(self).strip())


class StateMachine:
    def __init__(self, use_parity: bool = False) -> None:
        self.objects: Tuple[DateTime, Coordinate, Coordinate] = (
            DateTime(),
            Coordinate(),
            Coordinate(),
        )
        self.current_object = 0
        self.use_parity = use_parity
        self.parity_bit = 1
        self.cumulative_offset = 0

    def get_alphabet(self) -> dict[str, Character]:
        return self.objects[self.current_object].get_alphabet()

    def get_next_offset(self) -> int:
        if self.use_parity:
            offset = self.parity_bit
        else:
            offset = 0

        result = 214 + self.cumulative_offset + self.objects[self.current_object].offset
        return result + offset

    def append(self, char: str) -> None:
        if char.isdigit() and self.use_parity:
            offset = self.parity_bit
            self.parity_bit *= -1
        else:
            offset = 0
        self.objects[self.current_object].append(char, offset)
        self.is_complete()

    def is_complete(self) -> bool:
        if (
            self.current_object < len(self.objects)
            and self.objects[self.current_object].is_complete()
        ):
            self.cumulative_offset += self.objects[self.current_object].offset
            self.current_object += 1
        if self.current_object >= len(self.objects):
            return True
        return False

    def reset(self) -> None:
        self.current_object = 0
        self.cumulative_offset = 0
        self.parity_bit = 1
        for obj in self.objects:
            obj.reset()

    def result(self) -> EmbeddedData:
        assert self.is_complete()
        return EmbeddedData(
            datetime=self.objects[0].result(),
            latitude=self.objects[1].result(),
            longitude=self.objects[2].result(),
        )
