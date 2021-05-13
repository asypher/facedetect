#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import os
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
from main.detect import get_face_detect_data
import ssl

define("port", default=12345, help="run on the given port", type=int)

class MainHandler(tornado.websocket.WebSocketHandler):

    @classmethod
    def route_urls(cls):
        return [(r'/echo',cls, {}),]

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        image_data = get_face_detect_data(message)
        # logging.info("image read")
        if not image_data:
            image_data = message
        self.write_message(image_data)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/websocket", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liveface.settings")
    tornado.options.parse_command_line()
    
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("/etc/letsencrypt/live/asypher.tech/fullchain.pem",
                        "/etc/letsencrypt/live/asypher.tech/privkey.pem")
    http_server = tornado.httpserver.HTTPServer(tornado.web.Application(MainHandler.route_urls()), ssl_options=ssl_ctx)


    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()