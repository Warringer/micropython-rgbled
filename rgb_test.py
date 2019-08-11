import rgbled
import time

def pause():
    time.sleep(1)
    
def clear_pause():
    pause()
    led.clear()
    pause()

data_pin = 0 # ESP8266 GPIO0
# clock_pin = 1 # ESP8266 GPIO1 Only for APA102
led_count = 16 # number of LEDs

color = rgbled.COLOR_CYAN
intensity = 0.1

print("Testing the micropython-rgbled module")

# for NeoPixel
led = rgbled.RgbLed(count=led_count, data=data_pin)
# for ASA02
# led = rgbled.RgbLed(count=led_count, data=data_pin, clock=clock_pin)

print("Testing clearing LEDs")
led.clear()
pause

print("Testing setting LEDs")
'''
print("Testing setting single LED")
led.set_led(color, pos=3)
clear_pause()

print("Testing setting all LEDs")
led.set_led(color)
clear_pause()

print("Testing LED intensity")
led.set_led(color, intensity=intensity)
clear_pause()

print("Testing color_cycle")
led.color_cycle(wait=1)
clear_pause()

print("Testing cycle")
print("Testing normal cycle")
led.cycle(color, wait=20)
clear_pause()

print("Testing inverted cycle")
led.cycle(color, wait=20, invert=True)
clear_pause()
'''
print("Testing fade")
led.fade(color)
clear_pause()

print("Testing fade in")
led.fade(color, fadeout=False)
clear_pause()

print("Testing fade out")
led.fade(color, fadein=False)
clear_pause