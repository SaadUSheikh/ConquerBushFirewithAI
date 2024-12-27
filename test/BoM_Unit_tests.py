import pytest
import json
from requests_mock import Mocker
import sys
sys.path.append('../backend/bom_harvester/melbourne-all/harvester/')
from bom_fission import app, fetch_weather_data, parse_time, parse_float, parse_int, get_latitude, get_longitude, parse_time_UTC


# BoM RestfulAPI Function Unit tests
def test_parse_int():
    assert parse_int("100") == 100
    assert parse_int("abc") is None

def test_parse_float():
    # Test normal float conversion
    assert parse_float("123.45") == 123.45
    # Test integer conversion to float
    assert parse_float("123") == 123.0
    # Test invalid string
    assert parse_float("abc") is None
    # Test empty string
    assert parse_float("") is None

def test_parse_time_valid():
    assert parse_time("10:30PM") == "22:30"
    assert parse_time("12:00AM") == "00:00"

def test_parse_time_invalid():
    assert parse_time("25:30PM") is None
    assert parse_time("13:60PM") is None

def test_parse_time_placeholder():
    assert parse_time("-") is None
    assert parse_time("") is None
    
def test_get_latitude_longitude_valid():
    assert get_latitude("Melbourne (Olympic Park)") == -37.8
    assert get_longitude("Melbourne (Olympic Park)") == 145.0

def test_get_latitude_longitude_invalid():
    assert get_latitude("Nonexistent Station") is None
    assert get_longitude("Nonexistent Station") is None
    
def test_parse_time_UTC_valid():
    melbourne_time = "10:30PM"
    melbourne_date = "2024-04-27"
    # Expected to convert Melbourne time (UTC+10) to UTC time
    assert parse_time_UTC(melbourne_time, melbourne_date) == "2024-04-27T12:30"

def test_parse_time_UTC_invalid():
    test_date = '2024-04-27'
    assert parse_time_UTC("25:30PM", test_date) is None
    assert parse_time_UTC("", test_date) is None

def test_parse_time_UTC_special_values():
    test_date = '2024-04-27'
    test_time = "10:30PM"
    assert parse_time_UTC("-", test_date) is None
    assert parse_time_UTC("", test_date) is None
    assert parse_time_UTC(test_time, "-") is None

if __name__ == "__main__":
    pytest.main()
