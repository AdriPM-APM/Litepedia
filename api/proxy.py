import os
import json
from http.server import BaseHTTPRequestHandler
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read request from your website
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        # 2. Forward to OpenRouter with the SECRET KEY
        url = "https://openrouter.ai/api/v1/chat/completions"
        req = urllib.request.Request(url, data=body, method='POST')
        
        # This pulls the key from Vercel's secure environment settings
        req.add_header('Authorization', f"Bearer {os.environ.get('OPENROUTER_API_KEY')}")
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req) as response:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
