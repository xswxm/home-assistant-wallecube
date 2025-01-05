from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_DEVICE_ID, CONF_PASSWORD
import voluptuous as vol

import time
import asyncio
import paho.mqtt.client as mqtt
from .const import DOMAIN, MQTT_BROKER, MQTT_PORT

import logging
_LOGGER = logging.getLogger(__name__)

class WalleCubeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID]
            password = user_input[CONF_PASSWORD]
            
            result = await self._verify_mqtt_credentials(device_id, password)
            if result['success']:
                _LOGGER.debug("MQTT 验证成功")
                return self.async_create_entry(title=f"WalleCube {device_id}", data=user_input)
            else:
                return self.async_abort(reason=f'error_code: {result['error_code']}. {result['error_message']}')

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
        )

    def _get_schema(self):
        """Return the schema for the user input."""
        return vol.Schema({
            vol.Required(CONF_DEVICE_ID): str,
            vol.Required(CONF_PASSWORD): str,
        })

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return WalleCubeOptionsFlow(config_entry)

    async def _verify_mqtt_credentials(self, username, password, timeout = 30):
        result = {"success": False, "error_code": None, "error_message": ""}

        # 创建 asyncio 事件以等待回调完成
        event = asyncio.Event()

        # 定义回调函数
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                result["success"] = True
                result["error_message"] = "连接成功"
            else:
                result["error_code"] = rc
                result["error_message"] = f"连接失败，错误代码：{rc}（可能是用户名或密码错误）"
            event.set()  # 触发事件

        def on_connect_fail(client, userdata, rc):
            result["success"] = False
            result["error_code"] = rc
            result["error_message"] = f"连接失败，错误代码：{rc}"
            event.set()

        client_id = f'{username}_{int(time.time())}'
        client = mqtt.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.on_connect_fail = on_connect_fail

        client.loop_start()
        client.connect_async(MQTT_BROKER, MQTT_PORT)

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            result["success"] = False
            result["error_message"] = "连接超时，可能是网络问题或用户名/密码错误"

        client.loop_stop()
        client.disconnect()

        return result

class WalleCubeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init")
