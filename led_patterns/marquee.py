#trying to make multiple worms
import time
import board
import neopixel
import random

pixel_pin = board.D21
num_pixels = 17
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)

marquee_start = 0
marquee_end = 16


red_on = 10
green_on = 0
blue_on = 0

red_off = 0
green_off = 10
blue_off = 0

worm_body = []

move_right = True

num_on = 8
num_off = 8
counter = 0
init_on = True


print(worm_body)
while (True):
    for p in range(marquee_start, marquee_end+1):
        pixels[p] = (red_off, green_off, blue_off)
    for p in worm_body:
        pixels[min(p, marquee_end)] = (red_on, green_on, blue_on)

    for p in range(0, len(worm_body)):    
        worm_body[p] += 1
    if init_on:
        worm_body.append(0)
    if max(worm_body) > marquee_end:
        worm_body.remove(marquee_end+1)

    counter += 1
    if counter >= num_on and init_on:
        counter = 0
        init_on = False
        
    if counter >= num_off and not init_on:
        counter = 0
        init_on = True  

    pixels.show()
    time.sleep(.08)
