from __future__ import annotations

from typing import List
from typing import Dict

import json
import os
import sys

from operator import itemgetter

from martcal.geocoord import GeoCoord

class Port:
    def __init__(self, name: str, location: GeoCoord):
        self.name = name
        self.location = location

    def __str__(self) -> str:
        return '{} {}'.format(self.name, self.location)

class PortFinder:
    ports = None

    def __init__(self):
        plist = PortsList()
        PortFinder.ports = plist.ports()

    def nearest(self, location: GeoCoord) -> Port:
        nearest = []
        for name, coords in PortFinder.ports.items():
            port = Port(name, GeoCoord(coords['latitude'], coords['longitude']))
            distance = location.distance(port.location)
            nearest.append((port, distance))

        return Ports(sorted(nearest, key=itemgetter(1)))

    def from_name(self, name: str) -> Port:
        if name not in self.ports:
            return None

        port = self.ports[name]
        return Port(name, GeoCoord(port['latitude'], port['longitude']))

class Ports:
    def __init__(self, ports: List):
        self.ports = ports
        self.index = 0

    def __iter__(self) -> Ports:
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
    DATA_DIR = os.path.dirname(sys.modules['__main__'].__file__) + '/../data/'
    FILE_PORTS = 'ports.json'
    FILE_DISTANCES = 'distances.json'

    def __init__(self):
        self.plist = None

    def ports(self) -> Dict:
        if not self.plist:
            filename = PortsList.DATA_DIR + PortsList.FILE_PORTS
            with open(filename) as file:
                self.plist = json.load(file)

        return self.plist

    def distances(self, name: str) -> Dict:
        filename = PortsList.DATA_DIR + PortsList.FILE_DISTANCES
        with open(filename) as file:
            ports = json.load(file)

        for port in ports:
            if port['properties']['city'] == name:
                return port['distances']

        return None
