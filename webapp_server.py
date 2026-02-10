from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='webapp', **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = 8000
print(f"🌐 Сервер запущен на http://localhost:{PORT}")
print(f"📱 Откройте в браузере для теста")
print("Нажмите Ctrl+C для остановки")

httpd = HTTPServer(('', PORT), MyHandler)
httpd.serve_forever()
