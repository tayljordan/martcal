from typing import Optional

from martcal import trig

from martcal.geocoord import GeoCoord
from martcal.port import Port
from martcal.port import PortFinder
from martcal.port import PortsList

class Route:
    def __init__(self, destination: Port, ports_list: PortsList) -> None:
        self.destination = destination
        self.distances = ports_list.distances(destination.name)
        self.finder = PortFinder(ports_list)

    def distance_from(self, geocoord: GeoCoord) -> Optional[float]:
        if not self.distances:
            return None

        ports = self.finder.nearest(geocoord)

        while True:
            try:
                nearest = ports.next()
                if self.has_route_from(nearest):
                    near_dest_distance = self.distances[nearest.name]
                    break
            except IndexError:
                return None

        loc_near_bearing = geocoord.bearing(nearest.geocoord)
        near_dest_bearing = nearest.geocoord.bearing(self.destination.geocoord)
        angular_distance = trig.angular_distance(near_dest_bearing, loc_near_bearing)

        loc_near_distance = geocoord.distance(nearest.geocoord)

        distance = trig.distance(
            loc_near_distance, near_dest_distance, angular_distance)

        return distance

    def has_route_from(self, port: Port) -> bool:
        if port.name not in self.distances:
            return False

        return self.distances[port.name] != 'Cannot find a route'
