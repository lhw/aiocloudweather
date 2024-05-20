""""""

from dataclasses import dataclass, field
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

@dataclass
class CloudRawSensor:
    station_id: str
    station_key: str

@dataclass
class WundergroundRawSensor(CloudRawSensor):
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
        default=None, metadata={"units": UnitOfPressure.INHG, "arg": "baromin"}
    )
    temperature: float = field(
        default=None, metadata={"units": UnitOfTemperature.FAHRENHEIT, "arg": "tempf"}
    )
    humidity: float = field(
        default=None, metadata={"units": PERCENTAGE, "arg": "humidity"}
    )
    indoor_temperature: float = field(
        default=None,
        metadata={"units": UnitOfTemperature.FAHRENHEIT, "arg": "indoortempf"},
    )
    indoor_humidity: float = field(
        default=None, metadata={"units": PERCENTAGE, "arg": "indoorhumidity"}
    )

    dewpoint: float = field(
        default=None, metadata={"units": UnitOfTemperature.FAHRENHEIT, "arg": "dewptf"}
    )
    rain: float = field(
        default=None,
        metadata={"units": UnitOfPrecipitationDepth.INCHES, "arg": "rainin"},
    )
    daily_rain: float = field(
        default=None,
        metadata={"units": UnitOfPrecipitationDepth.INCHES, "arg": "dailyrainin"},
    )
    wind_direction: float = field(
        default=None, metadata={"units": DEGREE, "arg": "winddir"}
    )
    wind_speed: float = field(
        default=None,
        metadata={"units": UnitOfSpeed.MILES_PER_HOUR, "arg": "windspeedmph"},
    )
    wind_gust_speed: float = field(
        default=None,
        metadata={"units": UnitOfSpeed.MILES_PER_HOUR, "arg": "windgustmph"},
    )
    wind_gust_direction: float = field(
        default=None, metadata={"units": DEGREE, "arg": "windgustdir"}
    )
    uv: int = field(default=None, metadata={"units": UV_INDEX, "arg": "UV"})
    solar_radiation: float = field(
        default=None, metadata={"units": LIGHT_LUX, "arg": "solarRadiation"}
    )


@dataclass
class WeathercloudRawSensor(CloudRawSensor):
    """WeatherCloud API sensor parsed from the query path."""

    # /v01/set/wid/12345/key/12345/bar/10130/temp/164/hum/80/wdir/288/wspd/0/dew/129/heat/164/rainrate/0/rain/0/uvi/0/solarrad/47
    # Additional fields from https://groups.google.com/g/weewx-development/c/hLuHxl_W6kM/m/wQ61KIhNBoQJ
    station_id: str = field(metadata={"arg": "wid"})
    station_key: str = field(metadata={"arg": "key"})

    barometer: int = field(
        default=None, metadata={"units": UnitOfPressure.HPA, "arg": "bar"}
    )
    temperature: int = field(
        default=None, metadata={"units": UnitOfTemperature.CELSIUS, "arg": "temp"}
    )
    humidity: int = field(default=None, metadata={"units": PERCENTAGE, "arg": "hum"})
    indoor_temperature: int = field(
        default=None, metadata={"units": UnitOfTemperature.CELSIUS, "arg": "tempin"}
    )
    indoor_humidity: int = field(
        default=None, metadata={"units": PERCENTAGE, "arg": "humin"}
    )
    dewpoint: int = field(
        default=None, metadata={"units": UnitOfTemperature.CELSIUS, "arg": "dew"}
    )
    heat_index: int = field(
        default=None, metadata={"units": UnitOfTemperature.CELSIUS, "arg": "heat"}
    )
    daily_rain: int = field(
        default=None,
        metadata={"units": UnitOfPrecipitationDepth.MILLIMETERS, "arg": "rain"},
    )
    rain_rate: int = field(
        default=None,
        metadata={
            "units": UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR,
            "arg": "rainrate",
        },
    )
    wind_direction: int = field(default=None, metadata={"units": DEGREE, "arg": "wdir"})
    wind_speed: int = field(
        default=None, metadata={"units": UnitOfSpeed.METERS_PER_SECOND, "arg": "wspd"}
    )
    wind_gust_speed: int = field(
        default=None, metadata={"units": UnitOfSpeed.METERS_PER_SECOND, "arg": "wspdhi"}
    )
    wind_chill: int = field(
        default=None, metadata={"units": UnitOfTemperature.CELSIUS, "arg": "chill"}
    )
    uv: int = field(default=None, metadata={"units": UV_INDEX, "arg": "uvi"})
    solar_radiation: int = field(
        default=None,
        metadata={"units": UnitOfIrradiance.WATTS_PER_SQUARE_METER, "arg": "solarrad"},
    )
