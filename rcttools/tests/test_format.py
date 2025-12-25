from ..alphabet import NEGATIVE_OR_NOTHING, NEGATIVE_OR_NUMBER, NUMBERS
from ..text_format import Coordinate, DateTime, StateMachine


def test_datetime_format() -> None:
    state_machine = DateTime()
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 21
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("0", 0)
    assert state_machine.offset == 42
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 63
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("5", 0)
    assert state_machine.offset == 84
    assert state_machine.get_alphabet() == NUMBERS
    assert state_machine.offset == 100
    state_machine.append("0", 0)
    assert state_machine.offset == 121
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("6", 0)
    assert state_machine.offset == 142
    assert state_machine.get_alphabet() == NUMBERS
    assert state_machine.offset == 158
    state_machine.append("0", 0)
    assert state_machine.offset == 179
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("1", 0)
    assert state_machine.offset == 200
    assert state_machine.get_alphabet() == NUMBERS
    assert state_machine.offset == 210
    state_machine.append("1", 0)
    assert state_machine.offset == 231
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("3", 0)
    assert state_machine.offset == 252
    assert state_machine.get_alphabet() == NUMBERS
    assert state_machine.offset == 268
    state_machine.append("4", 0)
    assert state_machine.offset == 289
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("5", 0)
    assert state_machine.offset == 310
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("4", 0)
    assert state_machine.offset == 347
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("9", 0)
    assert state_machine.offset == 368
    assert state_machine.get_alphabet() == {}
    assert state_machine.is_complete()
    assert state_machine.offset == 378

    assert [x + 214 for x in state_machine.offset_history] == [
        214,
        235,
        256,
        277,  # year
        314,
        335,  # month
        372,
        393,  # day
        424,
        445,  # hour
        482,
        503,  # minute
        540,
        561,  # second
    ]
    assert "".join(state_machine.chars) == "2025/06/01 13:45:49 "


def test_coordinate1() -> None:
    """
    Test parsing of 47.62221
    """
    state_machine = Coordinate()
    assert state_machine.get_alphabet() == NEGATIVE_OR_NOTHING
    state_machine.append("", 0)
    assert state_machine.offset == 0
    state_machine.append(" ", 0)
    assert state_machine.offset == 10
    assert state_machine.get_alphabet() == NEGATIVE_OR_NUMBER
    state_machine.append("4", 0)
    assert state_machine.offset == 31
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("7", 0)
    assert state_machine.offset == 52
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("6", 0)
    assert state_machine.offset == 89
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 110
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 131
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 152
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("1", 0)
    assert state_machine.offset == 173
    assert state_machine.get_alphabet() == {}
    assert state_machine.is_complete()
    assert state_machine.offset == 183

    assert [x + 214 + 378 for x in state_machine.offset_history] == [
        602,
        623,  # lat int
        660,
        681,
        702,
        723,
        744,  # lat fraction
    ]


def test_coordinate2() -> None:
    """
    Test parsing of -122.17650
    """
    state_machine = Coordinate()
    assert state_machine.get_alphabet() == NEGATIVE_OR_NOTHING
    state_machine.append("-", 0)
    assert state_machine.offset == 16
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("1", 0)
    assert state_machine.offset == 37
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 58
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 0)
    assert state_machine.offset == 79
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("1", 0)
    assert state_machine.offset == 116
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("7", 0)
    assert state_machine.offset == 137
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("6", 0)
    assert state_machine.offset == 158
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("5", 0)
    assert state_machine.offset == 179
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("0", 0)
    assert state_machine.offset == 200
    assert state_machine.get_alphabet() == {}
    assert state_machine.is_complete()

    assert [x + 214 + 378 + 183 for x in state_machine.offset_history] == [
        791,
        812,
        833,  # lon int
        870,
        891,
        912,
        933,
        954,  # lon fraction
    ]


def test_date_20240608() -> None:
    """
    Test parsing of 2024-06-08 14:23:55
    """
    state_machine = DateTime()
    state_machine.append("2", 1)
    state_machine.append("0", -1)
    state_machine.append("2", 1)
    state_machine.append("4", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("0", 1)
    state_machine.append("6", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("0", 1)
    state_machine.append("8", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("1", 1)
    state_machine.append("4", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("2", 1)
    state_machine.append("3", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("5", 1)
    state_machine.append("5", -1)
    assert state_machine.offset == 368
    assert state_machine.get_alphabet() == {}
    assert state_machine.is_complete()
    assert state_machine.offset == 378

    assert [x + 214 for x in state_machine.offset_history] == [
        215,
        235,
        257,
        277,
        315,
        335,
        373,
        393,
        425,
        445,
        483,
        503,
        541,
        561,
    ]


def test_coordinate1_20240608() -> None:
    """
    Test parsing of 47.64068
    """
    state_machine = Coordinate()
    state_machine.append("", 0)
    state_machine.append(" ", 0)
    assert state_machine.get_alphabet() == NEGATIVE_OR_NUMBER
    state_machine.append("4", 1)
    state_machine.append("7", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("6", 1)
    state_machine.append("4", -1)
    state_machine.append("0", 1)
    state_machine.append("6", -1)
    state_machine.append("8", 1)
    assert state_machine.get_alphabet() == {}
    assert state_machine.offset == 184
    assert state_machine.is_complete()

    assert [x + 214 + 378 for x in state_machine.offset_history] == [
        603,
        623,
        661,
        681,
        703,
        723,
        745,
    ]


def test_coordinate2_20240608() -> None:
    """
    Test parsing of -122.17916
    """
    state_machine = Coordinate()
    state_machine.append("-", 0)
    state_machine.append("1", -1)
    state_machine.append("2", 1)
    state_machine.append("2", -1)
    assert state_machine.get_alphabet() == NUMBERS
    state_machine.append("1", 1)
    state_machine.append("7", -1)
    state_machine.append("9", 1)
    state_machine.append("1", -1)
    state_machine.append("6", 1)
    assert state_machine.get_alphabet() == {}
    assert state_machine.offset == 210

    # print(state_machine.)

    assert [x + 214 + 378 + 184 for x in state_machine.offset_history] == [
        791,
        813,
        833,
        871,
        891,
        913,
        933,
        955,
    ]


def test_state_machine() -> None:
    state_machine = StateMachine()
    assert state_machine.get_next_offset() == 214
    state_machine.append("2")
    assert state_machine.get_next_offset() == 235
    state_machine.append("0")
    assert state_machine.get_next_offset() == 256

    state_machine_parity = StateMachine(use_parity=True)
    assert state_machine_parity.get_next_offset() == 215
    state_machine_parity.append("2")
    assert state_machine_parity.get_next_offset() == 235
    state_machine_parity.append("0")
    assert state_machine_parity.get_next_offset() == 257
