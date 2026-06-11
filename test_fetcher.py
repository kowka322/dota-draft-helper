import pytest
from fetcher import is_valid_match


@pytest.fixture
def good_match():
    return {
        "duration": 1500,
        "lobby_type": 7,
        "game_mode": 22,
        "radiant_team": [1, 2, 3, 4, 5],
        "dire_team": [6, 7, 8, 9, 10],
        "num_rank_tier": 8,
        "avg_rank_tier": 75,
    }


def test_valid_match_returns_true(good_match):
    assert is_valid_match(good_match) == True

@pytest.mark.parametrize("field,bad_value", [
    ("duration", 0),
    ("lobby_type", 0),
    ("game_mode", 0),
    ("num_rank_tier", 0),
    ("avg_rank_tier", 0),
])
def test_invalid_field_returns_false(good_match, field, bad_value):
    good_match[field] = bad_value
    assert is_valid_match(good_match) == False
    

@pytest.mark.parametrize("field,bad_value", [
    ("radiant_team", [0, 1, 2, 3, 4]),
    ("dire_team", [0, 6, 7, 8, 9]),
])
def test_invalid_team_returns_false(good_match, field, bad_value):
    good_match[field] = bad_value
    assert is_valid_match(good_match) == False