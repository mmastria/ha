"""
Support for NHS-UPS.

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

CONF_ATTRIBUTION = "NHS UPS Premium Online 3000VA 14.25"
CONF_UPDATE_INTERVAL = 'update_interval'
DEFAULT_NAME = 'NHS-UPS'
DEFAULT_PORT = 2001

SENSOR_TYPES = {
    'nominal_input_voltage': ['Tensao Entrada Nominal', 'V', 'mdi:current-ac', 'tensao_entrada_nominal', 1],
    'nominal_output_voltage': ['Tensao Saida Nominal', 'V', 'mdi:current-ac', 'tensao_saida_nominal', 1],
    'batteries': ['Quantidade Baterias', '', 'mdi:car-battery', 'quantidade_baterias', 0],
    'nominal_charger_current': ['Corrente Nominal Carregador', 'i', 'mdi:flash', 'corrente_nominal_carregador', 0],
    'read_charger_current': ['Mede Corrente Carregador', '', 'mdi:comment-question-outline', 'mede_corrente_carregador', None],
    'read_temperature': ['Mede Temperatura', '', 'mdi:comment-question-outline', 'mede_temperatura', None],
    'input_voltage': ['Tensao Entrada', 'V', 'mdi:current-ac', 'tensao_entrada', 1],
    'output_voltage': ['Tensao Saida', 'V', 'mdi:current-ac', 'tensao_saida', 1],
    'load': ['Carga', '%', 'mdi:gauge-full', 'carga', 1],
    'battery_voltage': ['Tensao Bateria', 'V', 'mdi:batty-chaging-outline', 'tensao_bateria', 1],
    'temperature': ['Temperatura', TEMP_CELSIUS, 'mdi:oil-tempereture', 'temperatura', 1],
    'chager_current': ['Corrente Carregador', 'i', 'mdi:flash', 'corrente_carregador', 1],
    'status': ['Status', '', 'mdi:battery-alert', 'status', None],
    'source': ['Source', '', 'mdi:battery-alert', 'source', None]
}

SENSOR_STATE = {
    'ok': ['AC Source', "on"],
    'nok': ['On Battery', "off"]
}

"""
{
    "evento": {
        "tensao_entrada_nominal": 120,
        "tensao_saida_nominal": 120,
        "quantidade_baterias": 10,
        "corrente_nominal_carregador": 720,
        "mede_corrente_carregador": "não",
        "mede_temperatura": "sim",
        "tensao_entrada": 125.8,
        "tensao_saida": 120,
        "carga": 5,
        "tensao_bateria": 139,
        "temperatura": 35,
        "corrente_carregador": 0
    },
    "status": "ok"
}
"""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS, default=['load','status']):
        vol.All(cv.ensure_list, vol.Length(min=1), [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_UPDATE_INTERVAL, default=timedelta(seconds=60)): (
        vol.All(cv.time_period, cv.positive_timedelta)),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up NHS-UPS sensor."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    interval = config.get(CONF_UPDATE_INTERVAL)

    data = NhsData(host, port, interval)
    try:
        data.update(no_throttle=True)
    except Exception:
        _LOGGER.exception("Failure while testing NHS-UPS status retrieval.")
        return False
    
    sensors = []
    for sensor_type in config[CONF_MONITORED_CONDITIONS]:
        sensors.append(NhsSensor(name, sensor_type, data))

    add_devices(sensors, True)


class NhsSensor(Entity):
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


class NhsData(object):
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
            url = "http://{}:{}/dados_graficos_gauge".format(self.host, self.port)
            response = requests.get(url, timeout=5)
            rjson = response.json()
            try:
                for item in rjson:
                    if item == 'status':
                        values['source'] = SENSOR_STATE[rjson[item]][0]
                        values['status'] = SENSOR_STATE[rjson[item]][1]
                        continue
                    if item == 'evento':
                        for sensor in rjson[item]:
                            values[sensor] = rjson[item][sensor]
                self.measurings = values
            except:
                self.measurings = None
                _LOGGER.error("Unable to parse data")
        except requests.exceptions.ConnectionError:
            self.measurings = None
            _LOGGER.error("Unable to retrieve data or connect to %s", url)
