import time
from machine import Pin
from neopixel import NeoPixel

class NeoPixels():
    """ This class initializes a block of NeoPixel RGB LEDs and offers some convenience
        functions and effects to use with the block.
    """

    COLOR_BLACK = (0, 0, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_CYAN = (0, 255, 255)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_YELLOW = (255, 255, 0)

    def __init__(self, pin, size):
        """Initializes a block of NeoPixel LEDs.

        Parameters
        ----------
        pin : integer
            The pin to which the NeoPixel Blocks are connected
        size : type
            The size of the NeoPixel Block
        """
        self.np = NeoPixel(Pin(pin, Pin.OUT), size)
        self.n = size

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

    def clear(self):
        """Clears all NeoPixels."""
        for i in range(self.n):
            self.np[i] = self.COLOR_BLACK
        self.np.write()

    def set_color(self, color, pos=None):
        """Sets all NeoPixels to a specific color, given as RGB.

        Parameters
        ----------
        color: tuple or string
            The color of the NeoPixel, either as a RGB tuple or a RGB hex value
            Example:
                set_color("123456")
                set_color((16, 16, 16))
        pos : integer
            The number of the NeoPixel in the array that is to be set to the color
        """
        if type(color) is str:
            color = self.hex_to_rgb(color)
        if pos is None:
            for i in range(self.n):
                self.np[i] = color
        else:
            self.np[pos] = color
        self.np.write()

    def bounce(self, color, wait=10, repeats=4):
        """Bounces an empty light from one end of the NeoPixel Block to the other.

        Parameters
        ----------
        color: tuple or string
            The color of the NeoPixel, either as a RGB tuple or a RGB hex value
            Example:
                bounce("123456")
                bounce((16, 16, 16))
        wait : integer
            How long to wait in ms between refreshing.
            Default is 10 ms
        repeats: integer
            Number of repeats
            Default is 4
        """
        if type(color) is str:
            color = self.hex_to_rgb(color)
        for i in range(repeats * self.n):
            for j in range(self.n):
                self.np[j] = color
            if (i // self.n) % 2 == 0:
                self.np[i % self.n] = self.COLOR_BLACK
            else:
                self.np[self.n - 1 - (i % self.n)] = self.COLOR_BLACK
                self.np.write()
            time.sleep_ms(wait)

    def cycle(self, color, wait=10, repeats=4):
        """Cycles a light down a length of the NeoPixel block.

        Parameters
        ----------
        color: tuple or string
            The color of the NeoPixel, either as a RGB tuple or a RGB hex value
            Example:
                cycle("123456")
                cycle((16, 16, 16))
        wait : integer
            How long to wait in ms between refreshing.
            Default is 10 ms
        repeats: integer
            Number of repeats
            Default is 4
        """
        if type(color) is str:
            color = self.hex_to_rgb(color)
        for i in range(repeats * self.n):
            for j in range(self.n):
                self.np[j] = self.COLOR_BLACK
            self.np[i % self.n] = color
            self.np.write()
            time.sleep_ms(wait)

    def wheel(self, pos):
        """Input a value 0 to 255 to get a color value.
        The colours are a transition r - g - b - back to r.

        Parameters
        ----------
        pos : integer
            Position of the color in the Colour wheel.
        """
        if pos < 0 or pos > 255:
            return self.COLOR_BLACK
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self, wait=10):
        """Cycles all NeoPixels in the block through the color wheel

        Parameters
        ----------
        wait : integer
            How long to wait in ms between refreshing.
            Default is 10 ms
        """
        for j in range(255):
            for i in range(self.n):
                rc_index = (i * 256 // self.n) + j
                self.np[i] = self.wheel(rc_index & 255)
            self.np.write()
            time.sleep_ms(wait)
