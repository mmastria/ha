"""
Support for AAG-SOLO

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

CONF_ATTRIBUTION = "AAG-SOLO by Lunatico"
CONF_UPDATE_INTERVAL = 'update_interval'
DEFAULT_NAME = 'AAG-Solo'
DEFAULT_PORT = 80

SENSOR_TYPES = {
    'datetime': ['Date', '', 'mdi:information-outline', 'dataGMTTime', None],
    'cwinfo': ['Release', '', 'mdi:information-outline', 'cwinfo', None],
    'clouds': ['Clouds', TEMP_CELSIUS, 'mdi:weather-cloudy', 'clouds', 2],
    'temperature': ['Temperature', TEMP_CELSIUS, 'mdi:thermometer', 'temp', 1],
    'wind': ['Wind', 'km/h', 'mdi:weather-wind', 'wind', 0],
    'gust': ['Gust', 'km/h', 'mdi:weather-wind', 'gust', 0],
    'rain': ['Rain', 'u', 'mdi:weather-rainy', 'rain', 0],
    'light': ['Light', 'u', 'mdi:weather-sunny', 'light', 0],
    'switch': ['Switch', '', 'mdi:power', 'switch', None],
    'safe': ['Safe', '', 'mdi:alert', 'safe', None],
    'humidity': ['Humidity', '%', 'mdi:water-percent', 'hum', 1],
    'dewpoint': ['Dewpoint', TEMP_CELSIUS, 'mdi:thermometer', 'dewp', 1],
    'cloudsclear' : ['Sky Clear', TEMP_CELSIUS, 'mdi:weather-cloudy', 'Clear', 0],
    'cloudscloudy' : ['Sky Cloudy', TEMP_CELSIUS, 'mdi:weather-cloudy', 'Cloudy', 0],
    'cloudsovercast' : ['Sky Overcast', TEMP_CELSIUS, 'mdi:weather-cloudy', 'Overcast', 0],
    'raindry' : ['Weather Dry', 'u', 'mdi:weather-rainy', 'Dry', 0],
    'rainwet' : ['Weather Wet', 'u', 'mdi:weather-rainy', 'Wet', 0],
    'rainrain' : ['Weather Rain', 'u', 'mdi:weather-rainy', 'Rain', 0],
    'lightdark' : ['Sky Dark', 'u', 'mdi:weather-sunny', 'Dark', 0],
    'lightlight' : ['Sky Light', 'u', 'mdi:weather-sunny', 'Light', 0],
    'lightverylight' : ['Sky Very Light', 'u', 'mdi:weather-sunny', 'VeryLight', 0]
}

SENSOR_STATE = {
    '0': 'off',
    '1': 'on'
}

"""
http://aagsolo.arua/cgi-bin/cgiLastData

dataGMTTime=2019/04/12 17:52:54
cwinfo=Serial: 1198, FW: 5.7
clouds=2.420000
temp=34.410000
wind=-1
gust=-1
rain=2624
light=0
switch=0
safe=0
hum=-1
dewp=100.000000

http://aagsolo.arua/cgi-bin/config.pl

Ver=21
Title=Mastria
Subtitle=AAG Cloudwatcher Solo
GraphCloudMin=
Clear=0
Cloudy=5
Overcast=30
GraphRainMax=2700
Dry=2000
Wet=1700
Rain=400
RHDry=
Normal=
Humid=
Calm=5
Windy=43.9
VeryWindy=998.9
GraphLightMax=59950
Dark=27000
Light=1000
VeryLight=0
Sw_Clouds=0
Sw_Wind=24.9
Sw_Rain=2400
Sw_Light=27000
Sw_Hum=
HRSensor=0
WindSensor=0
BrowserLangs=en-us
Now=2019/04/13 15:07:57
TimeOffset=-10800
"""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS, default=['temperature']):
        vol.All(cv.ensure_list, vol.Length(min=1), [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_UPDATE_INTERVAL, default=timedelta(seconds=60)): (
        vol.All(cv.time_period, cv.positive_timedelta)),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up AAG-Solo sensor."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    interval = config.get(CONF_UPDATE_INTERVAL)

    data = AagData(host, port, interval)
    try:
        data.update(no_throttle=True)
    except Exception:
        _LOGGER.exception("Failure while testing AAG-Solo status retrieval.")
        return False
    
    sensors = []
    for sensor_type in config[CONF_MONITORED_CONDITIONS]:
        sensors.append(AagSensor(name, sensor_type, data))

    add_devices(sensors, True)

class AagSensor(Entity):
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

class AagData(object):
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
            url = "http://{}:{}/cgi-bin/cgiLastData".format(self.host, self.port)
            response = requests.get(url, timeout=5)
            try:
                for sensor, value in [(pair.split("=")) for pair in response.text.splitlines()]:
                    if sensor in ['safe', 'switch']:
                        values[sensor] = SENSOR_STATE[value]
                    else:
                        values[sensor] = value
                url = "http://{}:{}/cgi-bin/config.pl".format(self.host, self.port)
                response = requests.get(url, timeout=5)
                try:
                    for sensor, value in [(pair.split("=")) for pair in response.text.splitlines()]:
                        values[sensor] = value
                    self.measurings = values
                except:
                    self.measurings = None
                    _LOGGER.error("Unable to retrieve config")
            except:
                self.measurings = None
                _LOGGER.error("Unable to retrieve data")
        except requests.exceptions.ConnectionError:
            self.measurings = None
            _LOGGER.error("Unable to connect to %s", url)

