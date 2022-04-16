from geopy.geocoders import Nominatim
import pandas
import urllib
import json
from visualization import plot
import geopy.distance
import time
import math

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
        # Send OSRM request
        q = 'http://router.project-osrm.org/route/v1/car/' + str(self.__source[1]) + ',' + str(self.__source[0]) + \
            ';' + str(self.__destination[1]) + ',' + str(self.__destination[0]) + \
            '?alternatives=true&geometries=geojson&overview=full'

        req = urllib.request.Request(q)
        with urllib.request.urlopen(req) as response:
            routing_data = json.loads(response.read())

        # Read in model Data
        sensors = pandas.read_csv("90_sensors.csv")
        speeds = pandas.read_csv("test_result-compressed_90.csv", header=None, index_col=0)

        # Get Local Time
        t = time.localtime()
        current_time = time.strftime("%H.%M.%S", t)

        for path in routing_data['routes']:
            total = 0
            dist_total = 0
            closest = []
            start = path['geometry']['coordinates'][0]
            for cord in path['geometry']['coordinates'][1:]:
                # Find closest sensor to present location to get speed (within .001 of longitude and latitude)
                for index, latlon in sensors.iterrows():
                    case = float(latlon['latitude']) - 0.001 <= cord[1] and float(latlon['latitude']) + 0.001 >= cord[1] and float(latlon['longitude']) - 0.001 <= cord[0] and float(latlon['longitude']) + 0.001 >= cord[0]
                    if case:
                        closest = index # If no sensor in proximity continues at current speed
                        break
                
                # Recieve heading in degrees
                x = float(start[1]) - float(cord[1])
                y = float(start[0]) - float(cord[0])
                degrees_temp = math.atan2(x, y)/math.pi*180
                if degrees_temp < 0:
                    degrees = 360 + degrees_temp
                else:
                    degrees = degrees_temp                         

                # Retrieve assumed travelling speed
                if closest == []:
                    speed = 13.89 # Assume travelling speed of 50 km/h
                else:
                    hh, mm, ss = str(current_time).split('.')
                    temp_time = float(hh + '.' + mm)
                    loc_time = '{:.2f}'.format(round((0.05*round(float(temp_time)/0.05)), 2)) + '.00'
                    hh, mm, ss = loc_time.split('.')
                    temp_change = int(hh) * 3600 + int(mm) * 60 + int(ss)
                    loc_time = str(time.strftime("%H.%M.%S", time.gmtime(temp_change)))
                    loc_time = loc_time.replace('.',':')
                    if degrees >= 0 and degrees < 180:
                        speed = speeds.loc[loc_time,closest*2+1]
                    else:
                        speed = speeds.loc[loc_time,closest*2]
                
                # Get distance between starting coordinate and next coordinate
                cord1 = str(start[1]) + ',' + str(start[0])
                cord2 = str(cord[1]) + ',' + str(cord[0])
                dist = geopy.distance.distance(cord1, cord2).m
                dist_total += dist
                start = cord

                # Determine time to travel that distance
                change = dist/abs(float(speed))
                total += change # Total travel time

                # Advance current_time to time at coordinate
                hh, mm, ss = current_time.split('.')
                temp_change = int(hh) * 3600 + int(mm) * 60 + int(ss)
                current_time = time.strftime("%H.%M.%S", time.gmtime(temp_change + change))
            
            if closest != []:
                path['distance'] = dist_total
                path['duration'] = total

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