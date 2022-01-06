
import time



import board
import neopixel
import random
from threading import Thread

pixel_pin = board.D21
num_pixels = 17
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)


print('strting...')


    
def crawl(start, end):
    crawl_start = start
    crawl_end = end

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

def fire(start, end):
    fire_start = start
    fire_end = end

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



    


def main():
    
    Thread(target=fire, args=[0,8]).start()
    Thread(target=crawl, args=[9,13]).start()
    Thread(target=fire, args=[14,17]).start()
    


 
   



main()