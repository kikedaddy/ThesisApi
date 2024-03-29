#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import movement_master
import image_master

class S(BaseHTTPRequestHandler):
    move = movement_master.Steering()
    image = image_master.ImageReceiver()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>GET! " + self.image.getImage() + " </h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        if "speed" in post_data:
            speed = post_data.rsplit("=", -1)[1]
            print "Word: " + str(speed)
            self.move.setSpeed(float(speed))
        if "angle" in post_data:
            angle = post_data.rsplit("=", -1)[1]
            print "Word: " + str(angle)
            self.move.setAngle(float(angle))
        self._set_headers()
        self.wfile.write("<html><body><h1>POST! " + str(post_data) + " </h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()