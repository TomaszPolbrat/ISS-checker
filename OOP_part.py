import requests     # imports request library
import datetime     # imports datetime library


class IssLocator:       # idea of this class is to locate ISS position, compare it to user location and check if
    # atmospheric conditions allows user to see ISS (is it night?, is it cloudy?)

    def __init__(self):
        self.iss = requests.get(url="http://api.open-notify.org/iss-now.json")      # gets ISS location API
        self.iss_data = self.iss.json()["iss_position"]     # ISS data in json format
        self.iss_lon = float(self.iss_data["longitude"])        # ISS longitude data
        self.iss_lat = float(self.iss_data["latitude"])     # ISS latitude data
        self.my_lat = 1       # users latitude _ manually inserted
        self.my_lon = 1       # users longitude _ manually inserted
        self.is_night_now = None    # data placeholder
        self.my_email = "YYY@gmail.com"  # user Email address
        self.password = "password"  # user Email password
        self.password_app = "app_password"  # Gmail application password _ necessary for application functionality
        self.parameters = {
    "lat": self.my_lat,
    "lng": self.my_lon,
    "formatted": 0,
    }       # parameters dictionary for day and hour API, it gets data in this format, it uses Users position

    def clouds(self):       # API atmospheric information
        weather = requests.get(
            "http://api.weatherapi.com/v1/current.json?key=codefromwebside&q=City&aqi=no")
        # gets API information, copy here your created API
        # where "key = " user needs to put his authentication key after logging on https://www.weatherapi.com/my/
        # for free
        weather_json = weather.json()   # data in json format
        cloud_percentage = weather_json["current"]["cloud"]     # cloud percentage variable
        if cloud_percentage < 42:       # if clouds percentage is lower than 42%, ISS might be visible
            return True
        else:
            return False

    def is_it_night(self):      # API with sunrise and sunset data
        sun_data = requests.get("https://api.sunrise-sunset.org/json", params=self.parameters)     # gets API data
        sun_data_json = sun_data.json()     # refactor data into json
        sunrise = int(sun_data_json["results"]["sunrise"].split("T")[1].split(":")[0])
        # today's sunrise time at User position
        sunset = int(sun_data_json["results"]["sunset"].split("T")[1].split(":")[0])
        # today's sunset time at User position
        hour_now = datetime.datetime.now().hour     # current hour
        if hour_now >= sunset or hour_now <= sunrise:       # if statement checking is it currently night
            return True
        else:
            return False

    def longitude(self):        # localisation parameters stating max and min longitude for which ISS is visible
        my_lon_lowest = self.my_lon - 5
        my_lon_highest = self.my_lon + 5

        if my_lon_lowest < self.iss_lon < my_lon_highest:
            # if ISS current location is in created parameters, returns True
            return True
        else:
            return False

    def latitude(self):     # localisation parameters stating max and min latitude for which ISS is visible
        my_lat_lowest = self.my_lat - 5
        my_lat_highest = self.my_lat + 5

        if my_lat_lowest < self.iss_lat < my_lat_highest:
            # if ISS current location is in created parameters, returns True
            return True
        else:
            return False

    def is_iss_visible(self):       # definitive statement checking all the above conditions
        if self.latitude() and self.longitude() and self.is_it_night() and self.clouds():
            return True
        else:
            return False
