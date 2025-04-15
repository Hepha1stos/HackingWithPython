from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import base64

class Listener(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = urlparse(self.path).query
            params = parse_qs(query)
            cookie_encoded = params.get("cookie", [""])[0]

            try:
                cookie_decoded = base64.b64decode(cookie_encoded).decode()
            except Exception as e:
                cookie_decoded = f"Fehler beim Dekodieren: {e}"

            print("\n--- Neue Anfrage ---")
            print("Pfad:", self.path)
            print("Kodierter Cookie:", cookie_encoded)
            print("Dekodierter Cookie:", cookie_decoded)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print("Fehler beim Verarbeiten der Anfrage:", e)
            self.send_response(500)
            self.end_headers()

print("🚀 Server läuft auf http://0.0.0.0:5000")
try:
    HTTPServer(('0.0.0.0', 5000), Listener).serve_forever()
except KeyboardInterrupt:
    print("\n👋 Server gestoppt.")
