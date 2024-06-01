from aiocloudweather.station import (
    WeatherStation,
    WundergroundRawSensor,
    WeathercloudRawSensor,
)


def test_weather_station_from_wunderground():
    raw_sensor_data = WundergroundRawSensor(
        station_id="12345",
        station_key="12345",
        barometer=29.92,
        temperature=72.5,
        humidity=44,
        dewpoint=49.2,
        rain=0,
        dailyrain=0,
        winddirection=249,
        windspeed=2.0,
        windgustspeed=2.7,
        uv=2,
        solarradiation=289.2,
    )
    weather_station = WeatherStation.from_wunderground(raw_sensor_data)

    assert weather_station.station_id == "12345"
    assert weather_station.station_key == "12345"
    assert round(weather_station.barometer.metric, 2) == 1013.21
    assert weather_station.barometer.metric_unit == "hPa"
    assert weather_station.barometer.imperial == 29.92
    assert weather_station.barometer.imperial_unit == "inHg"
    assert weather_station.temperature.metric == 22.5
    assert weather_station.temperature.metric_unit == "°C"
    assert weather_station.temperature.imperial == 72.5
    assert weather_station.temperature.imperial_unit == "°F"
    assert weather_station.humidity.metric == 44
    assert weather_station.humidity.metric_unit == "%"
    assert weather_station.humidity.imperial == 44
    assert weather_station.humidity.imperial_unit == "%"


def test_weather_station_from_weathercloud():
    raw_sensor_data = WeathercloudRawSensor(
        station_id="12345",
        station_key="12345",
        barometer=10130,
        temperature=160,
        humidity=80,
        dewpoint=129,
        rain=0,
        dailyrain=0,
        winddirection=288,
        windspeed=0,
        windgustspeed=0,
        uv=0,
        solarradiation=470,
    )
    weather_station = WeatherStation.from_weathercloud(raw_sensor_data)

    assert weather_station.station_id == "12345"
    assert weather_station.station_key == "12345"
    assert weather_station.barometer.metric == 1013
    assert weather_station.barometer.metric_unit == "hPa"
    assert round(weather_station.barometer.imperial, 2) == 29.91
    assert weather_station.barometer.imperial_unit == "inHg"
    assert weather_station.temperature.metric == 16
    assert weather_station.temperature.metric_unit == "°C"
    assert weather_station.temperature.imperial == 60.8
    assert weather_station.temperature.imperial_unit == "°F"
    assert weather_station.humidity.metric == 80
    assert weather_station.humidity.metric_unit == "%"
    assert weather_station.humidity.imperial == 80
    assert weather_station.humidity.imperial_unit == "%"
