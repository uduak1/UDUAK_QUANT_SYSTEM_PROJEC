import pytest

from analysis.fvg_filter import FVGFilter


def valid_fvg():
    return {
        "gap_size": 0.0010,
        "age": 5,
        "retest_count": 1,
        "status": "OPEN",
        "direction": "BULLISH",
    }


def test_valid_fvg_passes_filter():
    response = FVGFilter().filter([valid_fvg()])

    assert response.success is True
    assert response.data["filtered_count"] == 1
    assert response.data["rejected_count"] == 0


def test_mitigated_fvg_rejected():
    fvg = valid_fvg()
    fvg["status"] = "MITIGATED"

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_small_gap_rejected():
    fvg = valid_fvg()
    fvg["gap_size"] = 0.0001

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0


def test_old_gap_rejected():
    fvg = valid_fvg()
    fvg["age"] = 50

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0


def test_excessive_retests_rejected():
    fvg = valid_fvg()
    fvg["retest_count"] = 5

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0


def test_malformed_fvg_rejected():
    response = FVGFilter().filter([{"bad": "data"}])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_empty_list_returns_success():
    response = FVGFilter().filter([])

    assert response.success is True
    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 0


def test_none_input_returns_error():
    response = FVGFilter().filter(None)

    assert response.success is False
    assert response.error == "EMPTY_FVG"


def test_mixed_valid_invalid_fvg():
    valid = valid_fvg()

    invalid = valid_fvg()
    invalid["status"] = "MITIGATED"

    response = FVGFilter().filter([valid, invalid])

    assert response.data["filtered_count"] == 1
    assert response.data["rejected_count"] == 1


def test_response_structure():
    response = FVGFilter().filter([valid_fvg()])

    assert "filtered_fvg" in response.data
    assert "rejected_fvg" in response.data
    assert "filtered_count" in response.data
    assert "rejected_count" in response.data


# ==========================================================
# Additional coverage tests
# ==========================================================

def test_invalid_direction_rejected():
    fvg = valid_fvg()
    fvg["direction"] = "SIDEWAYS"

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_invalid_status_rejected():
    fvg = valid_fvg()
    fvg["status"] = "UNKNOWN"

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_invalid_gap_size_rejected():
    fvg = valid_fvg()
    fvg["gap_size"] = -1

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_invalid_age_rejected():
    fvg = valid_fvg()
    fvg["age"] = -5

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_invalid_retest_count_rejected():
    fvg = valid_fvg()
    fvg["retest_count"] = -2

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_open_not_allowed():
    filt = FVGFilter()
    filt.ALLOW_OPEN = False

    response = filt.filter([valid_fvg()])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_partially_filled_allowed():
    fvg = valid_fvg()
    fvg["status"] = "PARTIALLY_FILLED"

    response = FVGFilter().filter([fvg])

    assert response.data["filtered_count"] == 1


def test_partial_not_allowed():
    filt = FVGFilter()
    filt.ALLOW_PARTIALLY_FILLED = False

    fvg = valid_fvg()
    fvg["status"] = "PARTIALLY_FILLED"

    response = filt.filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1


def test_mitigated_allowed_when_flag_disabled():
    filt = FVGFilter()
    filt.REJECT_MITIGATED = False

    fvg = valid_fvg()
    fvg["status"] = "MITIGATED"

    response = filt.filter([fvg])

    assert response.data["filtered_count"] == 0
    assert response.data["rejected_count"] == 1

def test_validate_fvg_rejects_non_dict():
    from analysis.fvg_filter import FVGFilter

    f = FVGFilter()

    assert f._validate_fvg(None) is False
    assert f._validate_fvg([]) is False
    assert f._validate_fvg("not a dict") is False

