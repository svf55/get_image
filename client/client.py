#!/usr/bin/env python
import io
from PIL import Image
import logging
from websocket import create_connection, ABNF

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))
import get_image_pb2


class WebSocketClient(object):
    """
    Getting an image through a Websocket
    """
    def __init__(self, host_ws, port_ws):
        self.host_ws = host_ws
        self.port_ws = port_ws
        self._logger = logging.getLogger(__name__)

    def get_image(self, image_generator, image_max_width, image_max_height, image_gray):
        ws = create_connection('ws://' + self.host_ws + ':' + str(self.port_ws))

        client_request = get_image_pb2.ClientRequest()
        client_request.image_generator = image_generator
        if image_max_width:
            client_request.image_max_width = image_max_width
        if image_max_height:
            client_request.image_max_height = image_max_height
        client_request.image_gray = image_gray

        message = client_request.SerializeToString()

        ws.send(message, opcode=ABNF.OPCODE_BINARY)

        self._logger.info('Sent')
        self._logger.info('Receive...')

        data = ws.recv()
        server_response = get_image_pb2.ServerResponse()
        server_response.ParseFromString(data)

        bio = io.BytesIO(server_response.image_byte)
        bio.seek(0)

        image = Image.open(bio)

        self._logger.info('Save image %s', server_response.image_file_name)

        image.save(server_response.image_file_name)

        ws.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Websocket client')
    parser.add_argument('--host_ws', help='Websocket host, example: localhost', required=True)
    parser.add_argument('--port_ws', type=int, default=8888, help='Websocket port, example: 9500')
    parser.add_argument('--image_generator', default='PIL',
                        choices=['file', 'PIL'], help='Image generator', required=True)
    parser.add_argument('--image_max_width', type=int, help='Image max width (integer)')
    parser.add_argument('--image_max_height', type=int, help='Image max height (integer)')
    parser.add_argument('--image_gray', action='store_true', default=False, help='Image is gray')

    args = parser.parse_args()

    # Setup logging
    FORMAT = '%(asctime)s %(process)d %(levelname)s %(name)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    # Getting an image through a Websocket
    WebSocketClient(args.host_ws, args.port_ws).get_image(args.image_generator, args.image_max_width,
                                                          args.image_max_height, args.image_gray)

