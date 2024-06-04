"""Proxy for forwarding data to the CloudWeather APIs."""

from enum import Enum
from aiohttp import web
from dns_client.adapters.requests import DNSClientSession
import random
from urllib.parse import quote

import requests


class DataSink(Enum):
    """Data sinks for the CloudWeather API."""

    WUNDERGROUND = "wunderground"
    WEATHERCLOUD = "weathercloud"


class CloudWeatherProxy:
    """Proxy for forwarding data to the CloudWeather API."""

    def __init__(self, dns_servers: list[str]):
        self.session = DNSClientSession(host=random.choice(dns_servers))

    async def forward_wunderground(self, request: web.Request) -> requests.Response:
        """Forward Wunderground data to the API."""
        query_string = quote(request.query_string).replace("%20", "+")
        url = f"https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?{query_string}"
        return self.session.get(url)

    async def forward_weathercloud(self, request: web.Request) -> web.Response:
        """Forward WeatherCloud data to the API."""
        new_path = request.path[request.path.index("/v01/set") :]
        url = f"https://api.weathercloud.net{new_path}"
        return self.session.get(url)

    async def forward(self, sink: DataSink, request: web.Request) -> requests.Response:
        """Forward data to the CloudWeather API."""
        if sink == DataSink.WUNDERGROUND:
            return await self.forward_wunderground(request)
        if sink == DataSink.WEATHERCLOUD:
            return await self.forward_weathercloud(request)
