"""Run local Test server."""

from __future__ import annotations

import asyncio
from dataclasses import Field, fields
import logging
import sys
from types import NoneType

from aiocloudweather import CloudWeatherListener, WeatherStation
from aiocloudweather.sensor import Sensor

_LOGGER = logging.getLogger(__name__)


def usage():
    """Print usage of the CLI."""
    print(f"Usage: {sys.argv[0]} port")


async def my_handler(station: WeatherStation) -> None:
    """Callback handler for printing data."""

    for sensor in fields(station):
        if not sensor.type == Sensor:
            continue
        value: Field[Sensor] = getattr(station, sensor.name)
        if value is None:
            continue

        print(f"{sensor.name}: {value.metric} ({value.metric_unit})")
        print(f"{sensor.name}: {value.imperial} ({value.imperial_unit})")
        print()

    # print(f"{str(station)}")


async def run_server(ecowitt_ws: CloudWeatherListener) -> None:
    """Run server in endless mode."""
    await ecowitt_ws.start()
    while True:
        await asyncio.sleep(100000)


def main() -> None:
    """Run main."""
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    print(f"Firing up webserver to listen on port {sys.argv[1]}")
    cloudweather_server = CloudWeatherListener(port=sys.argv[1])

    cloudweather_server.new_dataset_cb.append(my_handler)
    try:
        asyncio.run(run_server(cloudweather_server))
    except Exception as err:  # pylint: disable=broad-except
        print(str(err))
    print("Exiting")


if __name__ == "__main__":
    main()
