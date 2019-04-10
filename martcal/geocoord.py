import math

from geopy.distance import great_circle

class GeoCoord:
    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return '({}, {})'.format(self.latitude, self.longitude)

    def distance(self, location) -> float:
        start = (self.latitude, self.longitude)
        end = (location.latitude, location.longitude)

        return great_circle(start, end).miles

    def bearing(self, location) -> float:
        # https://gist.github.com/jeromer/2005586

        start_lat = math.radians(self.latitude)
        end_lat = math.radians(location.latitude)

        diff_long = math.radians(location.longitude - self.longitude)

        x = math.sin(diff_long) * math.cos(end_lat)
        y = math.cos(start_lat) * math.sin(end_lat) - (math.sin(start_lat)
                * math.cos(end_lat) * math.cos(diff_long))

        bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        return (math.degrees(bearing) + 360) % 360
