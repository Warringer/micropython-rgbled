import math, time
from machine import Pin
from neopixel import NeoPixel
from apa102 import APA102

def rgb_to_hsv(rgb_color):
    (r, g, b) = rgb_color
    r = float(1 / 255 * r)
    g = float(1 / 255 * g)
    b = float(1 / 255 * b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d/high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v

def hsv_to_rgb(hsv_color):
    (h, s, v) = hsv_color
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]
    r = int(255 * r)
    g = int(255 * g)
    b = int(255 * b)
    return r, g, b

def hex_to_rgb(self, hex):
    """ Returns the RGB value of a Hex Colour

    Parameters
    ----------
    hex : string
        The hex representation of a RGB color
        Example:
            hex_to_rgb("123456")
    """
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)
COLOR_YELLOW = (255, 255, 0)

class RgbLed():
    '''LED agnostic RGB LED driver'''

    def __init__(self, count, data, clock=None, apa102c=False):
        data_pin = Pin(data, Pin.OUT)
        self.neopixel = True
        if clock is None:
            self.leds = NeoPixel(data_pin, count)
        else:
            self.neopixel = False
            clock_pin = Pin(clock, Pin.OUT)
            self.leds = APA102(data_pin, clock_pin, count)
            if apa102c:
                self.leds.ORDER = (0, 2, 1, 3)
        self.count = count

    def _set_led(self, color, intensity, pos):
        if type(color) is str:
            color = hex_to_rgb(color)
        if self.neopixel:
            if intensity < 1:
                h, s, _ = rgb_to_hsv(color)
                v = intensity
                color = hsv_to_rgb((h, s, v))
        else:
            intensity = math.ceil(intensity * 31)
            (r, g, b) = color
            color = (r, g, b, intensity)
        self.leds[pos] = color

    def _color_wheel(self, pos, intensity=1.0):
        h = pos / 360
        return hsv_to_rgb((h, 1, intensity))

    def clear(self):
        '''Clears all LEDs.'''
        for n in range(self.count):
            self._set_led(COLOR_BLACK, 0, n)
        self.leds.write()

    def set_led(self, color, intensity=1.0, pos=None):
        if pos:
            self._set_led(color, intensity, pos)
        else:
            for n in range(self.count):
                self._set_led(color, intensity, n)
        self.leds.write()

    def color_cycle(self, wait=10, loop=4, intensity=1.0):
        for i in range(loop):
            for j in range(360):
                for k in range(self.count):
                    index = (j * 360 // self.count) + k
                    self._set_led(self._color_wheel(index), intensity, k)
                self.leds.write()
                time.sleep_ms(wait)