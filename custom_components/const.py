from homeassistant.const import Platform
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfTime,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    PERCENTAGE,
    UnitOfTemperature,
)

from typing import Final
from enum import StrEnum

DOMAIN: Final = "wallecube"
DEVICE_MODEL: Final = "W120"
MANUFACTURER: Final = "WalleCube"
MQTT_BROKER: Final = "mqtt.wlups.com"
MQTT_PORT: Final = 1883
MQTT_KEEPALIVE: Final = 120

PLATFORMS: Final = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR
]

BINARY_SENSOR_TYPES = {
    "acOK": {
        "name": "AC适配器状态",
        "device_class": BinarySensorDeviceClass.POWER,
        "icon_on": 'mdi:power-plug',
        "icon_off": 'mdi:power-plug-off',
        "index": 1,
    },
    "charging": {
        "name": "充电状态",
        "device_class": BinarySensorDeviceClass.BATTERY_CHARGING,
        "icon_on": 'mdi:battery-charging',
        "icon_off": 'mdi:battery',
        "index": 1,
    }
}

SENSOR_TYPES = {
    "totalConsumption": {
        "name": "总用电数",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "icon": 'mdi:lightning-bolt-circle',
        "index": 1,
    },
    "leftSecs": {
        "name": "电池运行时间",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTime.MINUTES,
        "icon": 'mdi:battery-clock',
        "index": 1,
    },
    "batteryCapacity": {
        "name": "剩余电量",
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
        "icon": 'mdi:battery',
        "index": 1,
    },
    "currentOut": {
        "name": "输出电流",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": 'mdi:alpha-a-circle',
        "index": 1,
    },
    "voltageOut": {
        "name": "输出电压",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "icon": 'mdi:alpha-v-circle',
        "index": 1,
    },
    "pwrOut": {
        "name": "输出功率",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "icon": 'mdi:alpha-p-circle',
        "index": 1,
    },
    "chargingCurrent": {
        "name": "充电电流",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": 'mdi:current-dc',
        "index": 1,
    },
    "batteryVoltage": {
        "name": "电池电压",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "icon": 'mdi:alpha-v-circle',
        "index": 1,
    },
    "currentInput": {
        "name": "输入电流",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "icon": 'mdi:alpha-a-circle',
        "index": 1,
    },
    "voltageInput": {
        "name": "输入电压",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "icon": 'mdi:alpha-v-circle',
        "index": 1,
    },
    "batteryTemperature": {
        "name": "电池温度",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": 'mdi:alpha-a-circle',
        "index": 1,
    },
    "ipAddress": {
        "name": "IP地址",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": "",
        "icon": 'mdi:ip',
        "index": 1,
    },
}