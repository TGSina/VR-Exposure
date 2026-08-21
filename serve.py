# serve.py
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import sys

class ReuseAddrServer(ThreadingHTTPServer):
    pass

ReuseAddrServer.allow_reuse_address = True

port = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
host = "0.0.0.0"

addr = (host, port)
print(f"Serving {addr} -> http://{host}:{port}/ (Ctrl-C to stop)")
try:
    with ReuseAddrServer(addr, SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopped")
except Exception as e:
    print("Server error:", e)
