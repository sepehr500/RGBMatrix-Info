import pyowm
import darksky as ds
import forecastio
import ConfigParser
from datetime import datetime
class WeatherInfo:
    configParser = ConfigParser.RawConfigParser()   
    configFilePath = 'Config.ini'
    configParser.readfp(open(configFilePath))
    key = configParser.get('Weather','DarkSkyKey')
    Lat = float(configParser.get('Weather','Lat'))
    Long = float(configParser.get('Weather','Long'))
    
    
   
       
    @classmethod
    def GetForcast(self):
        forecast = forecastio.load_forecast(self.key,self.Lat, self.Long)
        li = []
        daily = forecast.daily()
        #goes through each day giving max and min temp
        for x in daily.data:
            high = x.apparentTemperatureMax
            low = x.apparentTemperatureMin
            pressure = x.pressure
            humid = x.humidity
            summary = x.summary
            precipProb = x.precipProbability
            #maybe do this it is only there if there is an alert
            # print x.alerts
            #use for icon clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, or partly-cloudy-night
            icon = x.icon
            li.append(dict([ ('summary',summary), ('humid', humid), ('prob' , precipProb) , ("high", high) , ("low", low), ("icon", icon)]))
        return li
        
    #This is muchhhh better
    @classmethod
    def GetCurrentWeatherDarkSky(self):
        print("weather call made")
        forecast = forecastio.load_forecast( self.key,self.Lat, self.Long)
        now = forecast.currently()
        summary =  now.summary
        temp = now.temperature
        precipProb = now.precipProbability
        humid = now.humidity
        icon = now.icon
        return dict([('temp', temp), ('summary',summary), ('humid', humid), ('prob' , precipProb), ('icon' , icon)])
        