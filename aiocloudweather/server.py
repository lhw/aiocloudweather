"""aioEcoWitt API server."""

from __future__ import annotations

import logging
from typing import Callable
from copy import deepcopy

from aiohttp import web

from aiocloudweather.sensor import WundergroundRawSensor, WeathercloudRawSensor, WeatherStation

_LOGGER = logging.getLogger(__name__)
_CLOUDWEATHER_LISTEN_PORT = 49199


class CloudWeatherListener:
    """EcoWitt Server API server."""

    def __init__(self, port: int = _CLOUDWEATHER_LISTEN_PORT):
        """Initialize EcoWitt Server."""
        # API Constants
        self.port: int = port

        # webserver
        self.server: None | web.Server = None
        self.runner: None | web.ServerRunner = None
        self.site: None | web.TCPSite = None

        # internal data
        self.last_values: dict[str, dict[str, str | None]] = {}
        self.new_dataset_cb: list[Callable[[WeatherStation], None]] = []

        # storage
        self.stations: list[str] = []

    async def _new_dataset_cb(self, dataset: WeatherStation) -> None:
        """Internal new sensor callback

        binds to self.new_sensor_cb
        """
        for callback in self.new_dataset_cb:
            await callback(dataset)

    async def process_wunderground(self, data: dict[str, str | float]) -> WeatherStation:
        """Process Wunderground data."""

        fields = {f.metadata["arg"]: [f.name, f.type] for f in WundergroundRawSensor.__dataclass_fields__.values() if "arg" in f.metadata}
        instance_data = {}
        for arg, field in fields.items():
            if arg in data:
                instance_data[field[0]] = field[1](data[arg])

        return WeatherStation.from_wunderground(WundergroundRawSensor(**instance_data))

    async def process_weathercloud(self, path: str):
        """Process WeatherCloud data."""

        segments = [seg for seg in path.split('/') if seg]

        data = dict(zip(segments[2::2], map(int, segments[3::2])))

        fields = {f.metadata["arg"]: [f.name, f.type] for f in WeathercloudRawSensor.__dataclass_fields__.values() if "arg" in f.metadata}
        instance_data = {field[0]: field[1](data[arg]) for arg, field in fields.items() if arg in data}

        return WeatherStation.from_weathercloud(WeathercloudRawSensor(**instance_data))

    async def handler(self, request: web.BaseRequest) -> web.Response:
        """AIOHTTP handler for the API."""

        if request.method != "GET" or request.path is None:
            raise web.HTTPBadRequest()

        station_id: str = None
        dataset: WundergroundRawSensor | WeathercloudRawSensor = None
        if request.path.startswith('/weatherstation/updateweatherstation.php'):
            dataset = await self.process_wunderground(request.query)
            station_id = dataset.station_id
        elif request.path.startswith('/v01/set'):
            dataset = await self.process_weathercloud(request.path)
            station_id = dataset.station_id
        
        if station_id not in self.stations:
            _LOGGER.debug("Found new station: %s", station_id)
            self.stations.append(station_id)

        try:
            await self._new_dataset_cb(dataset)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.warning("CloudWeather new dataset callback error: %s", err)

        self.last_values[station_id] = deepcopy(dataset)
        return web.Response(text="OK")

    async def start(self) -> None:
        """Listen and process."""

        self.server = web.Server(self.handler)
        self.runner = web.ServerRunner(self.server)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, port=self.port)
        await self.site.start()

    async def stop(self) -> None:
        """Stop listening."""
        await self.site.stop()