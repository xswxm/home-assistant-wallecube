from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .mqtt_client import WalleCubeMqttClient
from .const import DOMAIN, PLATFORMS

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    mqtt_client = WalleCubeMqttClient(hass, entry.data)
    await mqtt_client.connect()
    hass.data[DOMAIN][entry.entry_id] = mqtt_client
    
    async def send_magic_packet(call):
        """Handle the service call."""
        mac_address = call.data.get('mac_address')
        _LOGGER.debug(f'send_magic_packet request received. mac_address: {mac_address}.')
        try:
            res = await mqtt_client.send_magic_packet(mac_address)
            _LOGGER.debug(f'send_magic_packet request received. mqtt_client: {mqtt_client}.')
            if res:
                hass.bus.fire('wallecube.magic_packet_sent', {'mac': mac_address, 'status': 'success'})
            else:
                hass.bus.fire('wallecube.magic_packet_sent', {'mac': mac_address, 'status': 'error', 'message': 'mac address format not allowed'})
        except Exception as e:
            hass.bus.fire('wallecube.magic_packet_sent', {'mac': mac_address, 'status': 'error', 'message': str(e)})
    hass.services.async_register(DOMAIN, 'send_magic_packet', send_magic_packet)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop(entry.entry_id)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)