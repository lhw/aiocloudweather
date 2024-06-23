""" A list of all the unit conversions. Many are just approximations."""

from .const import (
    LIGHT_LUX,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)


def unit(output_unit):
    """Decorator to set the output unit of the function."""

    def decorator(func):
        func.unit = output_unit
        return func

    return decorator


# imperial shenanigans
@unit(UnitOfTemperature.CELSIUS)
def fahrenheit_to_celsius(temp_f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (temp_f - 32) * 5.0 / 9.0


@unit(UnitOfPressure.HPA)
def inhg_to_hpa(pressure: float) -> float:
    """Convert inches of mercury (inHg) to hectopascals (hPa)."""
    return pressure * 33.864


@unit(UnitOfPrecipitationDepth.MILLIMETERS)
def in_to_mm(length: float) -> float:
    """Convert inches to millimeters (mm)."""
    return length * 25.4


@unit(UnitOfIrradiance.WATTS_PER_SQUARE_METER)
def lux_to_wm2(lux: float) -> float:
    """Convert lux to watts per square meter (W/m²).
    For natural daylight, the luminous efficacy varies
    but is typically in the range of 90 to 120 lm/W.
    A commonly used average value is around 93 lm/W
    """
    return lux / 93


@unit(UnitOfSpeed.METERS_PER_SECOND)
def mph_to_ms(speed: float) -> float:
    """Convert miles per hour (mph) to meters per second (m/s)."""
    return speed * 0.44704


@unit(UnitOfPressure.INHG)
def hpa_to_inhg(pressure: float) -> float:
    """Convert hectopascals (hPa) to inches of mercury (inHg)."""
    return pressure * 0.02953


@unit(UnitOfTemperature.FAHRENHEIT)
def celsius_to_fahrenheit(temp_c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return temp_c * 9.0 / 5.0 + 32


@unit(UnitOfPrecipitationDepth.INCHES)
def mm_to_in(length: float) -> float:
    """Convert millimeters (mm) to inches."""
    return length * 0.0393701


@unit(LIGHT_LUX)
def wm2_to_lux(lux: float) -> float:
    """Convert watts per square meter (W/m²) to lux.
    For natural daylight, the luminous efficacy varies
    but is typically in the range of 90 to 120 lm/W.
    A commonly used average value is around 93 lm/W
    """
    return lux * 93


@unit(UnitOfSpeed.MILES_PER_HOUR)
def ms_to_mph(speed: float) -> float:
    """Convert meters per second (m/s) to miles per hour (mph)."""
    return speed * 2.23694
