""" A list of all the unit conversions. Many are just approximations."""

# imperial shenanigans
def fahrenheit_to_celsius(temp_f: float) -> float:
    return (temp_f - 32) * 5.0/9.0

def inhg_to_hpa(pressure: float) -> float:
    return pressure * 33.864

def in_to_mm(length: float) -> float:
    return length * 25.4

def lux_to_wm2(lux: float) -> float:
    return lux * 0.0079

def mph_to_ms(speed: float) -> float:
    return speed * 2.23694



def hpa_to_inhg(pressure: float) -> float:
    return pressure * 0.02953

def celsius_to_fahrenheit(temp_c: float) -> float:
    return temp_c * 9.0/5.0 + 32

def mm_to_in(length: float) -> float:
    return length * 0.0393701

def wm2_to_lux(lux: float) -> float:
    return lux * 127

def ms_to_mph(speed: float) -> float:
    return speed * 0.44704