from martcal.geocoord import GeoCoord
from martcal.port import PortFinder

from martcal.route import Route

port_finder = PortFinder()

ship_location = GeoCoord(44.980, 13.008)
destination = port_finder.from_name('KOPER')
random_point = GeoCoord(41.8798, 16.2653)

print('Ship location:', ship_location)
print('Destination port:', destination)
print('Random point:', random_point)
print()

route = Route(destination)
distance = route.distance_from(ship_location)
print('Distance from ship location to destination port:', distance)

distance = ship_location.distance(random_point)
print('Distance from ship location to random point via great-circle:', distance)

print()
print('>> 10 nearest ports to ship location:')
ports = port_finder.nearest(ship_location)
i = 0
while i < 10:
    try:
        print(ports.next())
        i += 1
    except IndexError:
        print('All ports printed')
        break

print()
print('>> All ports sorted by distance:')
for port in port_finder.nearest(ship_location):
    print(port)
