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
DEFAULT_PORT = 2001

# http://system-obs.arua/ror/status