import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
from tornado.options import define, options
import time
import ssl
define('port', default=12345, help='port to listen on')

class web_socket_handler(ws.WebSocketHandler):
    '''
    This class handles the websocket channel
    '''
    @classmethod
    def route_urls(cls):
        return [(r'/webserver',cls, {}),]
    
    def simple_init(self):
        self.last = time.time()
        self.stop = False
    
    def open(self):
        '''
            client opens a connection
        '''
        self.simple_init()
        print("New client connected")
        self.write_message("You are connected")
        
    def on_message(self, message):
        '''
            Message received on the handler
        '''
        print("received message {}".format(message))
        self.write_message("You said {}".format(message))
        self.last = time.time()
    
    def on_close(self):
        '''
            Channel is closed
        '''
        print("connection is closed")
        self.loop.stop()
    
    def check_origin(self, origin):
        return True

def initiate_server():
    #create a tornado application and provide the urls

    
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("/etc/letsencrypt/live/asypher.tech/fullchain.pem",
                        "/etc/letsencrypt/live/asypher.tech/privkey.pem")
    http_server = tornado.httpserver.HTTPServer(tornado.web.Application(web_socket_handler.route_urls()), ssl_options=ssl_ctx)


    http_server.listen(12345)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == '__main__':
    initiate_server()