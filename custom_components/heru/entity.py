"""HERU Entity class"""
import logging
from custom_components.heru.helpers.general import get_parameter
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import CONF_HOST_NAME, DOMAIN, NAME, VERSION

_LOGGER = logging.getLogger(__name__)


class HeruEntity(CoordinatorEntity, Entity):
    """Entity class."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.idx = idx

        self._attr_name = self.idx["name"]
        self._attr_icon = self.idx["icon"]

        ip = get_parameter(config_entry, CONF_HOST_NAME).replace(".", "")
        modbus_address = str(self.idx["modbus_address"])
        self._attr_unique_id = f"{ip}_{modbus_address}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": self.config_entry.title,
            "model": VERSION,
            "manufacturer": NAME,
        }
