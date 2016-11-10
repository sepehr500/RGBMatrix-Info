#from NewsInfo import NewsInfo
from WeatherBrief import WeatherBrief
import argparse, time, sys, os
import urllib
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix
import Image
import ImageDraw
import time
from PIL import ImageFont
import datetime
#Center Definition


WeatherBrief.playScreen()