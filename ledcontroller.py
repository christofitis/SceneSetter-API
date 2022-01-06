import board
import neopixel
import time
import random
from threading import Thread
from flask import Flask
import json
from dbconnector import query_db, update_db
from noise import pnoise3


pixel_pin = board.D21
num_pixels = 0
pixels = None
restart_pattern_delay = 2
app = Flask(__name__)
is_initialized = False

def initialize_led_strip():
    global pixels
    global num_pixels
    num_pixels = query_db('SELECT num_leds FROM config WHERE id = 1;')[0][0]
    brightness = query_db('SELECT brightness FROM config where id = 1;')[0][0]
    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=brightness, auto_write=False
    )
    

def is_running():
    return query_db("SELECT running FROM state WHERE id = 1;")[0][0]


def get_function(func_name):
        if func_name == 'fire':
            return fire
        if func_name == 'crawl':
            return crawl
        if func_name == 'pulse':
            return pulse
        if func_name == 'solid':
            return solid
        if func_name == 'scifi_computer':
            return scifi_computer
        if func_name == 'marquee':
            return marquee
        else:
            return None

def run_find_led(num):
    initialize_led_strip()
    pixels.fill((0,0,0))
    pixels[max(0, min(int(num)-1, num_pixels-1))] = (25, 25, 25)
    pixels.show()


def start(data):
    query = query_db('SELECT pattern, start, end, red_on, green_on, blue_on, red_off, green_off, blue_off, crawl_length, move_right, crawl_bounce, speed_max, fade_speed_min, fade_speed_max, fade_speed_multiplier, fade_up_chance_ratio, colors, on_frequency, off_frequency, marquee_num_on, marquee_num_off, brightness, octives, persistence, lacunarity FROM scene_layouts WHERE sceneid = ' + str(data['sceneid']))
    scene_data = []
    for layout in query:
        scene_data.append(
            {
                'pattern': layout[0],
                'start': layout[1],
                'end': layout[2],
                'red_on': layout[3],
                'green_on': layout[4],
                'blue_on': layout[5],
                'red_off': layout[6],
                'green_off': layout[7],
                'blue_off': layout[8],
                'crawl_length': layout[9],
                'move_right': layout[10],
                'crawl_bounce': layout[11],
                'speed_max': layout[12],
                'fade_speed_min': layout[13],
                'fade_speed_max': layout[14],
                'fade_speed_multiplier': layout[15],
                'fade_up_chance_ratio': layout[16],
                'colors': layout[17],
                'on_frequency': layout[18],
                'off_frequency': layout[19],
                'marquee_num_on': layout[20],
                'marquee_num_off': layout[21],
                'brightness': layout[22],
                'octives': layout[23],
                'persistence': layout[24],
                'lacunarity': layout[25],
            }
        )
    for pattern_data in scene_data:
        function = get_function(pattern_data['pattern'])
        if function:
            update_db('UPDATE state SET running = 1 WHERE id = 1;')
            Thread(target=function, args=[pattern_data]).start()


def all_off():
    initialize_led_strip()
    pixels.fill((0,0,0))
    pixels.show()


def crawl(pattern_data):
    crawl_start = max(0, pattern_data['start'])
    crawl_end = min(pattern_data['end'], num_pixels)
    red_on = pattern_data['red_on']
    green_on = pattern_data['green_on']
    blue_on = pattern_data['blue_on']
    red_off = pattern_data['red_off']
    green_off = pattern_data['green_off']
    blue_off = pattern_data['blue_off']
    crawl_length = pattern_data['crawl_length']
    move_right = pattern_data['move_right']
    crawl_bounce = pattern_data['crawl_bounce'] 
    crawl_speed = pattern_data['speed_max']
    brightness = pattern_data['brightness']
    worm_body = []
    for x in range(crawl_start, crawl_start+crawl_length):
        worm_body.append(x)
    with app.app_context():
        while (is_running()):
            for x in range(0, len(worm_body)):
                if move_right:
                    worm_body[x] += 1
                    if worm_body[x] >= crawl_end:
                        worm_body[x] = crawl_start-1
                elif not move_right:
                    worm_body[x] -= 1
                    if worm_body[x] < crawl_start-1:
                        worm_body[x] = crawl_end-1
                for p in range(crawl_start-1, crawl_end+1):
                    pixels[max(0, min(num_pixels-1,p))] = (int(red_off*brightness), int(green_off*brightness), int(blue_off*brightness))
            if crawl_bounce:
                if crawl_end-1 in worm_body:
                    move_right = False
                elif crawl_start-1 in worm_body:
                    move_right = True
            for p in worm_body:
                pixels[max(0, min(num_pixels,p))] = (int(red_on*brightness), int(green_on*brightness), int(blue_on*brightness))
            pixels.show()
            time.sleep(crawl_speed)


