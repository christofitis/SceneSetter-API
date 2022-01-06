
import time
import board
import neopixel

pixel_pin = board.D21
num_pixels = 17
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)

pulse_start = 5
pulse_end = 6

fade_up = True #direction of fade
fade_speed = .0009 

red_min = 0
red_max = 3
red_current = 0
red_fade_speed =abs(red_max-red_min)*fade_speed
print('red ' + str(red_fade_speed))
green_min = 0
green_max = 12
green_current = 0
green_fade_speed = abs(green_max-green_min)*fade_speed
print('green ' + str(green_fade_speed))
blue_min = 0
blue_max = 10
blue_current = 0
blue_fade_speed = abs(blue_max-blue_min)*fade_speed
print('blue ' + str(blue_fade_speed))

while(True):
    for p in range(pulse_start, min(pulse_end+1, num_pixels)):
        if red_current >= red_max and green_current >= green_max and blue_current >= blue_max:
            fade_up = False
        if red_current <= red_min and green_current <= green_min and blue_current <= blue_min:
            fade_up = True
        if fade_up:
            red_current += red_fade_speed
            green_current += green_fade_speed
            blue_current += blue_fade_speed
        if not fade_up:
            red_current -= red_fade_speed
            green_current -= green_fade_speed
            blue_current -= blue_fade_speed

        red = max(red_min, min(red_max, red_current))
        green = max(green_min, min(green_max, green_current))
        blue = max(blue_min, min(blue_max, blue_current))
    
        pixels[p] = (int(red), int(green), int(blue))
    #pixels[2] = (0,0,100,100)
    pixels.show()

    

