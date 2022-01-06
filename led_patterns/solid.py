
import time
import board
import neopixel

pixel_pin = board.D21
num_pixels = 17
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)

solid_start = 5
solid_end = 7

red = 5
green = 20
blue = 100

while(True):
    for p in range(solid_start, min(solid_end+1, num_pixels)):
        pixels[p] = (red, green, blue)
    pixels.show()



