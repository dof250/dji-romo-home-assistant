"""Sensors for DJI Romo."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import ATTR_LAST_UPDATED, DOMAIN
from .coordinator import DjiRomoCoordinator
from .entity import DjiRomoCoordinatorEntity


@dataclass(frozen=True, kw_only=True)
class DjiRomoSensorDescription(SensorEntityDescription):
    """Entity description for Romo sensors."""

    value_fn: Callable[[DjiRomoCoordinator], Any]


SENSORS: tuple[DjiRomoSensorDescription, ...] = (
    DjiRomoSensorDescription(
        key="battery",
        name="Battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        value_fn=lambda coordinator: coordinator.data.battery_level,
    ),
    DjiRomoSensorDescription(
        key="status",
        name="Status",
        value_fn=lambda coordinator: coordinator.data.status_text,
    ),
    DjiRomoSensorDescription(
        key="last_update",
        name="Last Update",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.data.last_updated,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Romo sensors."""
    coordinator: DjiRomoCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(DjiRomoSensor(coordinator, description) for description in SENSORS)


class DjiRomoSensor(DjiRomoCoordinatorEntity, SensorEntity):
    """Coordinator-backed Romo sensor."""

    entity_description: DjiRomoSensorDescription

    def __init__(
        self,
        coordinator: DjiRomoCoordinator,
        description: DjiRomoSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.device_sn}_{description.key}"

    @property
    def native_value(self) -> Any:
        """Return the current sensor state."""
        return self.entity_description.value_fn(self.coordinator)
