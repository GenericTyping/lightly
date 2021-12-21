from typing import Protocol, Callable


class LedController(Protocol):
    """
    A protocol for controlling the LEDs.

    Fields:
    - pin: int, the GPIO pin the LEDs are connected to.
    - count: int, the number of LEDs.
    - order: str, the order of the LEDs.

    Methods:
    - setPixels(pixels: list[tuple[int, int, int]]) -> None, sets the LEDs to the given colors.
    """

    # Define the three fields above
    pin: int
    count: int
    order: str

    def setPixels(self, pixels: dict[int, tuple[int, int, int]]):
        """Sets the LEDs at the given indices to the given colors."""
        print("Unimplemented method setPixels() called with", pixels)

    def buildPixels(
        self, buildColor: Callable[[int], tuple[int, int, int]]
    ) -> dict[int, tuple[int, int, int]]:
        """Runs the given pixel builder callback for each pixel in the chain
        and returns the resulting dictionary of pixels.

        The callback should take a single argument, which is the current pixel index.
        """
        pixels: dict[int, tuple[int, int, int]] = {}
        for i in range(self.count):
            pixel = buildColor(i)
            if pixel is not None:
                pixels[i] = pixel
        return pixels


# Neopixel
# pixels = neopixel.NeoPixel(
#   PIXEL_PIN,
#   NUM_PIXELS,
#   pixel_order=ORDER,
#   auto_write=False,
#   brightness=0.2,
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
#   return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


# def rainbow_cycle(wait):
#   for j in range(255):
#   for i in range(NUM_PIXELS):
#     pixel_index = (i * 256 // NUM_PIXELS) + j
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
