
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

scifi_start = 0
scifi_end = 17

static_colors = True #if single pixel is given and color and never changes that color or not
colors = [[0, 0, 166], [200, 0, 0], [50, 50, 50], [255, 230, 0]]
density = 1 #percentage of led strip to be lit at one time
percent_off = 999 #higher number = on more often


# for p in range(0, int((num_pixels-1)*density)):
#     colors.append([0,0,0])
pixel_data = []
for p in range(scifi_start, min(scifi_end+1, num_pixels)):
    color_index = random.randrange(0, len(colors))
    pixel = {
        'id': p,
        'r': colors[color_index][0],
        'g': colors[color_index][1],
        'b': colors[color_index][2],
        'reset_on_count': random.randrange(0, 1000),
        'on_count': 0,
        'reset_off_count': random.randrange(0, 1000),
        'off_count': 0,
        'on': random.randrange(0, 1),
        'random_blinking': random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]) #allows some pixels to randomly blink

    }
    pixel_data.append(pixel)


while(True):
    
    
    for p in pixel_data:
        if p['on']:
            if p['on_count'] < p['reset_on_count']:
                p['on_count'] += 1
                if static_colors:
                    pixels[p['id']] = (p['r'], p['g'], p['b'])   
                if not static_colors:
                    color_index = random.randrange(0, len(colors))
                    pixels[p['id']] = (colors[color_index][0], colors[color_index][1], colors[color_index][2])
            else:
                p['on_count'] = 0
                p['on'] = 0
                
        if not p['on']:    
            if p['off_count'] < p['reset_off_count']:
                pixels[p['id']] = (0,0,0)
                p['off_count'] += 1
            else:
                p['off_count'] = 0
                p['on'] = 1
        if p['random_blinking']:
            p['reset_on_count'] = random.randrange(0, 1000)
            p['reset_off_count'] = random.randrange(0, 1000)

                
            #time.sleep(.01)

    pixels.show()
        


#leds turn on and off in a perfect pattern


#make a always on

#make a property called "blink", "random", "always-on"

#array of colors to display and randomly fades them in and out
#can fade or just turn on and off
#can maybe change colors instead of fading out then changing
