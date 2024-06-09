# aiocloudweather

[![PyPI Release][pypi]][pypi-page]
[![GitHub Activity][commits-shield]][commits]
[![Project Maintenance][maintenance-shield]][maintainer]
[![Mastodon][mastodon]][mastodon_profile]


A simple Python library for parsing Wunderground and Weathercloud update requests, based on aioecowitt for Ecowitt weather stations.

## Installation

You can install `aiocloudweather` from PyPI using pip:

```shell
pip install aiocloudweather
```

## Usage

```python
import asyncio
import aiocloudweather

async def dataset_handler(station: WeatherStation):
    # Your code here


app = CloudWeatherListener()
app.new_dataset_cb.append(dataset_handler)

await app.start()
while True:
    await asyncio.sleep(100000)

```

## Contributing

Contributions are welcome! Please also check the [Cloud Weather Proxy][cloudweatherproxy] project which uses this library to enable the weather stations in HomeAssistant.



[pypi]: https://img.shields.io/pypi/v/aiocloudweather
[pypi-page]: https://pypi.org/project/aiocloudweather/
[commits-shield]: https://img.shields.io/github/commit-activity/y/lhw/cloudweatherproxy.svg
[commits]: https://github.com/lhw/cloudweatherproxy/commits/main
[maintenance-shield]: https://img.shields.io/badge/maintainer-Lennart%20Weller%20%40lhw-blue.svg
[maintainer]: https://github.com/lhw
[mastodon]: https://img.shields.io/mastodon/follow/000048422?domain=https%3A%2F%2Fchaos.social
[mastodon_profile]: https://chaos.social/@lhw
[cloudweatherproxy]: https://github.com/lhw/cloudweatherproxy