# def fire(pattern_data):
#     fire_start = max(0, pattern_data['start']-1)
#     fire_end = min(pattern_data['end'], num_pixels)
#     fade_speed_multiplier = pattern_data['fade_speed_multiplier'] #higher number = slower fade
#     fade_speed_min = pattern_data['fade_speed_min'] #larger number = faster fade
#     fade_speed_max = pattern_data['fade_speed_max']
#     fade_up_chance_ratio = pattern_data['fade_up_chance_ratio']  #a out of b chance of lighting up
#     red_on = pattern_data['red_on']
#     green_on = pattern_data['green_on']
#     blue_on = pattern_data['blue_on']
#     brightness = pattern_data['brightness']
#     red_off = 0 #off values must stay at 0
#     green_off = 0
#     blue_off = 0

#     pixel_data = []
#     #initialize strip
#     for p in range(fire_start, fire_end):
#         pixel = {
#             'id': p, 
#             'fade_speed': random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplier,
#             'fade_up': random.randrange(0,1),
#             'red_current': 0,
#             'green_current': 0,
#             'blue_current': 0,
#         }
#         pixel_data.append(pixel)

#     with app.app_context():
#         while(is_running()):
#             for p in pixel_data:
#                 dir_change_offset = random.uniform(.1,1)
#                 if p['red_current'] >= red_on*dir_change_offset and p['green_current'] >= green_on*dir_change_offset and p['blue_current'] >= blue_on*dir_change_offset:
#                     p['fade_up'] = 0
#                     p['fade_speed'] = random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplier
#                 if p['red_current'] <= red_off*dir_change_offset and p['green_current'] <= green_off*dir_change_offset and p['blue_current'] <= blue_off*dir_change_offset:
#                     if random.randrange(0,fade_up_chance_ratio) == 1:
#                         p['fade_up'] = 1
#                     p['fade_speed'] = random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplier
#                 if p['fade_up']:
#                     p['red_current'] += abs(red_on-red_off)*p['fade_speed']
#                     p['green_current'] += abs(green_on-green_off)*p['fade_speed']
#                     p['blue_current'] += abs(blue_on-blue_off)*p['fade_speed']
#                 if not p['fade_up']:
#                     p['red_current'] -= abs(red_on-red_off)*p['fade_speed']  
#                     p['green_current'] -= abs(green_on-green_off)*p['fade_speed'] 
#                     p['blue_current'] -= abs(blue_on-blue_off)*p['fade_speed']

#                 p['red_current'] = max(red_off, min(red_on, p['red_current']))
#                 p['green_current'] = max(green_off, min(green_on, p['green_current']))
#                 p['blue_current'] = max(blue_off, min(blue_on, p['blue_current']))

#                 pixels[p['id']] = (int(p['red_current']*brightness), int(p['green_current']*brightness), int(p['blue_current']*brightness))
#             pixels.show()

def fire(pattern_data):
    fire_start = max(0, pattern_data['start']-1)
    fire_end = min(pattern_data['end'], num_pixels)
    speed = pattern_data['speed_max']
    octives = pattern_data['octives']
    persistence = pattern_data['persistence']
    lacunarity = pattern_data['lacunarity']
    # fade_speed_multiplier = pattern_data['fade_speed_multiplier'] #higher number = slower fade
    # fade_speed_min = pattern_data['fade_speed_min'] #larger number = faster fade
    # fade_speed_max = pattern_data['fade_speed_max']
    # fade_up_chance_ratio = pattern_data['fade_up_chance_ratio']  #a out of b chance of lighting up
    red_on = pattern_data['red_on']
    green_on = pattern_data['green_on']
    blue_on = pattern_data['blue_on']
    brightness = pattern_data['brightness']
    red_off = pattern_data['red_off']
    green_off = pattern_data['green_off']
    blue_off = pattern_data['blue_off']

    pixel_data = []

    counter = 0.0
    counter_repeat_limit = 10000
    counter_direction = 1
    #initialize strip
    for p in range(fire_start, fire_end):
        
        pixel = {
            'id': p, 
            #'fade_speed': speed,
            # 'fade_up': random.randrange(0,1),
            
            'red_current': 0,
            'green_current': 0,
            'blue_current': 0,
            'y': random.random()*random.randrange(1, 1024),
            'z': random.random()*random.randrange(1, 1024),
            'base': 0
        }
        pixel_data.append(pixel) 

    with app.app_context():
        while(is_running()):
            if counter >= counter_repeat_limit:
                counter_direction *= -1
            counter += speed*counter_direction
            for p in pixel_data:
                #pnoise3(x, y, z, octaves=1, persistence=0.5, lacunarity=2.0repeatx=1024, repeaty=1024, repeatz=1024, base=0.0)
                fader = pnoise3(counter, p['y'], p['z'], octives, persistence, lacunarity, 1024, 1024, 1024, p['base'])*2 #
                p['red_current'] = (red_on*fader)
                p['green_current'] = (green_on*fader)
                p['blue_current'] = (blue_on*fader)

                p['red_current'] = max(red_off, min(red_on, p['red_current']))
                p['green_current'] = max(green_off, min(green_on, p['green_current']))
                p['blue_current'] = max(blue_off, min(blue_on, p['blue_current']))

                pixels[p['id']] = (int(p['red_current']*brightness), int(p['green_current']*brightness), int(p['blue_current']*brightness))
            
            pixels.show()
            time.sleep(.01)


