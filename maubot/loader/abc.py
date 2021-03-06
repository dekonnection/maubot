# maubot - A plugin-based Matrix bot system.
# Copyright (C) 2018 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import TypeVar, Type, Dict, Set, TYPE_CHECKING
from abc import ABC, abstractmethod
import asyncio

from ..plugin_base import Plugin

if TYPE_CHECKING:
    from ..instance import PluginInstance

PluginClass = TypeVar("PluginClass", bound=Plugin)


class IDConflictError(Exception):
    pass


class PluginLoader(ABC):
    id_cache: Dict[str, 'PluginLoader'] = {}

    references: Set['PluginInstance']
    id: str
    version: str

    def __init__(self):
        self.references = set()

    @classmethod
    def find(cls, plugin_id: str) -> 'PluginLoader':
        return cls.id_cache[plugin_id]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "version": self.version,
            "instances": [instance.to_dict() for instance in self.references],
        }

    @property
    @abstractmethod
    def source(self) -> str:
        pass

    @abstractmethod
    async def read_file(self, path: str) -> bytes:
        pass

    async def stop_instances(self) -> None:
        await asyncio.gather(*[instance.stop() for instance
                               in self.references if instance.started])

    async def start_instances(self) -> None:
        await asyncio.gather(*[instance.start() for instance
                               in self.references if instance.enabled])

    @abstractmethod
    async def load(self) -> Type[PluginClass]:
        pass

    @abstractmethod
    async def reload(self) -> Type[PluginClass]:
        pass

    @abstractmethod
    async def unload(self) -> None:
        pass

    @abstractmethod
    async def delete(self) -> None:
        pass
