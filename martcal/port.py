from typing import Optional

from typing import List
from typing import Dict

import errno
import os
import pickle

from operator import itemgetter
from pathlib import Path

from martcal.geocoord import GeoCoord

class Port:
    def __init__(self, name: str, geocoord: GeoCoord) -> None:
        self.name = name
        self.geocoord = geocoord

    def __str__(self) -> str:
        return '{} {}'.format(self.name, self.geocoord)

class Ports:
    def __init__(self, ports: List) -> None:
        self.ports = ports
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Port:
        try:
            return self.next()
        except IndexError:
            raise StopIteration

    def next(self) -> Port:
        port = self.ports[self.index][0]
        self.index += 1
        return port

    def current(self) -> Port:
        return self.ports[self.index][0]

class PortsList:
    FILE_PORTS = 'ports.p'
    FILE_DISTANCES = 'distances.p'

    def __init__(self, directory: str) -> None:
        path = Path(directory).resolve()
        if not path.is_dir():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(path))

        self.path = path
        self.ports_list = None

    def ports(self) -> Optional[Dict]:
        if self.ports_list is None:
            path = self.path.joinpath(PortsList.FILE_PORTS)
            with path.open('rb') as file:
                self.ports_list = pickle.load(file)

        return self.ports_list

    def distances(self, name: str) -> Optional[Dict]:
        path = self.path.joinpath(PortsList.FILE_DISTANCES)
        with path.open('rb') as file:
            ports = pickle.load(file)

        for port in ports:
            if port['properties']['city'] == name:
                return port['distances']

        return None

class PortFinder:
    ports = {}

    def __init__(self, ports_list: PortsList) -> None:
        PortFinder.ports = ports_list.ports()

    def nearest(self, geocoord: GeoCoord) -> Ports:
        nearest = []
        for name, coords in PortFinder.ports.items():
            port = Port(name, GeoCoord(coords['latitude'], coords['longitude']))
            distance = geocoord.distance(port.geocoord)
            nearest.append((port, distance))

        return Ports(sorted(nearest, key=itemgetter(1)))

    def from_name(self, name: str) -> Optional[Port]:
        if name not in self.ports:
            return None

        port = self.ports[name]
        return Port(name, GeoCoord(port['latitude'], port['longitude']))
