from geopy.geocoders import Nominatim
import urllib
import json
from visualization import plot

geoloc = Nominatim(user_agent='Rec')


class Path:
    __coordinates = None
    __dist = None
    __time = None

    def __init__(self, coordinates, distance, time):
        self.__coordinates = coordinates
        self.__dist = distance
        self.__time = time

    def getDistance(self):
        return self.__dist

    def getDuration(self):
        return self.__time

    def getCoordinates(self):
        return self.__coordinates


class Paths:
    __source = None
    __destination = None
    __paths = None

    def __init__(self, source:list, destination:list):
        self.__source = self.get_coordinates(source)
        self.__destination = self.get_coordinates(destination)
        self.__paths = []
        self.set_paths()

    def get_coordinates(self, address):
        location = geoloc.geocode(address)
        return [location.latitude, location.longitude]

    def set_paths(self):
        q = 'http://router.project-osrm.org/route/v1/car/' + str(self.__source[1]) + ',' + str(self.__source[0]) + \
            ';' + str(self.__destination[1]) + ',' + str(self.__destination[0]) + \
            '?alternatives=true&geometries=geojson&overview=full'

        req = urllib.request.Request(q)
        with urllib.request.urlopen(req) as response:
            routing_data = json.loads(response.read())

        for i in range(len(routing_data['routes'])):
            dist = (round(routing_data['routes'][i]['distance'] / 1000.0, 5))    # m -> Km
            dur = (round(routing_data['routes'][i]['duration'] / 60.0, 5))  # seconds -> minutes
            routes = routing_data['routes'][i]['geometry']['coordinates']
            routes = [[x[1],x[0]] for x in routes]

            self.__paths.append(Path(routes, dist, dur))

    def getPaths(self):
        return self.__paths

    def plot(self):
        plot(self.__source, self.__destination, self.__paths)