from typing import Optional

from martcal import trig

from martcal.geocoord import GeoCoord
from martcal.port import Port
from martcal.port import PortFinder
from martcal.port import PortsList

class Route:
    def __init__(self, destination: Port):
        plist = PortsList()
        self.distances = plist.distances(destination.name)
        self.destination = destination

    def distance_from(self, location: GeoCoord) -> Optional[float]:
        if not self.distances:
            return None

        finder = PortFinder()
        ports = finder.nearest(location)

        while True:
            try:
                nearest = ports.next()
                if self.has_route_from(nearest):
                    near_dest_distance = self.distances[nearest.name]
                    break
            except IndexError:
                return None

        loc_near_bearing = location.bearing(nearest.location)
        near_dest_bearing = nearest.location.bearing(self.destination.location)

        loc_near_distance = location.distance(nearest.location)
        loc_dest_distance = location.distance(self.destination.location)

        angular_distance = trig.angular_distance(near_dest_bearing, loc_near_bearing)

        distance = trig.distance(
            loc_near_distance, near_dest_distance, angular_distance)

        return distance

    def has_route_from(self, port: Port) -> bool:
        if port.name not in self.distances:
            return False

        return self.distances[port.name] != 'Cannot find a route'
