from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import subprocess
import os

HTML_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open(HTML_PATH, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/stream':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            process = subprocess.Popen(
                ['python3', '../hello_loop.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(__file__)
            )
            for line in process.stdout:
                msg = f"data: {line.strip()}\n\n"
                self.wfile.write(msg.encode('utf-8'))
                self.wfile.flush()
            process.wait()
            self.wfile.write(b"data: [done]\n\n")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # keep console quiet

if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 5000), Handler)
    print("Server running on http://0.0.0.0:5000")
    server.serve_forever()
