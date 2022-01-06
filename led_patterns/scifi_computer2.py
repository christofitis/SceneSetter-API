
import time
import board
import neopixel
import random

pixel_pin = board.D21
num_pixels = 17
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=.1, auto_write=False, pixel_order=ORDER
)

static_colors = True #if single pixel is given and color and never changes that color or not
colors = [[218, 247, 166], [255, 195, 0], [255, 87, 51], [199, 0, 57], [144, 12, 63], [88, 24, 69]]
density = 1 #percentage of led strip to be lit at one time
percent_off = 1000 #if random number between 0 - 100 is greater than this, then it gets a color, else off. 


# for p in range(0, int((num_pixels-1)*density)):
#     colors.append([0,0,0])
assigned_colors = []
for p in range(0, num_pixels-1):
    color_index = random.randrange(0, len(colors)-1)
    pixel = {
        'id': p,
        'r': colors[color_index][0],
        'g': colors[color_index][1],
        'b': colors[color_index][2],

    }
    assigned_colors.append(pixel)


while(True):
    p = random.randrange(0, num_pixels-1)
    color_index = random.randrange(0, len(colors)-1)
    if random.randrange(0, 10000) > percent_off:
        if static_colors:
            pixels[p] = (assigned_colors[p]['r'], assigned_colors[p]['g'], assigned_colors[p]['b'])   
        if not static_colors:
            pixels[p] = (colors[color_index][0], colors[color_index][1], colors[color_index][2])
    else: 
        pixels[p] = (0,0,0)
    

    pixels.show()
    #time.sleep(random.uniform(.01, 1))

    #time.sleep causes all pixels to pause the same amount. 