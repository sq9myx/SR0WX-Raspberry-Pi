import requests
from config import *


def wind_direction(azi):
    if 0 <= azi <= 22:
        res = "północnych"
    elif 22 <= azi <= 67:
        res = "pólnocno-zzachodnich"
    elif 67 <= azi <= 112:
        res = "zachodnich"
    elif 112 <= azi <= 157:
        res = "południowo-zachodnich"
    elif 157 <= azi <= 202:
        res = "południowych"
    elif 202 <= azi <= 247:
        res = "południowo-wschodnich"
    elif 247 <= azi <= 292:
        res = "wschodnich"
    elif 292 <= azi <= 337:
        res = "pólnocno-wschodnich"
    elif 337 <= azi <= 360:
        res = "północnych"
    else:
        res = "nieokreślonych"
    return res


def meter_declination(meter): # TODO: trzeba poprawić dla wartości powyżej 10
    if meter == 1:
        res = 'metr'
    elif 2 <= meter < 5:
        res = 'metry'
    elif 5 <= meter < 22:
        res = 'metrów'
    elif 2 <= (meter%10) < 5:
        res = 'metry'
    else:
        res = 'metrów'
    return res


def degree_declination(degree):
    if degree == 1:
        res = 'stopień'
    elif 2 <= degree < 5:
        res = 'stopnie'
    elif 5 <= degree < 22:
        res = 'stopni'
    elif 2 <= (degree%10) < 5:
        res = 'stopnie'
    else:
        res = 'stopni'
    return res


class DarkSky:
    key = darksky_key
    lang = darksky_lang
    units = darksky_units
    cities = darksky_cities
    url_forecast = "https://api.darksky.net/forecast/{key}/{lat},{lon}"

    def get_data(self):
        message = ""
        for city_conf in self.cities:
            city = DarkSkyCity(city_conf["lat"], city_conf["lon"], city_conf["name"])
            message += city.name + " - "
            message += city.get_weather_now()
            message += city.get_summary_hourly()
            message += city.get_forecast_daily()
            message += "  "

        return {
            "message": message,
            "source": "darksky.com",
        }


class DarkSkyCity(DarkSky):
    lat = 0
    lon = 0
    name = ""
    forecast = ""

    def __init__(self, lat, lon, name):
        self.lat = lat
        self.lon = lon
        self.name = name
        self.forecast = self.get_forecast()


    def get_forecast(self):
        url = self.url_forecast.format(
            key=self.key,
            lat=self.lat,
            lon=self.lon)
        params = {'lang': self.lang, 'units': self.units}
        req = requests.get(url, params=params)
        return eval(req.content)

    def get_weather_now(self):
        curr = self.forecast["currently"]
        msg = "Aktualnie " + curr["summary"] + "," + \
              " temperatura " + str(int(curr["temperature"])) + " " + degree_declination(int(curr["temperature"]))
        if abs(curr["temperature"] - curr["apparentTemperature"]) > 2:
            msg = msg + ", temperatura odczuwalna" + str(curr["apparentTemperature"]) + " " + \
                  degree_declination(int(curr["temperature"]))
        else:
            msg += ". "
        msg += "Wiatr z kierunków " + wind_direction(curr["windBearing"]) + ", " + \
               str(round(curr["windSpeed"])) + " " + \
               meter_declination(round(curr["windSpeed"])) + " na sekundę"
        if abs(curr["windSpeed"] - curr["windGust"]) > 2:
            msg += " w porywach do " + str(round(curr["windGust"])) + " " + meter_declination(
                round(curr["windGust"])) + " na sekundę. "
        else:
            msg += ". "
        if curr["precipProbability"] > 50:
            msg = msg + "Prawdopodobieństwo wystąpienia opadu o intensywności " + \
                  curr["precipIntensity"] + "jednostek ni chuja nie znam, to " + \
                  curr["precipProbability"] + " procent."                          # TODO: jednostki dla opadu i napisać bardziej po polsku
        msg += "Ciśnienie " + str(round(curr["pressure"])) + " hektopaskali, "
        # TODO: i będzie spadać/rosnąć
        msg += "wilgotność " + str(round(curr["humidity"] * 100)) + " procent. "
        return msg


    def get_forecast_next_hour(self):   # TODO: dopisać prognozę na kolejną godzinę

        return None

    def get_summary_hourly(self):
        a = self.forecast["hourly"]
        b = a["summary"]
        msg = "W najbliższych godzinach " + b + " "
        return msg

    def get_forecast_daily(self):
        a = self.forecast["daily"]
        b = a["summary"]
        msg = "Prognoza na kolejne dni - " + b
        return msg


a = DarkSky()
print(a.get_data())
