""" A list of all the unit conversions. Many are just approximations."""

from .const import (
    LIGHT_LUX,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)

def unit(unit):
    def decorator(func):
        func.unit = unit
        return func
    return decorator


# imperial shenanigans
@unit(UnitOfTemperature.CELSIUS)
def fahrenheit_to_celsius(temp_f: float) -> float:
    return (temp_f - 32) * 5.0/9.0

@unit(UnitOfPressure.HPA)
def inhg_to_hpa(pressure: float) -> float:
    return pressure * 33.864

@unit(UnitOfPrecipitationDepth.MILLIMETERS)
def in_to_mm(length: float) -> float:
    return length * 25.4

@unit(UnitOfIrradiance.WATTS_PER_SQUARE_METER)
def lux_to_wm2(lux: float) -> float:
    return lux * 0.0079

@unit(UnitOfSpeed.METERS_PER_SECOND)
def mph_to_ms(speed: float) -> float:
    return speed * 2.23694


@unit(UnitOfPressure.INHG)
def hpa_to_inhg(pressure: float) -> float:
    return pressure * 0.02953

@unit(UnitOfTemperature.FAHRENHEIT)
def celsius_to_fahrenheit(temp_c: float) -> float:
    return temp_c * 9.0/5.0 + 32

@unit(UnitOfPrecipitationDepth.INCHES)
def mm_to_in(length: float) -> float:
    return length * 0.0393701

@unit(LIGHT_LUX)
def wm2_to_lux(lux: float) -> float:
    return lux * 127

@unit(UnitOfSpeed.MILES_PER_HOUR)
def ms_to_mph(speed: float) -> float:
    return speed * 0.44704