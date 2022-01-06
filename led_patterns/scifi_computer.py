
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
colors = [[0, 0, 166], [200, 0, 0], [50, 50, 50], [255, 230, 0]]
density = 1 #percentage of led strip to be lit at one time
percent_off = 100 #higher number = on more often


# for p in range(0, int((num_pixels-1)*density)):
#     colors.append([0,0,0])
assigned_colors = []
for p in range(0, num_pixels-1):
    color_index = random.randrange(0, len(colors))
    pixel = {
        'id': p,
        'r': colors[color_index][0],
        'g': colors[color_index][1],
        'b': colors[color_index][2],
        'delay': random.randrange(0, percent_off)

    }
    assigned_colors.append(pixel)


while(True):
    
    for i in range(0, 100):
        p = random.randrange(0, num_pixels-1)
        if assigned_colors[p]['delay'] > random.randrange(0, i+1):
            if static_colors:
                pixels[p] = (assigned_colors[p]['r'], assigned_colors[p]['g'], assigned_colors[p]['b'])   
            if not static_colors:
                color_index = random.randrange(0, len(colors))
                pixels[p] = (colors[color_index][0], colors[color_index][1], colors[color_index][2])
        else: 
            pixels[p] = (0,0,0)
        time.sleep(random.uniform(.001, .05))

        pixels.show()
        


#tried to make each pixel blink at its own rate rather than a overall time.sleep

#make a property called "blink", "random", "always-on"

#array of colors to display and randomly fades them in and out
#can fade or just turn on and off
#can maybe change colors instead of fading out then changing
