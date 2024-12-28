"""aioCloudWeather API server."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Coroutine
from copy import deepcopy
from dataclasses import fields

from aiohttp import web

from .proxy import CloudWeatherProxy, DataSink
from .station import (
    WundergroundRawSensor,
    WeathercloudRawSensor,
    WeatherStation,
)

_LOGGER = logging.getLogger(__name__)
_CLOUDWEATHER_LISTEN_PORT = 49199


class CloudWeatherListener:
    """CloudWeather Server API server."""

    def __init__(
        self,
        port: int = _CLOUDWEATHER_LISTEN_PORT,
        proxy_sinks: list[DataSink] | None = None,
        dns_servers: list[str] | None = None,
    ):
        """Initialize CloudWeather Server."""
        # API Constants
        self.port: int = port

        # Proxy functionality
        self.proxy: None | CloudWeatherProxy = None
        self.dns_servers: list[str] = dns_servers or ["9.9.9.9"]
        self.proxy_sinks: list[DataSink] | None = proxy_sinks
        self.proxy_enabled: bool = proxy_sinks and len(proxy_sinks) > 0
        if self.proxy_enabled:
            self.proxy = CloudWeatherProxy(proxy_sinks, dns_servers or ["9.9.9.9"])

        # webserver
        self.server: None | web.Server = None
        self.runner: None | web.ServerRunner = None
        self.site: None | web.TCPSite = None

        # internal data
        self.last_values: dict[str, WeatherStation] = {}
        self.last_updates: dict[str, float] = {}
        self.new_dataset_cb: list[
            Callable[[WeatherStation], Coroutine[Any, Any, Any]]
        ] = []

        # storage
        self.stations: list[str] = []

    async def update_config(
        self,
        proxy_sinks: list[DataSink] | None = None,
        dns_servers: list[str] | None = None,
    ) -> None:
        """Update the proxy configuration."""
        self.proxy_enabled = proxy_sinks and len(proxy_sinks) > 0
        if self.proxy_enabled:
            if self.proxy:
                await self.proxy.close()
            self.proxy = CloudWeatherProxy(proxy_sinks, dns_servers or ["9.9.9.9"])

    def get_active_proxies(self) -> list[DataSink]:
        """Get the active proxies."""
        return self.proxy_sinks

    def get_dns_servers(self) -> list[str]:
        """Get the DNS servers."""
        return self.dns_servers

    async def _new_dataset_cb(self, dataset: WeatherStation) -> None:
        """Internal new sensor callback

        binds to self.new_sensor_cb
        """
        for callback in self.new_dataset_cb:
            await callback(dataset)

    async def process_wunderground(
        self, data: dict[str, str | float]
    ) -> WeatherStation:
        """Process Wunderground data."""

        dfields = {
            f.metadata["arg"]: f
            for f in fields(WundergroundRawSensor)
            if "arg" in f.metadata
        }
        instance_data = {}
        for arg, field in dfields.items():
            if arg in data:
                instance_data[field.name] = field.type(data[arg])

        return WeatherStation.from_wunderground(WundergroundRawSensor(**instance_data))

    async def process_weathercloud(self, segments: list[str]) -> WeatherStation:
        """Process WeatherCloud data."""

        data = dict(zip(segments[::2], segments[1::2]))
        dfields = {
            f.metadata["arg"]: f
            for f in fields(WeathercloudRawSensor)
            if "arg" in f.metadata
        }
        instance_data = {
            field.name: field.type(data[arg])
            for arg, field in dfields.items()
            if arg in data
        }

        return WeatherStation.from_weathercloud(WeathercloudRawSensor(**instance_data))

    async def handler(self, request: web.BaseRequest) -> web.Response:
        """AIOHTTP handler for the API."""

        if request.method != "GET" or request.path is None:
            raise web.HTTPBadRequest()

        station_id: str = None
        dataset: WeatherStation = None
        sink: DataSink = None
        if request.path.endswith("/weatherstation/updateweatherstation.php"):
            dataset = await self.process_wunderground(request.query)
            station_id = dataset.station_id
            sink = DataSink.WUNDERGROUND
        elif "/v01/set" in request.path:
            dataset_path = request.path.split("/v01/set/", 1)[1]
            path_segments = dataset_path.split("/")
            dataset = await self.process_weathercloud(path_segments)
            station_id = dataset.station_id
            sink = DataSink.WEATHERCLOUD

        if station_id not in self.stations:
            _LOGGER.debug("Found new station: %s", station_id)
            self.stations.append(station_id)

        self.last_updates[station_id] = time.monotonic()
        dataset.update_time = self.last_updates[station_id]

        # The User-Agent is the only recognizable information we have aside from the IP
        # In case of the station at hand it just shows lwIP/2.1.2 of their IP stack
        user_agent = request.headers.get("User-Agent")
        if user_agent:
            dataset.station_sw_version = user_agent

        # Extract client IP from request just in case
        if "X-Real-IP" in request.headers:
            dataset.station_client_ip = request.headers["X-Real-IP"]
        else:
            dataset.station_client_ip = request.remote

        try:
            await self._new_dataset_cb(dataset)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.warning("CloudWeather new dataset callback error: %s", err)

        if self.proxy_enabled and sink is not None:
            try:
                response: web.Response = await self.proxy.forward(sink, request)
                _LOGGER.debug(
                    "CloudWeather proxy response[%d]: %s",
                    response.status,
                    await response.text(),
                )
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.warning("CloudWeather proxy error: %s", err)

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
