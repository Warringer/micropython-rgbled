import rgbled
import time

def pause():
    time.sleep(500)

data_pin = 0 # ESP8266 GPIO0
# clock_pin = 1 # ESP8266 GPIO1 Only for APA102
led_count = 8 # number of LEDs

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

print("Testing setting single LED")
led.set_led(color, pos=3)
pause()
led.clear()
pause()

print("Testing setting all LEDs")
led.set_led(color)
pause()
led.clear()
pause()

print("Testing LED intensity")
led.set_led(color, intensity=intensity)
pause()
led.clear()
pause()

print("Testing color_cycle")
led.color_cycle()
pause()
led.clear()
pause()

print("Testing cycle")
print("Testing normal cycle")
led.cycle(color)
pause()
led.clear()
pause()

print("Testing inverted cycle")
led.cycle(color, invert=True)
pause()
led.clear()
pause()