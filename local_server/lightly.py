#!/usr/bin/env python3
"""
This simple Python server is responsible for handling the requests
from the Node.js server (../server) and controlling the LEDs.
"""

import sys
import json
import time
import logging
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from led_controller.led_controller import LedController

controller: LedController = None

try:
    from led_controller.pi_controller import PiController

    controller = PiController()
except ImportError:
    from led_controller.mock_controller import MockController

    controller = MockController()

# Constants
HOST_NAME = "0.0.0.0"
SERVER_PORT = 1234

# HTTP
class LightlyLocalServer(BaseHTTPRequestHandler):
    def _writeResponse(self, data: str):
        self.wfile.write(bytes(data, "utf-8"))

    def _set_response(self, code: int, data: str = None):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if data != None:
            self._writeResponse(data)

    def do_GET(self):
        logging.info(
            "GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers)
        )
        self._set_response(200, dict_to_json({"success": True, "status": "ok"}))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        body = post_data.decode("utf-8")
        logging.info(
            "POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
            str(self.path),
            str(self.headers),
            body,
        )

        if self.path == "/set":
            try:
                # 'body' is a JSON list of lists, each containing 3 elements
                # representing a pixel's RGB values.
                #
                # Example:
                # [ [255, 0, 0], [0, 255, 0], [0, 0, 255] ]
                #
                # It needs to be converted to a list of tuples, each containing
                # 3 elements representing a pixel's RGB values.
                #
                # Example:
                # [ (255, 0, 0), (0, 255, 0), (0, 0, 255) ]
                #
                # However, some of the elements in the body might be null,
                # which means that that pixel should go unchanged.
                #
                # Example:
                # [ [255, 0, 0], null, [0, 0, 255] ]
                pixels: list[tuple[int, int, int]] = []
                for pixel in json.loads(body):
                    print("Pixel: ", pixel)
                    if pixel == None:
                        pixels.append(None)
                    else:
                        pixels.append(tuple(pixel))

                controller.setPixels(pixels)
                self._set_response(
                    200, dict_to_json({"success": True, "pixels": pixels})
                )
            except Exception as e:
                logging.error(e)
                logging.error(get_stack_trace())
                self._set_response(
                    400,
                    dict_to_json(
                        {
                            "success": False,
                            "action": "set",
                            "error": str(e),
                            "stack_trace": get_stack_trace(),
                        }
                    ),
                )
        else:
            # Unknown path
            self._set_response(404)


def runServer():
    server_address = (HOST_NAME, SERVER_PORT)
    httpd = HTTPServer(server_address, LightlyLocalServer)
    logging.info("Starting httpd on %s:%s", HOST_NAME, SERVER_PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping httpd")


def get_stack_trace():
    import traceback, sys

    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:  # i.e. an exception is present
        del stack[-1]  # remove call of full_stack, the printed exception
        # will contain the caught exception caller instead
    trc = "Traceback (most recent call last):\n"
    stackstr = trc + "".join(traceback.format_list(stack))
    if exc is not None:
        stackstr += "  " + traceback.format_exc().lstrip(trc)
    return stackstr


def dict_to_json(d):
    return json.dumps(d, sort_keys=True, indent=4)


if __name__ == "__main__":
    now = datetime.now()
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            # logging.FileHandler with file called "debug_${date as iso string}.log"
            logging.FileHandler(
                "debug_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".log",
                mode="w",
            ),
            logging.StreamHandler(),
        ],
    )
    runServer()
