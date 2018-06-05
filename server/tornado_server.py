#!/usr/bin/env python
import io
import os
import sys
import logging
import socket
import tornado.websocket
import tornado.ioloop
from tornado.options import define, options
from generators import gen_image_pil, gen_image_from_file
from PIL.ImageOps import grayscale

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..', 'proto'))
import get_image_pb2


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self._logger = logging.getLogger(__name__)

    def check_origin(self, origin):
        return True

    def open(self):
        self._logger.info("A client connected.")

    def on_close(self):
        self._logger.info("A client disconnected")

    def on_message(self, message):
        client_request = get_image_pb2.ClientRequest()
        client_request.ParseFromString(message)

        max_size_kwargs = {}
        if client_request.HasField('image_max_width'):
            if client_request.image_max_width <= 0:
                self._logger.error('Request error: image_max_width must be positive!')
                self.send_error()
                return
            max_size_kwargs['image_max_width'] = client_request.image_max_width

        if client_request.HasField('image_max_height'):
            if client_request.image_max_height <= 0:
                self._logger.error('Request error: image_max_height must be positive!')
                self.send_error()
                return
            max_size_kwargs['image_max_height'] = client_request.image_max_height

        if client_request.image_generator == 'file':
            file_name = os.path.join(BASE_DIR, 'images/pic.jpg')
            image = gen_image_from_file(file_name, **max_size_kwargs)
        elif client_request.image_generator == 'PIL':
            image = gen_image_pil(**max_size_kwargs)
        else:
            self._logger.error('Request error: unknown image generator: %s', client_request.image_generator)
            self.send_error()
            return

        if client_request.image_gray:
            image = grayscale(image)

        img_bytes_io = io.BytesIO()
        image.save(img_bytes_io, format='JPEG')
        image_byte = img_bytes_io.getvalue()

        server_response = get_image_pb2.ServerResponse()
        server_response.image_file_name = 'pic.jpg'
        server_response.image_byte = image_byte

        self.write_message(server_response.SerializeToString(), binary=True)


if __name__ == "__main__":
    define('port', default=8888, help='run on the given port', type=int)

    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    myip = socket.gethostbyname(socket.gethostname())
    logging.info("\n\n*** Websocket Server Started at %s ***\n" % myip)
    tornado.ioloop.IOLoop.instance().start()

