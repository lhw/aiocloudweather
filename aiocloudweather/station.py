"""The module parses incoming weather data from various sources into a common format."""

from dataclasses import dataclass, field, fields
from enum import Enum
import logging
from typing import Final

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
from .const import (
    DEGREE,
    LIGHT_LUX,
    PERCENTAGE,
    UV_INDEX,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfVolumetricFlux,
)

_LOGGER = logging.getLogger(__name__)


class WeatherstationVendor(Enum):
    """The weather station cloud vendor."""

    WUNDERGROUND = "Weather Underground"
    WEATHERCLOUD = "Weathercloud.net"


@dataclass
class WundergroundRawSensor:
    """Wunderground sensor parsed from query string."""

    # /weatherstation/updateweatherstation.php?ID=12345&PASSWORD=12345&dateutc=2024-5-18+16%3A42%3A43&baromin=29.92&tempf=72.5&humidity=44&dewptf=49.2&rainin=0&dailyrainin=0&winddir=249&windspeedmph=2.0&windgustmph=2.7&UV=2&solarRadiation=289.2
    # Additional fields from https://www.openhab.org/addons/bindings/wundergroundupdatereceiver/
    station_id: str = field(metadata={"arg": "ID"})
    station_key: str = field(metadata={"arg": "PASSWORD"})

    date_utc: str = field(
        default=None,
        metadata={"arg": "dateutc", "format_string": "%Y-%m-%d+%H%%3A%M%%3A%S"},
    )

    barometer: float = field(
        default=None, metadata={"unit": UnitOfPressure.INHG, "arg": "baromin"}
    )
    temperature: float = field(
        default=None, metadata={"unit": UnitOfTemperature.FAHRENHEIT, "arg": "tempf"}
    )
    humidity: float = field(
        default=None, metadata={"unit": PERCENTAGE, "arg": "humidity"}
    )
    indoortemperature: float = field(
        default=None,
        metadata={"unit": UnitOfTemperature.FAHRENHEIT, "arg": "indoortempf"},
    )
    indoorhumidity: float = field(
        default=None, metadata={"unit": PERCENTAGE, "arg": "indoorhumidity"}
    )

    dewpoint: float = field(
        default=None, metadata={"unit": UnitOfTemperature.FAHRENHEIT, "arg": "dewptf"}
    )
    rain: float = field(
        default=None,
        metadata={"unit": UnitOfPrecipitationDepth.INCHES, "arg": "rainin"},
    )
    dailyrain: float = field(
        default=None,
        metadata={"unit": UnitOfPrecipitationDepth.INCHES, "arg": "dailyrainin"},
    )
    winddirection: float = field(
        default=None, metadata={"unit": DEGREE, "arg": "winddir"}
    )
    windspeed: float = field(
        default=None,
        metadata={"unit": UnitOfSpeed.MILES_PER_HOUR, "arg": "windspeedmph"},
    )
    windgustspeed: float = field(
        default=None,
        metadata={"unit": UnitOfSpeed.MILES_PER_HOUR, "arg": "windgustmph"},
    )
    windgustdirection: float = field(
        default=None, metadata={"unit": DEGREE, "arg": "windgustdir"}
    )
    uv: int = field(default=None, metadata={"unit": UV_INDEX, "arg": "UV"})
    solarradiation: float = field(
        default=None,
        metadata={
            "unit": LIGHT_LUX,
            "keep": True,
            "factor": 1000,
            "arg": "solarRadiation",
        },
    )


