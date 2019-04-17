"""
Support for Roll Off Roof

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

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = "ROR RollOff Roof"
CONF_UPDATE_INTERVAL = 'update_interval'
DEFAULT_NAME = 'ROR'
DEFAULT_PORT = 80

SENSOR_TYPES = {
    'safe': ['ROR Safe', '', 'mdi:alert-octagon-outline', 'safe', None],
    'parked': ['ROR Parked', '', 'mdi:alert-octagon-outline', 'parked', None],
    'closed': ['ROR Closed', '', 'mdi:alert-octagon-outline', 'closed', None],
    'mount_parked': ['Mounts Parked', '', 'mdi:alert-octagon-outline', 'mount_parked', None],
    'open': ['ROR Open', '', 'mdi:alert-octagon-outline', 'open', None],
    'aagsafe': ['AAG Safe', '', 'mdi:alert-octagon-outline', 'aagsafe', None],
}

SENSOR_STATE = {
    True: 'on',
    False: "off"
}

"""

http://system-obs.arua/status

{
    "safe": false,
    "parked": true,
    "closed": true,
    "mount_parked": true,
    "open": false,
    "aagsafe": false
}

"""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS, default=['safe']):
        vol.All(cv.ensure_list, vol.Length(min=1), [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_UPDATE_INTERVAL, default=timedelta(seconds=60)): (
        vol.All(cv.time_period, cv.positive_timedelta)),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up RoR sensor."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    interval = config.get(CONF_UPDATE_INTERVAL)

    data = RorData(host, port, interval)
    try:
        data.update(no_throttle=True)
    except Exception:
        _LOGGER.exception("Failure while testing RoR status retrieval.")
        return False
    
    sensors = []
    for sensor_type in config[CONF_MONITORED_CONDITIONS]:
        sensors.append(RorSensor(name, sensor_type, data))

    add_devices(sensors, True)


class RorSensor(Entity):
    """Implementation of sensor."""

    def __init__(self, name, sensor_type, data):
        """Initialize the sensor."""
        self.client_name = name
        self.type = sensor_type
        self._name = SENSOR_TYPES[self.type][0]
        self._xref = SENSOR_TYPES[self.type][3]
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self._precision = SENSOR_TYPES[self.type][4]
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
    def is_on(self):
        """Return the state of the entity."""
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
                    self._sensor_value = round(float(self._data.measurings[self._xref]), self._precision)
                else:
                    self._sensor_value = int(round(float(self._data.measurings[self._xref]), self._precision))
            else:
                self._sensor_value = self._data.measurings[self._xref]


class RorData(object):
    """The Class for handling the data retrieval."""

    def __init__(self, host, port, interval):
        """Initialize the data object."""
        self.host = host
        self.port = port
        self.measurings = None
        self.update = Throttle(interval)(self._update)

    def _update(self):
        """Get the latest data"""
        values = {}
        try:
            url = "http://{}:{}/status".format(self.host, self.port)
            response = requests.get(url, timeout=5)
            rjson = response.json()
            try:
                for sensor in rjson:
                    values[sensor] = SENSOR_STATE[rjson[sensor]]
                self.measurings = values
            except:
                self.measurings = None
                _LOGGER.error("Unable to parse data")
        except requests.exceptions.ConnectionError:
            self.measurings = None
            _LOGGER.error("Unable to retrieve data or connect to %s", url)