#pattern using perlin noise moving down z axis to give effect that pixels are spreading there color to each other
def contagious(pattern_data):
    fire_start = max(0, pattern_data['start']-1)
    fire_end = min(pattern_data['end'], num_pixels)
    fade_speed_multiplier = pattern_data['fade_speed_multiplier'] #higher number = slower fade
    fade_speed_min = pattern_data['fade_speed_min'] #larger number = faster fade
    fade_speed_max = pattern_data['fade_speed_max']
    fade_up_chance_ratio = pattern_data['fade_up_chance_ratio']  #a out of b chance of lighting up
    red_on = pattern_data['red_on']
    green_on = pattern_data['green_on']
    blue_on = pattern_data['blue_on']
    brightness = pattern_data['brightness']
    red_off = 0 #off values must stay at 0
    green_off = 0
    blue_off = 0

    pixel_data = []

    z = 1

    counter = 0.0
    #initialize strip
    for p in range(fire_start, fire_end):
        z += .05
        pixel = {
            'id': p, 
            'fade_speed': random.uniform(fade_speed_min, fade_speed_max)/fade_speed_multiplier,
            'fade_up': random.randrange(0,1),
            'red_current': 0,
            'green_current': 0,
            'blue_current': 0,
            'y': z,
            'z': random.random()*random.randrange(1, 1024),
            'base': 0
        }
        pixel_data.append(pixel) 

    with app.app_context():
        while(is_running()):
            counter += .001
            for p in pixel_data:
                fader = pnoise3(p['y'], 1, counter, 5, .9, 2, 1024, 1024, 1024, p['base'])*2 #this
                #fader = pnoise3(counter, p['y'], p['z'], 5, .5, 2, 1024, 1024, 1024, p['base'])*2
                p['red_current'] = red_on*fader
                p['green_current'] = green_on*fader
                p['blue_current'] = blue_on*fader

                p['red_current'] = max(red_off, min(red_on, p['red_current']))
                p['green_current'] = max(green_off, min(green_on, p['green_current']))
                p['blue_current'] = max(blue_off, min(blue_on, p['blue_current']))

                pixels[p['id']] = (int(p['red_current']*brightness), int(p['green_current']*brightness), int(p['blue_current']*brightness))
            
            pixels.show()
            time.sleep(.01)


def pulse(pattern_data):
    pulse_start = max(0, pattern_data['start']-1)
    pulse_end = min(pattern_data['end'], num_pixels)
    fade_speed = pattern_data['speed_max'] 
    red_on = pattern_data['red_on']
    green_on = pattern_data['green_on']
    blue_on = pattern_data['blue_on']
    red_off = pattern_data['red_off']
    green_off = pattern_data['green_off']
    blue_off = pattern_data['blue_off']
    brightness = pattern_data['brightness']

    red_current = 0
    green_current = 0
    blue_current = 0
    red_fade_speed = abs(red_on-red_off)*fade_speed
    green_fade_speed = abs(green_on-green_off)*fade_speed
    blue_fade_speed = abs(blue_on-blue_off)*fade_speed
    fade_up = True #direction of fade

    color_mult = 0
    with app.app_context():
        while(is_running()):
            if fade_up:
                color_mult += fade_speed
            if not fade_up:
                color_mult -= fade_speed
            if color_mult >= 100:
                fade_up = False
            if color_mult <= 0:
                fade_up = True
            for p in range(pulse_start, pulse_end):
                on_mult = color_mult/100
                off_mult = abs(color_mult-100)/100
                red = int((red_on*on_mult) + (red_off*off_mult))
                green = int((green_on*on_mult) + (green_off*off_mult))
                blue = int((blue_on*on_mult) + (blue_off*off_mult))
                #pixels[p] = max(0, min(255,(int(red*brightness)))), max(0, min(255, int(green*brightness))), max(0, min(255, int(blue*brightness))))
                pixels[p] = (max(0, min(255,(int(red*brightness)))), max(0, min(255, int(green*brightness))), max(0, min(255, int(blue*brightness))))
            pixels.show()