@dataclass
class WeathercloudRawSensor:
    """WeatherCloud API sensor parsed from the query path."""

    # /v01/set/wid/12345/key/12345/bar/10130/temp/164/hum/80/wdir/288/wspd/0/dew/129/heat/164/rainrate/0/rain/0/uvi/0/solarrad/47
    # Additional fields from https://groups.google.com/g/weewx-development/c/hLuHxl_W6kM/m/wQ61KIhNBoQJ
    station_id: str = field(metadata={"arg": "wid"})
    station_key: str = field(metadata={"arg": "key"})

    barometer: int = field(
        default=None, metadata={"unit": UnitOfPressure.HPA, "arg": "bar"}
    )
    temperature: int = field(
        default=None, metadata={"unit": UnitOfTemperature.CELSIUS, "arg": "temp"}
    )
    humidity: int = field(default=None, metadata={"unit": PERCENTAGE, "arg": "hum"})
    indoortemperature: int = field(
        default=None, metadata={"unit": UnitOfTemperature.CELSIUS, "arg": "tempin"}
    )
    indoorhumidity: int = field(
        default=None, metadata={"unit": PERCENTAGE, "arg": "humin"}
    )
    dewpoint: int = field(
        default=None, metadata={"unit": UnitOfTemperature.CELSIUS, "arg": "dew"}
    )
    heatindex: int = field(
        default=None, metadata={"unit": UnitOfTemperature.CELSIUS, "arg": "heat"}
    )
    dailyrain: int = field(
        default=None,
        metadata={"unit": UnitOfPrecipitationDepth.MILLIMETERS, "arg": "rain"},
    )
    rain: int = field(
        default=None,
        metadata={
            "unit": UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR,
            "arg": "rainrate",
        },
    )
    winddirection: int = field(default=None, metadata={"unit": DEGREE, "arg": "wdir"})
    windspeed: int = field(
        default=None, metadata={"unit": UnitOfSpeed.METERS_PER_SECOND, "arg": "wspd"}
    )
    windgustspeed: int = field(
        default=None, metadata={"unit": UnitOfSpeed.METERS_PER_SECOND, "arg": "wspdhi"}
    )
    windchill: int = field(
        default=None, metadata={"unit": UnitOfTemperature.CELSIUS, "arg": "chill"}
    )
    uv: int = field(default=None, metadata={"unit": UV_INDEX, "arg": "uvi"})
    solarradiation: int = field(
        default=None,
        metadata={
            "unit": UnitOfIrradiance.WATTS_PER_SQUARE_METER,
            "keep": True,
            "arg": "solarrad",
        },
    )


IMPERIAL_TO_METRIC: Final = {
    UnitOfPressure.INHG: inhg_to_hpa,
    UnitOfTemperature.FAHRENHEIT: fahrenheit_to_celsius,
    UnitOfPrecipitationDepth.INCHES: in_to_mm,
    LIGHT_LUX: lux_to_wm2,
    UnitOfSpeed.MILES_PER_HOUR: mph_to_ms,
}

METRIC_TO_IMPERIAL: Final = {
    UnitOfPressure.HPA: hpa_to_inhg,
    UnitOfTemperature.CELSIUS: celsius_to_fahrenheit,
    UnitOfPrecipitationDepth.MILLIMETERS: mm_to_in,
    UnitOfIrradiance.WATTS_PER_SQUARE_METER: wm2_to_lux,
    UnitOfSpeed.METERS_PER_SECOND: ms_to_mph,
}


@dataclass
class Sensor:
    """Represents a weather sensor."""

    name: str

    metric: float
    metric_unit: str
    imperial: float
    imperial_unit: str


