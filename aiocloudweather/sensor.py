""""""

from dataclasses import dataclass, field
from typing import Final

from aiocloudweather.conversion import (celsius_to_fahrenheit, fahrenheit_to_celsius, hpa_to_inhg, in_to_mm, inhg_to_hpa, lux_to_wm2, mm_to_in, mph_to_ms, ms_to_mph, wm2_to_lux)
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


imperial_to_metric: Final = {
    UnitOfPressure.INHG: inhg_to_hpa,
    UnitOfTemperature.FAHRENHEIT: fahrenheit_to_celsius,
    UnitOfPrecipitationDepth.INCHES: in_to_mm,
    LIGHT_LUX: lux_to_wm2,
    UnitOfSpeed.MILES_PER_HOUR: mph_to_ms,
}

metric_to_imperial: Final = {
    UnitOfPressure.HPA: hpa_to_inhg,
    UnitOfTemperature.CELSIUS: celsius_to_fahrenheit,
    UnitOfPrecipitationDepth.MILLIMETERS: mm_to_in,
    UnitOfIrradiance.WATTS_PER_SQUARE_METER: wm2_to_lux,
    UnitOfSpeed.METERS_PER_SECOND: ms_to_mph,
}

@dataclass
class WeatherStationSensor:
    """
    Weather data.
    """
    station_id: str
    station_key: str
    date_utc: str

    barometer: tuple[float,float]
    temperature: tuple[float, float]
    humidity: tuple[float, float]
    indoor_temperature: tuple[float, float]
    indoor_humidity: tuple[float, float]
    dewpoint: tuple[float, float]
    rain: tuple[float, float]
    daily_rain: tuple[float, float]
    wind_direction: tuple[float, float]
    wind_speed: tuple[float, float]
    wind_gust_speed: tuple[float, float]
    wind_gust_direction: tuple[float, float]
    uv: tuple[int, int]
    solar_radiation: tuple[float, float]

    @staticmethod
    def from_wunderground(data: WundergroundRawSensor) -> 'WeatherStationSensor':
        converted_data = {}
        for field, value in data.__dict__.items():
            if field.startswith('_') or field == 'station_id' or field == 'station_key':
                continue
            units = data.__dataclass_fields__[field].metadata.get('units')
            conversion_func = imperial_to_metric.get(units)
            if conversion_func:
                converted_value = conversion_func(value)
                converted_data[field] = converted_value
            else:
                converted_data[field] = value
        return WeatherStationSensor(**converted_data)
    
    @staticmethod
    def from_weathercloud(data: WeathercloudRawSensor) -> 'WeatherStationSensor':
        converted_data = {}
        for field, value in data.__dict__.items():
            if field.startswith('_') or field == 'station_id' or field == 'station_key':
                continue
            units = data.__dataclass_fields__[field].metadata.get('units')
            conversion_func = metric_to_imperial.get(units)
            if conversion_func:
                val = value/10
                converted_value = conversion_func(value)
                converted_data[field] = converted_value
            else:
                converted_data[field] = value
        return WeatherStationSensor(**converted_data)
