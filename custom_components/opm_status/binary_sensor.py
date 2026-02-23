"""Binary sensor platform for OPM Status."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import OPMStatusCoordinator

DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, DOMAIN)},
    name="OPM Federal Operating Status",
    manufacturer="U.S. Office of Personnel Management",
    model="Operating Status API",
    entry_type=DeviceEntryType.SERVICE,
    configuration_url="https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OPM binary sensor from a config entry."""
    coordinator: OPMStatusCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([OPMOpenBinarySensor(coordinator, entry)])


class OPMOpenBinarySensor(
    CoordinatorEntity[OPMStatusCoordinator], BinarySensorEntity
):
    """Binary sensor that is ON when federal offices are open."""

    _attr_has_entity_name = True
    _attr_name = "Federal Offices Open"
    _attr_device_class = BinarySensorDeviceClass.OPENING

    def __init__(
        self, coordinator: OPMStatusCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_open"
        self._attr_device_info = DEVICE_INFO

    @property
    def is_on(self) -> bool | None:
        """Return True if federal offices are open."""
        if not self.coordinator.data:
            return None
        status = self.coordinator.data.get("status_summary", "")
        # Consider "open" if the status summary starts with "Open"
        return status.lower().startswith("open")

    @property
    def icon(self) -> str:
        """Return the icon."""
        if self.is_on:
            return "mdi:door-open"
        return "mdi:door-closed"

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}
        return {
            "status_summary": self.coordinator.data.get("status_summary"),
            "applies_to": self.coordinator.data.get("applies_to"),
        }
