from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory

from .const import DOMAIN
from .entity import HisenseEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinators = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for coordinator in coordinators.values():
        if coordinator.client.is_ac:
            continue
        entities.extend(
            [
                HisenseDeviceTypeSensor(coordinator),
                HisenseDeviceIdSensor(coordinator),
                HisenseRawStatusSensor(coordinator),
            ]
        )
    async_add_entities(entities)


class HisenseDeviceTypeSensor(HisenseEntity, SensorEntity):
    _attr_translation_key = "device_type"
    _attr_icon = "mdi:devices"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator):
        super().__init__(coordinator, "device_type", "device_type")

    @property
    def native_value(self):
        return self.client.device_type_name or self.client.device_type


class HisenseDeviceIdSensor(HisenseEntity, SensorEntity):
    _attr_translation_key = "device_id"
    _attr_icon = "mdi:identifier"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator):
        super().__init__(coordinator, "device_id", "device_id")

    @property
    def native_value(self):
        return self.client.device_id


class HisenseRawStatusSensor(HisenseEntity, SensorEntity):
    _attr_translation_key = "raw_status"
    _attr_icon = "mdi:code-array"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator):
        super().__init__(coordinator, "raw_status", "raw_status")

    @property
    def native_value(self):
        raw_status_length = self.status.get("raw_status_length")
        if raw_status_length is None:
            return "unknown"
        return str(raw_status_length)

    @property
    def extra_state_attributes(self):
        return {
            "last_refresh_success": self.status.get("last_refresh_success"),
            "raw_status": self.status.get("raw_status"),
        }
