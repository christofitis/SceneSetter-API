
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

crawl_start = 1
crawl_end = 5

red_on = 0
green_on = 0
blue_on = 100

red_off = 0
green_off = 0
blue_off = 0

length = 2

worm_body = []

move_right = True

bounce = True

crawl_speed = 70000

for x in range(crawl_start, crawl_start+length):
    worm_body.append(x)

while (True):

    for x in range(0, len(worm_body)):
        if move_right:
            worm_body[x] += 1
            if worm_body[x] >= min(crawl_end+1, num_pixels):
                worm_body[x] = crawl_start
        if not move_right:
            worm_body[x] -= 1
            if worm_body[x] < crawl_start:
                worm_body[x] = min(crawl_end+1, num_pixels)
    for p in range(crawl_start, min(crawl_end+1, num_pixels)):
            pixels[p] = (red_off, green_off, blue_off)
    if bounce:
        if min(crawl_end, num_pixels-1) in worm_body:
            move_right = False
        if crawl_start in worm_body:
            move_right = True
    for p in worm_body:
        pixels[p] = (red_on, green_on, blue_on)
    pixels.show()
    #print(worm_body)
    time.sleep(.08)

#length of worm
#number of worms at a time
#speed of worms
#direction of worms

