from config.timeframes import (
    M1,
    M5,
    M15,
    H1,
    D1,
    timeframes,
)


def test_minutes():
    assert M1.minutes == 1
    assert M5.minutes == 5
    assert M15.minutes == 15
    assert H1.minutes == 60
    assert D1.minutes == 1440


def test_rank_order():
    assert M1.rank < M5.rank < M15.rank < H1.rank < D1.rank


def test_execution():
    assert timeframes.execution.name == "M5"


def test_confirmation():
    assert timeframes.confirmation.name == "M15"


def test_trend():
    assert timeframes.trend.name == "H1"


def test_macro():
    assert timeframes.macro.name == "H4"


def test_supported_timeframes():
    assert len(timeframes.supported) == 9


def test_unique_names():
    names = [tf.name for tf in timeframes.supported]
    assert len(names) == len(set(names))