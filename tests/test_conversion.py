from aiocloudweather.conversion import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    hpa_to_inhg,
    in_to_mm,
    inhg_to_hpa,
    lux_to_wm2,
    mm_to_in,
    mph_to_ms,
    ms_to_mph,
    wm2_to_lux,
)


def test_fahrenheit_to_celsius():
    assert round(fahrenheit_to_celsius(32), 2) == 0
    assert round(fahrenheit_to_celsius(212), 2) == 100
    assert round(fahrenheit_to_celsius(50), 2) == 10


def test_inhg_to_hpa():
    assert round(inhg_to_hpa(29.92), 2) == 1013.21
    assert round(inhg_to_hpa(30), 2) == 1015.92
    assert round(inhg_to_hpa(28), 2) == 948.19


def test_in_to_mm():
    assert round(in_to_mm(1), 2) == 25.4
    assert round(in_to_mm(2.5), 2) == 63.5
    assert round(in_to_mm(0.5), 2) == 12.7


def test_lux_to_wm2():
    assert round(lux_to_wm2(100), 2) == 1.08
    assert round(lux_to_wm2(500), 2) == 5.38
    assert round(lux_to_wm2(1000), 2) == 10.75


def test_mph_to_ms():
    assert round(mph_to_ms(10), 4) == 4.4704
    assert round(mph_to_ms(30), 4) == 13.4112
    assert round(mph_to_ms(5), 4) == 2.2352


def test_hpa_to_inhg():
    assert round(hpa_to_inhg(1013.25), 2) == 29.92
    assert round(hpa_to_inhg(1000), 2) == 29.53
    assert round(hpa_to_inhg(950), 2) == 28.05


def test_celsius_to_fahrenheit():
    assert round(celsius_to_fahrenheit(0)) == 32
    assert round(celsius_to_fahrenheit(100)) == 212
    assert round(celsius_to_fahrenheit(10)) == 50


def test_mm_to_in():
    assert round(mm_to_in(25.4), 2) == 1
    assert round(mm_to_in(63.5), 2) == 2.5
    assert round(mm_to_in(12.7), 2) == 0.5


def test_wm2_to_lux():
    assert round(wm2_to_lux(1)) == 93
    assert round(wm2_to_lux(5)) == 465
    assert round(wm2_to_lux(10)) == 930


def test_ms_to_mph():
    assert round(ms_to_mph(4.4704), 4) == 10
    assert round(ms_to_mph(13.4112), 4) == 30
    assert round(ms_to_mph(2.2352), 4) == 5
