from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import DOMAIN, DEVICE_MODEL, MANUFACTURER, SENSOR_TYPES

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    sensors = []
    for sensor_type in SENSOR_TYPES:
        sensors.append(WalleCubeSensor(entry.data["device_id"], sensor_type, SENSOR_TYPES[sensor_type]))
    async_add_entities(sensors)

class WalleCubeSensor(SensorEntity):
    def __init__(self, device_id, sensor_id, config):
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._config = config
        self._state = None
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
    def state_class(self) -> SensorStateClass:
        """Return the type of state class."""

        return self._config['state_class']

    @property
    def device_class(self) -> SensorDeviceClass:
        """Return entity device class."""

        return self._config['device_class']

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the native unit."""

        return self._config['unit']

    @property
    def icon(self) -> str:
        """Set icon."""
        if self._sensor_id == 'batteryCapacity':
            if self._state == None:
                return f"{self._config['icon']}-unknown"
            battery_life = max(10, min(int(round(self._state / 10) * 10), 100))
            if battery_life >= 100:
                return self._config['icon']
            return f"{self._config['icon']}-{battery_life}"
        return self._config['icon']

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, self.unique_id, self.update_state
            )
        )

    def update_state(self, new_state):
        self._state = new_state
        self.hass.loop.call_soon_threadsafe(self.async_write_ha_state)