def solid(pattern_data):
    solid_start = max(0, pattern_data['start']-1)
    solid_end = min(pattern_data['end'], num_pixels)
    red_on = pattern_data['red_on']
    green_on = pattern_data['green_on']
    blue_on = pattern_data['blue_on']
    brightness = pattern_data['brightness']
    
    with app.app_context():
        while(is_running()):
            for p in range(solid_start, solid_end):
                pixels[p] = (int(red_on*brightness), int(green_on*brightness), int(blue_on*brightness))
            pixels.show()


def scifi_computer(pattern_data):
    scifi_start = max(0, pattern_data['start']-1)
    scifi_end = min(pattern_data['end'], num_pixels)
    on_frequency = pattern_data['on_frequency']#higher number slower the blinks
    off_frequency = pattern_data['off_frequency']
    colors = json.loads(pattern_data['colors'])
    brightness = pattern_data['brightness']
    static_colors = True #BROKE if single pixel is given and color and never changes that color or not
    pixel_data = []
    color_index = 0
    for p in range(scifi_start, scifi_end):
        color_index = random.randrange(0, len(colors))
        pixel = {
            'id': p,
            'r': colors[color_index][0],
            'g': colors[color_index][1],
            'b': colors[color_index][2],
            'reset_on_count': random.randrange(0, on_frequency), 
            'on_count': 0,
            'reset_off_count': random.randrange(0, off_frequency),
            'off_count': 0,
            'on': random.randrange(0, 1),
            'random_blinking': random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]) #allows some pixels to randomly blink
        }
        pixel_data.append(pixel)

    with app.app_context():
        while(is_running()):
            for p in pixel_data:
                if p['on']:
                    if p['on_count'] < p['reset_on_count']:
                        p['on_count'] += 1
                        if static_colors:
                            pixels[p['id']] = (int(p['r']*brightness), int(p['g']*brightness), int(p['b']*brightness))   
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
                    p['reset_on_count'] = random.randrange(0, on_frequency)
                    p['reset_off_count'] = random.randrange(0, off_frequency)
            pixels.show()


def marquee(pattern_data):
    marquee_start = max(0, pattern_data['start']-1)
    marquee_end = min(pattern_data['end'], num_pixels)
    red_on = pattern_data['red_on']
    green_on = pattern_data['green_on']
    blue_on = pattern_data['blue_on']
    red_off = pattern_data['red_off']
    green_off = pattern_data['green_off']
    blue_off = pattern_data['blue_off']
    move_right = pattern_data['move_right']
    marquee_num_on = pattern_data['marquee_num_on']
    marquee_num_off = pattern_data['marquee_num_off']
    scroll_speed = pattern_data['speed_max']
    brightness = pattern_data['brightness']
    counter = 0
    init_on = True
    worm_body = []
    with app.app_context():
        while (is_running()):
            for p in range(marquee_start, marquee_end):
                pixels[p] = (int(red_off*brightness), int(green_off*brightness), int(blue_off*brightness))
            for p in worm_body:
                pixels[min(max(p, marquee_start-1), marquee_end-1)] = (int(red_on*brightness), int(green_on*brightness), int(blue_on*brightness))
            for p in range(0, len(worm_body)):  
                if move_right:  
                    worm_body[p] += 1
                if not move_right:
                    worm_body[p] -= 1
            if init_on:
                if move_right:
                    worm_body.append(marquee_start)
                if not move_right:
                    worm_body.append(marquee_end)
            if move_right:
                if max(worm_body) >= marquee_end:
                    worm_body.remove(marquee_end)
            if not move_right:
                if min(worm_body) <= marquee_start-1:
                    worm_body.remove(marquee_start-1)
            counter += 1
            if counter >= marquee_num_on and init_on:
                counter = 0
                init_on = False
            if counter >= marquee_num_off and not init_on:
                counter = 0
                init_on = True  
            pixels.show()
            time.sleep(scroll_speed)

