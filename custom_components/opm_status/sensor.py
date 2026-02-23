"""Sensor platform for OPM Status."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_APPLIES_TO,
    ATTR_DATE_POSTED,
    ATTR_EXTENDED_INFO,
    ATTR_ICON,
    ATTR_LOCATION,
    ATTR_LONG_MESSAGE,
    ATTR_SHORT_MESSAGE,
    ATTR_STATUS_SUMMARY,
    ATTR_STATUS_TYPE,
    ATTR_TITLE,
    ATTR_URL,
    DOMAIN,
)
from .coordinator import OPMStatusCoordinator

# Map OPM icon values to Material Design Icons
ICON_MAP = {
    "Open": "mdi:door-open",
    "Closed": "mdi:door-closed",
    "Alert": "mdi:alert",
    "Announcement": "mdi:bullhorn",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OPM Status sensor from a config entry."""
    coordinator: OPMStatusCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            OPMStatusSensor(coordinator, entry),
            OPMShortMessageSensor(coordinator, entry),
        ]
    )


class OPMStatusSensor(CoordinatorEntity[OPMStatusCoordinator], SensorEntity):
    """Sensor showing the current OPM operating status."""

    _attr_has_entity_name = True
    _attr_name = "Operating Status"

    def __init__(
        self, coordinator: OPMStatusCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "OPM Federal Operating Status",
            "manufacturer": "U.S. Office of Personnel Management",
            "model": "Operating Status API",
            "entry_type": "service",
            "configuration_url": "https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/",
        }

    @property
    def native_value(self) -> str | None:
        """Return the current operating status."""
        if self.coordinator.data:
            return self.coordinator.data.get("status_summary")
        return None

    @property
    def icon(self) -> str:
        """Return the icon based on status."""
        if self.coordinator.data:
            opm_icon = self.coordinator.data.get("icon", "")
            return ICON_MAP.get(opm_icon, "mdi:office-building")
        return "mdi:office-building"

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}
        data = self.coordinator.data
        return {
            ATTR_TITLE: data.get("title"),
            ATTR_LOCATION: data.get("location"),
            ATTR_STATUS_SUMMARY: data.get("status_summary"),
            ATTR_SHORT_MESSAGE: data.get("short_message"),
            ATTR_LONG_MESSAGE: data.get("long_message"),
            ATTR_EXTENDED_INFO: data.get("extended_information"),
            ATTR_APPLIES_TO: data.get("applies_to"),
            ATTR_ICON: data.get("icon"),
            ATTR_STATUS_TYPE: data.get("status_type"),
            ATTR_DATE_POSTED: data.get("date_posted"),
            ATTR_URL: data.get("url"),
        }


class OPMShortMessageSensor(CoordinatorEntity[OPMStatusCoordinator], SensorEntity):
    """Sensor showing the short OPM status message."""

    _attr_has_entity_name = True
    _attr_name = "Status Message"

    def __init__(
        self, coordinator: OPMStatusCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_short_message"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "OPM Federal Operating Status",
            "manufacturer": "U.S. Office of Personnel Management",
            "model": "Operating Status API",
            "entry_type": "service",
            "configuration_url": "https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/",
        }

    @property
    def native_value(self) -> str | None:
        """Return the short status message."""
        if self.coordinator.data:
            return self.coordinator.data.get("short_message")
        return None

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:message-text"
