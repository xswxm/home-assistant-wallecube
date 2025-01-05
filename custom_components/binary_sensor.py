from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import DOMAIN, DEVICE_MODEL, MANUFACTURER, BINARY_SENSOR_TYPES

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    sensors = []
    for sensor_type in BINARY_SENSOR_TYPES:
        sensors.append(WalleCubeBinarySensor(entry.data["device_id"], sensor_type, BINARY_SENSOR_TYPES[sensor_type]))
    async_add_entities(sensors)

class WalleCubeBinarySensor(BinarySensorEntity):
    def __init__(self, device_id, sensor_id, config):
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._config = config
        self._is_on = False
        self._attr_name = self._config['name']

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._device_id}_{self._sensor_id}"

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": DEVICE_MODEL,
            "manufacturer": MANUFACTURER,
            "sw_version": '0.0.1'
        }

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""

        return True

    @property
    def device_class(self) -> BinarySensorDeviceClass:
        """Return entity device class."""

        return self._config['device_class']

    @property
    def icon(self) -> str:
        """Set icon."""

        return self._config['icon_on'] if self._is_on else self._config['icon_off']

    @property
    def is_on(self):
        return self._is_on

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, self.unique_id, self.update_state
            )
        )

    def update_state(self, new_state):
        self._is_on = new_state
        self.hass.loop.call_soon_threadsafe(self.async_write_ha_state)
