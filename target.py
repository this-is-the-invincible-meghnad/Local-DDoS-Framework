import http.server
import socketserver

print("[*] Victim Server booting on port 8080...")
with socketserver.TCPServer(("127.0.0.1", 8080), http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()