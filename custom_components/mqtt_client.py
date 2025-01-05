import time
import paho.mqtt.client as mqtt
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from .const import DOMAIN, MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE

import re
import logging
import asyncio
_LOGGER = logging.getLogger(__name__)

class WalleCubeMqttClient:
    def __init__(self, hass: HomeAssistant, config):
        self.hass = hass
        self.device_id = config["device_id"]
        self.password = config["password"]
        self.client = None
        self.topic_up = f"ups/up/{self.device_id}"
        self.topic_dn = f"ups/dn/{self.device_id}"
        self.initialize()

    def initialize(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

        client_id = f'{self.device_id}_{int(time.time())}'
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(self.device_id, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    async def connect(self):
        await self.hass.async_add_executor_job(self.client.connect, MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        self.client.loop_start()

    async def disconnect(self):
        self.client.loop_stop()
        await self.hass.async_add_executor_job(self.client.disconnect)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            _LOGGER.info("Connected to MQTT Broker")
            client.subscribe(self.topic_up)
        else:
            _LOGGER.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        _LOGGER.warning("Disconnected from MQTT Broker")
        if rc != 0:
            _LOGGER.info("Attempting to reconnect in 5 seconds...")
            self.hass.loop.create_task(self._async_reconnect())

    async def _async_reconnect(self):
        await asyncio.sleep(5)
        self.initialize()
        await self.connect()

    def on_message(self, client, userdata, message):
        if message.topic != self.topic_up:
            _LOGGER.debug(f'MQTT Receviced: {message}')
            return
        _p = message.payload
        _LOGGER.debug(f'MQTT Payload: {_p.hex()}')
        data = {}
        def convert2int(byte_data):
            return int.from_bytes(byte_data, byteorder='big')
        if _p[1] == 0x01:
            # High and low swaps
            p = _p[::-1]
            data['acOK'] = p[0] in [0x04, 0x05]
            data['charging'] = p[1] == 0x81
            data['totalConsumption'] = convert2int(p[2:6]) / 1000000 # kwh
            data['leftSecs'] = convert2int(p[6:8]) / 60 # min
            data['batteryCapacity'] = convert2int(p[8:10]) / 10 # %
            data['currentOut'] = convert2int(p[10:12]) / 1000 # A
            data['voltageOut'] = convert2int(p[12:14]) / 1000 # V
            data['pwrOut'] = data['voltageOut'] * data['currentOut'] # W
            if data['charging']:
                data['chargingCurrent'] = convert2int(p[14:16]) / 1000
            elif p[23] not in [0x01, 0x02]:
                data['chargingCurrent'] = -convert2int(p[14:16]) / 1000
            data['batteryVoltage'] = convert2int(p[16:18]) / 1000 # V
            data['currentInput'] = convert2int(p[18:20]) / 1000 # A
            data['voltageInput'] = convert2int(p[20:22]) / 1000 # V
            data['batteryTemperature'] = int(p[22]) # ℃
        # update ip address
        elif _p[1] == 0x02:
            data['ipAddress'] = f'{int(_p[12])}.{int(_p[13])}.{int(_p[14])}.{int(_p[7])}'

        _LOGGER.debug(f'MQTT Payload Decryped: {data}')

        for sensor_name, sensor_value in data.items():
            self.hass.loop.call_soon_threadsafe(
                async_dispatcher_send,
                self.hass,
                f"{DOMAIN}_{self.device_id}_{sensor_name}",
                sensor_value
            )

    def publish(self, topic, msg):
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            _LOGGER.debug(f"Publish `{msg}` to `{topic}` topic")
        else:
            _LOGGER.debug(f"Failed to send message to topic {topic}")

    def send_magic_packet(self, mac_address):
        # varify mac_address
        pattern = r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$'
        if bool(re.match(pattern, mac_address)):
            _LOGGER.debug(f'MQTT Client: Ready to send_magic_packet to {mac_address}.')
            mac_address = '5103000600' + mac_address.replace(":", "").upper()
            self.publish(self.topic_dn, bytes.fromhex(mac_address))
            return True
        _LOGGER.debug(f'MQTT Client: Mac address {mac_address} format not allowed.')
        return False