@dataclass
class WeatherStation:
    """
    Represents a weather station with various sensor readings.
    """

    station_id: str
    station_key: str
    vendor: WeatherstationVendor

    station_sw_version: str = field(default=None)
    station_client_ip: str = field(default=None)
    update_time: float = field(default=None)

    date_utc: str = field(default=None)

    barometer: Sensor = field(default=None, metadata={"name": "Absolute Pressure"})
    temperature: Sensor = field(default=None, metadata={"name": "Outdoor Temperature"})
    humidity: Sensor = field(default=None, metadata={"name": "Outdoor Humidity"})
    indoortemperature: Sensor = field(
        default=None, metadata={"name": "Indoor Temperature"}
    )
    indoorhumidity: Sensor = field(default=None, metadata={"name": "Indoor Humidity"})
    dewpoint: Sensor = field(default=None, metadata={"name": "Outdoor Dewpoint"})
    rain: Sensor = field(default=None, metadata={"name": "Rain Rate"})
    dailyrain: Sensor = field(default=None, metadata={"name": "Daily Rain Rate"})
    winddirection: Sensor = field(default=None, metadata={"name": "Wind Direction"})
    windspeed: Sensor = field(default=None, metadata={"name": "Wind Speed"})
    windgustspeed: Sensor = field(default=None, metadata={"name": "Wind Gust"})
    windgustdirection: Sensor = field(
        default=None, metadata={"name": "Wind Gust Direction"}
    )
    uv: Sensor = field(default=None, metadata={"name": "UV Index"})
    solarradiation: Sensor = field(default=None, metadata={"name": "Solar Radiation"})
    solarradiationraw: Sensor = field(
        default=None, metadata={"name": "Solar Radiation Raw"}
    )
    heatindex: Sensor = field(default=None, metadata={"name": "Heat Index"})

    @staticmethod
    def from_wunderground(data: WundergroundRawSensor) -> "WeatherStation":
        """
        Converts raw sensor data from the Wunderground API into a WeatherStation object.

        Args:
            data (WundergroundRawSensor): The raw sensor data from the Wunderground API.

        Returns:
            WeatherStation: The converted WeatherStation object.

        Raises:
            TypeError: If there is an error converting the sensor data.

        """
        sensor_data = {}
        for sensor_field in fields(data):
            if sensor_field.name in ("station_id", "station_key"):
                continue
            value = getattr(data, sensor_field.name)
            if value is None:
                continue

            value = sensor_field.type(value) * sensor_field.metadata.get("factor", 1)
            unit = sensor_field.metadata.get("unit")
            keep_original = sensor_field.metadata.get("keep", False)
            conversion_func = IMPERIAL_TO_METRIC.get(unit)

            if conversion_func:
                try:
                    converted_value = conversion_func(value)
                except TypeError as e:
                    _LOGGER.error(
                        "Failed to convert %s from %s to %s: %s[%s] -> %s",
                        sensor_field,
                        unit,
                        conversion_func.unit,
                        value,
                        type(value),
                        e,
                    )
                    continue
                sensor_data[sensor_field.name] = Sensor(
                    name=sensor_field.name,
                    metric=converted_value,
                    metric_unit=conversion_func.unit,
                    imperial=value,
                    imperial_unit=unit,
                )
            if not conversion_func or keep_original:
                field_name = (
                    sensor_field.name
                    if not keep_original
                    else f"{sensor_field.name}raw"
                )
                sensor_data[field_name] = Sensor(
                    name=field_name,
                    metric=value,
                    metric_unit=unit,
                    imperial=value,
                    imperial_unit=unit,
                )
        return WeatherStation(
            station_id=data.station_id,
            station_key=data.station_key,
            vendor=WeatherstationVendor.WUNDERGROUND,
            **sensor_data,
        )

    @staticmethod
    def from_weathercloud(data: WeathercloudRawSensor) -> "WeatherStation":
        """
        Converts raw sensor data from the Weathercloud.net API into a WeatherStation object.

        Args:
            data (WeathercloudRawSensor): The raw sensor data from the Weathercloud.net API.

        Returns:
            WeatherStation: The converted WeatherStation object.

        Raises:
            TypeError: If there is an error converting the sensor data.

        """
        sensor_data = {}
        for sensor_field in fields(data):
            if sensor_field.name in ("station_id", "station_key"):
                continue
            value = getattr(data, sensor_field.name)
            if value is None:
                continue

            value = sensor_field.type(value)  # No idea why this is needed
            unit = sensor_field.metadata.get("unit")
            conversion_func = METRIC_TO_IMPERIAL.get(unit)

            if conversion_func:
                value: float = float(value) / 10  # All values are shifted by 10
                try:
                    converted_value = conversion_func(value)
                except TypeError as e:
                    _LOGGER.error(
                        "Failed to convert %s from %s to %s: %s -> %s",
                        sensor_field,
                        unit,
                        conversion_func.unit,
                        value,
                        e,
                    )
                    continue
                converted_value = conversion_func(value)
                sensor_data[sensor_field.name] = Sensor(
                    name=sensor_field.name,
                    metric=float(value),
                    metric_unit=unit,
                    imperial=converted_value,
                    imperial_unit=conversion_func.unit,
                )
            else:
                sensor_data[sensor_field.name] = Sensor(
                    name=sensor_field.name,
                    metric=value,
                    metric_unit=unit,
                    imperial=value,
                    imperial_unit=unit,
                )

        return WeatherStation(
            station_id=str(data.station_id),
            station_key=str(data.station_key),
            vendor=WeatherstationVendor.WEATHERCLOUD,
            **sensor_data,
        )
