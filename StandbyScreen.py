import threading

import time
import Queue
import datetime
from NewsInfo import NewsInfo
from WeatherInfo import WeatherInfo
import argparse, time, sys, os
import urllib
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix
import Image
import ImageDraw
import time
from PIL import ImageFont

import datetime

class StandbyScreen():
    
    @classmethod
    def standby(self, e):
        def CenterFind(draw, text):
          w, h = draw.textsize(text)
          return ((32 - w) / 2, (32 - h) / 2)
        # Matrix Tuning
        print("standby")

        matrix = RGBMatrix(32, 1, 1)
        matrix.brightness = 80
        matrix.pwmBits = 7
        matrix.luminanceCorrect = True
        # Matrix Tuning
        helv = ImageFont.load('helvR08.pil')
        tiny = ImageFont.truetype("REDENSEK.TTF", 12)
        fnt = ImageFont.load('pilfonts/helvetica-bold-8.pil')
        fnt2 = helv
        fnt3  = helv
        doubleBuffer = matrix.CreateFrameCanvas()
        matrix.Clear()
        # img_width, img_height = image.size

        # let's scroll
        W, H = (32, 32)

        posStart = 22
        incY = -1
        posStartX = 35
        incX = 0


        WO = WeatherInfo.GetCurrentWeatherDarkSky()
        Temp = str(int(WO['temp'])) + "F"
        Precip = str(WO['prob'])
        TrendingList = NewsInfo.GetRecentEventsReddit()
        trendIndex = 0
        trend = TrendingList[trendIndex]
        seekLoc = 0

        #im = Image.open("clear-day16x16.gif")
        temp  = Image.open("WeatherGifs/"+WO['icon']+"16x16.gif")

        goAt = 20
        incerSlow = goAt
        while (e.isSet() == False):
            
              
            

            
            if (datetime.datetime.now().minute % 15 == 0 and datetime.datetime.now().second == 3):
                time.sleep(3)
                WO = WeatherInfo.GetCurrentWeatherDarkSky()
                Temp = str(int(WO['temp']))+ "F"
                Precip = str(WO['prob'] * 10)
                temp  = Image.open("WeatherGifs/"+WO['icon']+"16x16.gif")
                TrendingList = NewsInfo.GetRecentEventsReddit()
                
                
                print("Update Time!")


            try:
              
              if(incerSlow == goAt):
                incerSlow = 0
                temp.seek(temp.tell() + 1)
              
                im = temp
              
                im = im.convert("RGB")
              incerSlow += 1
              
              
              
            except EOFError:
              
              temp  = Image.open("WeatherGifs/"+WO['icon']+"16x16.gif")
              pass






            # set time
            ti = datetime.datetime.now()
            strTime = str(ti.hour if ti.hour <12 else ti.hour - 12) + ":" + str(ti.minute if ti.minute > 9 else "0"+str(ti.minute))
            Ctime = strTime

            image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
            draw = ImageDraw.Draw(image)

            image.paste(im, (0, 8))
            w, h = CenterFind(draw, Ctime)
            w2, h2 = CenterFind(draw, Temp)
            w3, h3 = CenterFind(draw, trend)
            wS, hS = draw.textsize(trend)
            draw.text((w+4, h - 12), Ctime, font=fnt, fill=(0, 0, 225))
            draw.text((w2 + 10, h2 - 4), Temp, font=fnt2, fill=(0, 0, 225))
            draw.text((w2 + 10, h2 + 4), Precip, font=fnt2, fill=(0, 0, 225))
            draw.text((w2 + 20, h2+2 ), '%', font=tiny, fill=(0, 0, 225))

            # Do movements

            if (posStartX == -wS + 20):
                incY = -1
                incX = 0
                #posStart = 32
                posStartX = 35
                if(trendIndex == len(TrendingList) -1):
                  trendIndex = -1
                trendIndex += 1
                trend = TrendingList[trendIndex]
            # 26 is stopping point
            if (posStart == posStart):
                incY = 0
                incX = -1

            if (posStart == 33):
                incY = incY * -1
            posStart += incY
            posStartX += incX
            try:
              draw.text((posStartX, posStart), trend, font=fnt3, fill=(225, 0, 0))
            except UnicodeEncodeError:
              pass
            # image.resize((matrix.width, matrix.height), Image.ANTIALIAS)

            doubleBuffer.SetImage(image)

            doubleBuffer = matrix.SwapOnVSync(doubleBuffer)
            time.sleep(.04)

