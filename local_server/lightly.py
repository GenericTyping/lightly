import sys
import json
import board
import neopixel
import time
import logging
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# Constants
HOST_NAME = '0.0.0.0'
SERVER_PORT = 1337

PIXEL_PIN = board.D18
NUM_PIXELS = 200
ORDER = neopixel.GRB

# HTTP
class LightlyLocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"status": "OK"}', "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), LightlyLocalServer)
    print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# Neopixel
pixels = neopixel.NeoPixel(
  PIXEL_PIN,
  NUM_PIXELS,
  pixel_order=ORDER,
  auto_write=False,
  brightness=0.2,
)

# def wheel(pos):
#   # Input a value 0 to 255 to get a color value.
#   # The colours are a transition r - g - b - back to r.
#   if pos < 0 or pos > 255:
#     r = g = b = 0
#   elif pos < 85:
#     r = int(pos * 3)
#     g = int(255 - pos * 3)
#     b = 0
#   elif pos < 170:
#     pos -= 85
#     r = int(255 - pos * 3)
#     g = 0
#     b = int(pos * 3)
#   else:
#     pos -= 170
#     r = 0
#     g = int(pos * 3)
#     b = int(255 - pos * 3)
#   return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


# def rainbow_cycle(wait):
#   for j in range(255):
#     for i in range(NUM_PIXELS):
#       pixel_index = (i * 256 // NUM_PIXELS) + j
#       pixels[i] = wheel(pixel_index & 255)
#     pixels.show()
#     time.sleep(wait)


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

firstArg = sys.argv[1]
print('Arg: ', firstArg)
jsonPayload = json.loads(firstArg)
print('Json payload: ', jsonPayload)

rgb = jsonPayload

pixels = neopixel.NeoPixel(board.D18, 200, brightness=1)

for _i in range(5):
  print('%s Blackout' % datetime.now())
  pixels.fill((0, 0, 0))
  time.sleep(0.5)

  print('%s Show LED' % datetime.now())
  # G, R, B
  pixels.fill((rgb[1], rgb[0], rgb[2]))
  pixels.show()
  time.sleep(0.5)
  print('--------------')
