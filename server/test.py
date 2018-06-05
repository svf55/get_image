#!/usr/bin/env python
import unittest

import io
import tornado
from PIL import Image
from tornado import websocket
from tornado.testing import AsyncHTTPTestCase

from generators import gen_image_from_file, gen_image_pil
from tornado_server import MainHandler

import os
import sys
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..', 'proto'))
import get_image_pb2


class TestGenerators(unittest.TestCase):

    def test_gen_image_from_file(self):
        file_name = os.path.join(BASE_DIR, 'images/pic.jpg')
        max_width = 200
        max_height = 100
        image = gen_image_from_file(file_name, image_max_width=max_width, image_max_height=max_height)
        self.assertTrue(isinstance(image, Image.Image))
        self.assertTrue(image.width <= max_width)
        self.assertTrue(image.height <= max_height)

        max_width = 200
        image = gen_image_from_file(file_name, image_max_width=max_width)
        self.assertTrue(isinstance(image, Image.Image))
        self.assertTrue(image.width <= max_width)

        max_height = 150
        image = gen_image_from_file(file_name, image_max_height=max_height)
        self.assertTrue(isinstance(image, Image.Image))
        self.assertTrue(image.height <= max_height)

        image = gen_image_from_file(file_name)
        self.assertTrue(isinstance(image, Image.Image))

    def test_gen_image_from_pil(self):
        width = 200
        height = 200
        image = gen_image_pil(image_max_width=width, image_max_height=height)
        self.assertTrue(isinstance(image, Image.Image))
        self.assertTrue(image.width == width)
        self.assertTrue(image.height == height)

        width = 200
        image = gen_image_pil(image_max_width=width)
        self.assertTrue(isinstance(image, Image.Image))
        self.assertTrue(image.width == width)

        height = 200
        image = gen_image_pil(image_max_height=height)
        self.assertTrue(isinstance(image, Image.Image))
        self.assertTrue(image.height == height)

        image = gen_image_pil()
        self.assertTrue(isinstance(image, Image.Image))


class TestWebSockets(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = tornado.web.Application([
            (r'/', MainHandler)
        ])
        return app

    @tornado.testing.gen_test
    def test_websocket(self):
        ws_url = "ws://localhost:" + str(self.get_http_port()) + "/"
        ws_client = yield tornado.websocket.websocket_connect(ws_url)

        client_request = get_image_pb2.ClientRequest()
        client_request.image_generator = 'file'
        client_request.image_gray = True
        message = client_request.SerializeToString()

        ws_client.write_message(message, binary=True)
        response = yield ws_client.read_message()

        server_response = get_image_pb2.ServerResponse()
        server_response.ParseFromString(response)

        bio = io.BytesIO(server_response.image_byte)
        bio.seek(0)

        image = Image.open(bio)
        self.assertEqual(image.mode, 'L')


if __name__ == '__main__':
    unittest.main()

