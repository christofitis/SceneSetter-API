
import time
import board
import neopixel
import random

pixel_pin = board.D21
num_pixels = 17
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

fire_start = 0
fire_end = 17

fade_speed_multiplyer = 20 #higher number = slower fade
fade_speed_min = .01 #larger number = faster fade
fade_speed_max = .001

fade_up_chance_ratio = [10,10000]  #a out of b chance of lighting up

red_min = 0 #min values must stay at 0
red_max = 200
green_min = 0
green_max = 50
blue_min = 0
blue_max = 0


pixel_data = []
def start():
    #initialize strip
    for p in range(fire_start, min(fire_end+1, num_pixels)):
        pixel = {
            'id': p, 
            'fade_speed': random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplyer,
            'fade_up': random.randrange(0,1),
            'red_current': 0,
            'green_current': 0,
            'blue_current': 0,
        }
        pixel_data.append(pixel)

    #animation loop
    while(True):
        for p in pixel_data:
            dir_change_offset = random.uniform(.1,1)
            if p['red_current'] >= red_max*dir_change_offset and p['green_current'] >= green_max*dir_change_offset and p['blue_current'] >= blue_max*dir_change_offset:
                p['fade_up'] = 0
                p['fade_speed'] = random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplyer
            if p['red_current'] <= red_min*dir_change_offset and p['green_current'] <= green_min*dir_change_offset and p['blue_current'] <= blue_min*dir_change_offset:
                if random.randrange(0,fade_up_chance_ratio[1]) >= fade_up_chance_ratio[1]-fade_up_chance_ratio[0]:
                    p['fade_up'] = 1
                p['fade_speed'] = random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplyer
            if p['fade_up']:
                p['red_current'] += abs(red_max-red_min)*p['fade_speed']
                p['green_current'] += abs(green_max-green_min)*p['fade_speed']
                p['blue_current'] += abs(blue_max-blue_min)*p['fade_speed']
            if not p['fade_up']:
                p['red_current'] -= abs(red_max-red_min)*p['fade_speed']  
                p['green_current'] -= abs(green_max-green_min)*p['fade_speed'] 
                p['blue_current'] -= abs(blue_max-blue_min)*p['fade_speed']

            p['red_current'] = max(red_min, min(red_max, p['red_current']))
            p['green_current'] = max(green_min, min(green_max, p['green_current']))
            p['blue_current'] = max(blue_min, min(blue_max, p['blue_current']))

            pixels[p['id']] = (int(p['red_current']), int(p['green_current']), int(p['blue_current']))
        pixels.show()

def random_range(start, stop):
    return random.randint(start, stop)

start()