"""DataUpdateCoordinator for OPM Status."""
from __future__ import annotations

from datetime import timedelta
import logging
import re
from typing import Any

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)


def _parse_dotnet_date(date_str: str | None) -> str | None:
    """Parse .NET JSON date format /Date(1234567890000)/ to ISO string."""
    if not date_str:
        return None
    match = re.search(r"/Date\((\d+)\)/", date_str)
    if match:
        from datetime import datetime, timezone

        timestamp_ms = int(match.group(1))
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return dt.isoformat()
    return date_str


class OPMStatusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch OPM operating status data."""

    def __init__(self, hass: HomeAssistant, scan_interval: int) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from OPM API."""
        try:
            async with async_timeout.timeout(30):
                resp = await self.session.get(API_URL)

            if resp.status != 200:
                raise UpdateFailed(
                    f"OPM API returned status {resp.status}"
                )

            data = await resp.json(content_type=None)

            # Normalize the data
            return {
                "id": data.get("Id"),
                "title": data.get("Title", ""),
                "location": data.get("Location", ""),
                "status_summary": data.get("StatusSummary", "Unknown"),
                "short_message": data.get("ShortStatusMessage", ""),
                "long_message": data.get("LongStatusMessage", ""),
                "extended_information": data.get("ExtendedInformation", ""),
                "applies_to": data.get("AppliesTo", ""),
                "icon": data.get("Icon", ""),
                "status_type": data.get("StatusType", ""),
                "status_type_guid": data.get("StatusTypeGuid", ""),
                "date_posted": _parse_dotnet_date(data.get("DateStatusPosted")),
                "url": data.get("Url", data.get("StatusWebPage", "")),
            }

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with OPM API: {err}") from err
        except TimeoutError as err:
            raise UpdateFailed("Timeout communicating with OPM API") from err
        except (KeyError, TypeError, ValueError) as err:
            raise UpdateFailed(f"Error parsing OPM API response: {err}") from err
