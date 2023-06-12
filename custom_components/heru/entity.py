"""HERU Entity class"""
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NAME, VERSION

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
        name = self._attr_name.replace(" ", "_").lower()
        self._attr_unique_id = "_".join([name, str(self.idx["address"])])

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": self.config_entry.title,
            "model": VERSION,
            "manufacturer": NAME,
        }
