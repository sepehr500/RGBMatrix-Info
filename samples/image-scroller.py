#!/usr/bin/env python
import time
from samplebase import SampleBase
from rgbmatrix import RGBMatrix
from PIL import Image
import argparse, time, sys, os
class ImageScroller(SampleBase):
    def __init__(self, image_file, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.image = Image.open(image_file)

    def Run(self):
        print(sys.path)
        self.image = self.image.convert("RGB")
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        doubleBuffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size
        print(img_width)
        print(img_height)
        print(self.image)

        # let's scroll
        xpos = 0
        while True:
            xpos += 1
            if (xpos > img_width):
                xpos = 0
                
            doubleBuffer.SetImage(self.image, -xpos)
            time.sleep(1)
            doubleBuffer.SetImage(self.image, -xpos + img_width)

        
            doubleBuffer = self.matrix.SwapOnVSync(doubleBuffer)
            time.sleep(0.01)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    scroller = ImageScroller(image_file = "../../workspace/Rain32x32.gif")
    if (not scroller.process()):
        scroller.print_help()
