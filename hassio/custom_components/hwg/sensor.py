"""
Support for HWG-STE.

"""

import logging
import voluptuous as vol
import requests
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_PORT, TEMP_CELSIUS, CONF_MONITORED_CONDITIONS, ATTR_ATTRIBUTION)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

REQUIREMENTS = ['xmltodict==0.11.0']

_LOGGER = logging.getLogger(__name__)


CONF_ATTRIBUTION = "HWg-STE temperature and humidity sensor"
CONF_UPDATE_INTERVAL = 'update_interval'
DEFAULT_NAME = 'HWg-STE'
DEFAULT_PORT = 80

SENSOR_TYPES = {
    'temperature': ['Ambient Temperature', TEMP_CELSIUS, 'mdi:thermometer', 1],
    'humidity': ['Ambient Humidity', '%', 'mdi:water-percent', 1],
    'temperature_status': ['Temperature Status', '', 'mdi:alert-outline', None],
    'humidity_status': ['Humidity Status', '', 'mdi:alert-outline', None],
    'temperature_normal': ['Temperature Normal', '', 'mdi:information-outline', None],
    'humidity_normal': ['Humidity Normal', '', 'mdi:information-outline', None],
}

SENSOR_STATE = {
    '0': ['Invalid', None],
    '1': ['Normal', True],
    '2': ['OutOfRangeLo', False],
    '3': ['OutOfRangeHi', False],
    '4': ['AlarmLo', False],
    '5': ['AlarmHi', False]
}

"""
<?xml version="1.0" encoding="utf-8"?>
<val:Root xmlns:val="http://www.hw-group.com/XMLSchema/ste/values.xsd">
<Agent>
    <Version>2.1.1</Version>
    <XmlVer>1.01</XmlVer>
    <DeviceName>HWg-STE</DeviceName>
    <Model>33</Model>
    <vendor_id>0</vendor_id>
    <MAC>00:0A:59:01:D5:0E</MAC>
    <IP>192.168.0.203</IP>
    <MASK>255.255.255.0</MASK>
    <sys_name>HWg-STE</sys_name>
    <sys_location></sys_location>
    <sys_contact>HWg-STE:For more information try http://www.hw-group.com</sys_contact>
</Agent>
<SenSet>
    <Entry>
        <ID>215</ID>
        <Name>Temperatura</Name>
        <Units>C</Units>
        <Value>31.3</Value>
        <Min>5.0</Min>
        <Max>35.0</Max>
        <Hyst>0.0</Hyst>
        <EmailSMS>0</EmailSMS>
        <State>1</State>
    </Entry>
    <Entry>
        <ID>216</ID>
        <Name>Umidade</Name>
        <Units>%RH</Units>
        <Value>57.4</Value>
        <Min>40.0</Min>
        <Max>60.0</Max>
        <Hyst>0.0</Hyst>
        <EmailSMS>0</EmailSMS>
        <State>1</State>
    </Entry>
</SenSet>
</val:Root>
"""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS, default=['temperature', 'humidity']):
        vol.All(cv.ensure_list, vol.Length(min=1), [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_UPDATE_INTERVAL, default=timedelta(seconds=60)): (
        vol.All(cv.time_period, cv.positive_timedelta)),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up HWg-STE sensor."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    interval = config.get(CONF_UPDATE_INTERVAL)

    data = HWgData(host, port, interval)
    try:
        data.update(no_throttle=True)
    except Exception:
        _LOGGER.exception("Failure while testing HWg-STE status retrieval.")
        return False
    
    sensors = []
    for sensor_type in config[CONF_MONITORED_CONDITIONS]:
        sensors.append(HWgSensor(name, sensor_type, data))

    add_devices(sensors, True)


class HWgSensor(Entity):
    """Implementation of sensor."""

    def __init__(self, name, sensor_type, data):
        """Initialize the sensor."""
        self.client_name = name
        self.type = sensor_type
        self._name = SENSOR_TYPES[self.type][0]
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self._precision = SENSOR_TYPES[self.type][3]
        self._data = data
        self._sensor_value = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self.client_name, self._name)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._sensor_value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
        }

    def update(self):
        """Get the latest data and update the states."""
        self._data.update()
        if self._data.measurings is not None:
            if self._precision is not None:
                if self._precision > 0:
                    self._sensor_value = round(float(self._data.measurings[self.type]), self._precision)
                else:
                    self._sensor_value = int(round(float(self._data.measurings[self.type]), self._precision))
            else:
                self._sensor_value = self._data.measurings[self.type]


class HWgData(object):
    """The Class for handling the data retrieval."""

    def __init__(self, host, port, interval):
        """Initialize the data object."""
        self.host = host
        self.port = port
        self.measurings = None
        self.update = Throttle(interval)(self._update)

    def _update(self):
        """Get the latest data"""
        import xmltodict
        values = {}
        try:
            url = "http://{}:{}/values.xml".format(self.host, self.port)
            response = requests.get(url, timeout=5)
            try:
                sensors = xmltodict.parse(response.text)['val:Root']['SenSet']['Entry']
                for sensor in sensors:
                    if sensor.get('ID') == '215':
                        values['temperature'] = float(sensor.get('Value'))
                        values['temperature_status'] = SENSOR_STATE[sensor.get('State')][0]
                        values['temperature_normal'] = SENSOR_STATE[sensor.get('State')][1]
                        continue
                    if sensor.get('ID') == '216':
                        values['humidity'] = float(sensor.get('Value'))
                        values['humidity_status'] = SENSOR_STATE[sensor.get('State')][0]
                        values['humidity_normal'] = SENSOR_STATE[sensor.get('State')][1]
                if values['temperature'] > -20 and values['temperature'] < 80 and values['humidity'] > 0 and values['humidity'] <= 100:
                    self.measurings = values
                else:
                    self.measurings = None
                    _LOGGER.error("Values out of range")
            except AttributeError:
                self.measurings = None
                _LOGGER.error("Unable to retrieve data")
        except requests.exceptions.ConnectionError:
            self.measurings = None
            _LOGGER.error("Unable to connect to %s", url)

