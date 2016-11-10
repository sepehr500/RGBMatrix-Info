
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







class WeatherBrief:
    
    @classmethod
    def playScreen(self):
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
        now = datetime.datetime.now()
        WO = WeatherInfo.GetForcast()
        print(WO[:5])
        for forcast in WO[:5]:
          print(forcast)
          temp  = Image.open("WeatherGifs/"+forcast['icon']+"16x16.gif")
          hi = str(int(forcast['high']))
          low = str(int(forcast['low']))
          sum = str(forcast['summary'])
          hum = str(forcast['humid'])
          precip = str(forcast['prob'] * 10)
          
          im = temp
          #day of the week
          Ctime = now.strftime("%A")

          xPos = 33
          image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
          draw = ImageDraw.Draw(image)
          for x in range(0,draw.textsize(sum)[0]):
          
          
            image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
            draw = ImageDraw.Draw(image)

            image.paste(im, (0, 7))
            w, h = CenterFind(draw, Ctime[:4])
            w2, h2 = CenterFind(draw, hi)

            draw.text((w+4, h - 12), Ctime[:4], font=fnt, fill=(0, 0, 225))
            draw.text((w2 + 10, h2 - 4), hi, font=fnt2, fill=(0, 0, 225))
            draw.text((w2 + 10, h2 + 4), low, font=fnt2, fill=(0, 0, 225))
            draw.text((xPos, 22 ), sum, font=fnt2, fill=(0, 0, 225))
            xPos -= 1
            time.sleep(.05)
          
          
          
            doubleBuffer.SetImage(image)
            doubleBuffer = matrix.SwapOnVSync(doubleBuffer)
          xPos = 0
          now = now + datetime.timedelta(days=1)
          #time.sleep(5)