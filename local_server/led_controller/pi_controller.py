from .led_controller import LedController
import board
import neopixel
import time
import threading

_PIXEL_PIN = board.D18
_NUM_PIXELS = 200
_ORDER = neopixel.GRB


class PiController(LedController):
    """A working LED controller for Raspberry Pi devices.

    Can only be used on a Raspberry Pi."""

    pin: int
    count: int
    order: str

    _pixels: neopixel.NeoPixel

    def __init__(self):
        self.pin = _PIXEL_PIN
        self.count = _NUM_PIXELS
        self.order = _ORDER
        self.pixels = neopixel.NeoPixel(
            self.pin,
            self.count,
            pixel_order=self.order,
            auto_write=False,
            brightness=0.2,
        )
        self.pixels.fill((0, 0, 0))
        self._start_pixel_show_timer()
        super().__init__()

    def _start_pixel_show_timer(self):
        self._show_pixels()
        threading.Timer(0.5, self._start_pixel_show_timer).start()

    def _show_pixels(self):
        self.pixels.show()

    def setPixels(self, data: dict[int, tuple[int, int, int]]) -> None:
        for i in data:
            rgb = data[i]
            if rgb is None:
                continue
            if self.order == neopixel.RGB:
                self.pixels[i] = rgb
            else:
                self.pixels[i] = (rgb[1], rgb[0], rgb[2])
        self._show_pixels()


# Neopixel
# pixels = neopixel.NeoPixel(
#     _PIXEL_PIN,
#     _NUM_PIXELS,
#     pixel_order=_ORDER,
#     auto_write=False,
#     brightness=0.2,
# )

# def wheel(pos):
#   # Input a value 0 to 255 to get a color value.
#   # The colours are a transition r - g - b - back to r.
#   if pos < 0 or pos > 255:
#   r = g = b = 0
#   elif pos < 85:
#   r = int(pos * 3)
#   g = int(255 - pos * 3)
#   b = 0
#   elif pos < 170:
#   pos -= 85
#   r = int(255 - pos * 3)
#   g = 0
#   b = int(pos * 3)
#   else:
#   pos -= 170
#   r = 0
#   g = int(pos * 3)
#   b = int(255 - pos * 3)
#   return (r, g, b) if _ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


# def rainbow_cycle(wait):
#   for j in range(255):
#   for i in range(_NUM_PIXELS):
#     pixel_index = (i * 256 // _NUM_PIXELS) + j
#     pixels[i] = wheel(pixel_index & 255)
#   pixels.show()
#   time.sleep(wait)


# while True:
#   # Comment this line out if you have RGBW/GRBW NeoPixels
#   pixels.fill((255, 0, 0))
#   # Uncomment this line if you have RGBW/GRBW NeoPixels
#   # pixels.fill((255, 0, 0, 0))
#   pixels.show()
#   time.sleep(1)

#   # Comment this line out if you have RGBW/GRBW NeoPixels
#   pixels.fill((0, 255, 0))
#   # Uncomment this line if you have RGBW/GRBW NeoPixels
#   # pixels.fill((0, 255, 0, 0))
#   pixels.show()
#   time.sleep(1)

#   # Comment this line out if you have RGBW/GRBW NeoPixels
#   pixels.fill((0, 0, 255))
#   # Uncomment this line if you have RGBW/GRBW NeoPixels
#   # pixels.fill((0, 0, 255, 0))
#   pixels.show()
#   time.sleep(1)

#   rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

# firstArg = sys.argv[1]
# print("Arg: ", firstArg)
# jsonPayload = json.loads(firstArg)
# print("Json payload: ", jsonPayload)

# rgb = jsonPayload

# pixels = neopixel.NeoPixel(board.D18, 200, brightness=1)

# for _i in range(5):
#     print("%s Blackout" % datetime.now())
#     pixels.fill((0, 0, 0))
#     time.sleep(0.5)

#     print("%s Show LED" % datetime.now())
#     # G, R, B
#     pixels.fill((rgb[1], rgb[0], rgb[2]))
#     pixels.show()
#     time.sleep(0.5)
#     print("--------------")
