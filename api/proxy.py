import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. API Key Setup
            api_key = os.environ.get('OPENROUTER_API_KEY')
            
            # 2. Read and Validate Body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            if not body:
                print("Error: Empty request body")
                self.send_error(400, "Empty request")
                return

            # 3. Call OpenRouter with REQUIRED headers
            url = "https://openrouter.ai/api/v1/chat/completions"
            req = urllib.request.Request(url, data=body, method='POST')
            
            # These headers prevent the 404/403 errors
            req.add_header('Authorization', f"Bearer {api_key}")
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'LitePedia-App')
            req.add_header('HTTP-Referer', 'https://litepedia.vercel.app')
            
            with urllib.request.urlopen(req) as response:
                response_data = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
                
        except Exception as e:
            # This captures the exact error in your Vercel Logs
            print(f"CRITICAL PYTHON ERROR: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
