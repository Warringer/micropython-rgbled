import math, time
from machine import Pin
from neopixel import NeoPixel
from apa102 import APA102

def rgb_to_hsv(rgb_color):
    """Converts colors from the RGB color space to the HSV color space.

    Parameters
    ----------
    rgb_color : tuple (r, g, b)
        Color in the RGB color space

    Returns
    -------
    tuple (h, s, v)
        Color in the HSV color space

    """
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
    """Converts colors from the HSV color space to the RGB color space.

    Parameters
    ----------
    hsv_color : tuple (h, s, v)
        Color in the HSV color space

    Returns
    -------
    tuple (r, g, b)
        Color in the RGB color space

    """
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
        """Initializes the LED driver

        Parameters
        ----------
        count : int
            Required
            Number of LEDs in the LED strip/matrix
        data : int
            Required
            Pin of the Data Line
        clock : int
            Optional
            Pin for the clock Line.
            Used only by the APA102
        apa102c : bool
            Optional
            Used only by the APA102C to reorder the color sequence
        """
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
        """Internal method to set individual LEDs to a coloir

        Parameters
        ----------
        color : tuple (r, g, b) or string
            Required
            Color of the LED in the RGB color space
            Either as (r, g, b) tuple or as a Hexadecimal string 'AA55CC'
        intensity : float
            Required
            Intensity of the color/LED from 0 to 1
        pos : int
            Required
            Position of the LED in the LED strip/matrix
        """
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
        """Short summary.

        Parameters
        ----------
        pos : int
            Required
            Position of the color in the HSV color wheel
            from 0 to 360 degrees
        intensity : float
            Intensity of the color/LED from 0 to 1

        Returns
        -------
        tuple (r, g, b)
            Color in the RGB color space

        """
        if pos > 360:
            pos = pos - 360
        h = pos / 360
        return hsv_to_rgb((h, 1, intensity))

    def clear(self):
        """Clears all LEDs and sets them to Black"""
        for n in range(self.count):
            self._set_led(COLOR_BLACK, 0, n)
        self.leds.write()

    def set_led(self, color, intensity=1.0, pos=None):
        """Set one or all LEDs to a color.

        Parameters
        ----------
        color : tuple (r, g, b) or string
            Required
            Color of the LED in the RGB color space
            Either as (r, g, b) tuple or as a Hexadecimal string 'AA55CC'
        intensity : float
            Intensity of the color/LED from 0 to 1
        pos : int
            Position of the LED in the LED strip/matrix
        """
        if pos:
            self._set_led(color, intensity, pos)
        else:
            for n in range(self.count):
                self._set_led(color, intensity, n)
        self.leds.write()

    def color_cycle(self, wait=10, loop=4, intensity=1.0):
        """Cycles all LEDs through the HSV color space

        Parameters
        ----------
        wait : int
            How long to wait between refreshing the LEDs
        loop : int
            How many times the cycle is looped
        intensity : float
            Intensity of the color/LED from 0 to 1
        """
        for i in range(loop):
            for j in range(360):
                for k in range(self.count):
                    pos = j + 10 * k
                    self._set_led(self._color_wheel(pos), intensity, k)
                self.leds.write()
                time.sleep_ms(wait)

    def cycle(self, color, intensity=1.0, wait=10, loop=4, invert=False):
        """Cycles a single LED down the LED strip/matrix. The LED is either
           turned off (color black), while all other LEDs are set to a color
           or all LEDs are turned off with only one color.add()

        Parameters
        ----------
        color : tuple (r, g, b) or string
            Required
            Color of the LED in the RGB color space
            Either as (r, g, b) tuple or as a Hexadecimal string 'AA55CC'
        intensity : float
            Intensity of the color/LED from 0 to 1
        wait : int
            How long to wait between refreshing the LEDs
        loop : int
            How many times the cycle is looped
        invert : bool
            Inverts the display

        Returns
        -------
        type
            Description of returned object.

        """
        clear = COLOR_BLACK
        clear_intensity = 0
        if invert:
            clear = color
            clear_intensity = intensity
            color = COLOR_BLACK
            intensity = 0
        for i in range(loop * self.count):
            for j in range(self.count):
                if invert:
                    self._set_led(color, intensity, j)
                else:
                    self._set_led(COLOR_BLACK, 0, j)
            if invert:
                self._set_led(COLOR_BLACK, 0, i % self.count)
            else:
                self._set_led(color, intensity, i % self.count)
            self.leds.write()
            time.sleep_ms(wait)
