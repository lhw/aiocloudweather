""" A list of all the unit conversions. Many are just approximations."""

from .const import (
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
