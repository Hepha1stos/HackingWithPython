from http.server import BaseHTTPRequestHandler, HTTPServer

class Listener(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Cookie:", self.path)
        self.send_response(200)
        self.end_headers()

HTTPServer(('localhost', 5000), Listener).serve_forever()
