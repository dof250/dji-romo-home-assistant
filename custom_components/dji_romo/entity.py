"""Shared entity helpers for DJI Romo."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_MODEL, DOMAIN
from .coordinator import DjiRomoCoordinator


class DjiRomoCoordinatorEntity(CoordinatorEntity[DjiRomoCoordinator]):
    """Base entity bound to the Romo coordinator."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: DjiRomoCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.device_sn)},
            manufacturer="DJI",
            model=coordinator.device_info_payload.get("product_name")
            or coordinator.device_info_payload.get("model")
            or "Romo",
            name=coordinator.device_name,
            serial_number=coordinator.device_sn,
            suggested_area=coordinator.device_info_payload.get("home_name"),
            configuration_url="https://home-api-vg.djigate.com/",
        )

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Expose a few raw metadata fields on all entities."""
        attrs: dict[str, str] = {}
        if model := self.coordinator.device_info_payload.get("model"):
            attrs[ATTR_MODEL] = str(model)
        return attrs
