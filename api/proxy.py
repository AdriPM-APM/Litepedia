from http.server import BaseHTTPRequestHandler
import os
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Log the state of the key to Vercel Logs
        api_key = os.environ.get('OPENROUTER_API_KEY')
        print(f"DEBUG: Key exists: {api_key is not None}")
        
        # 2. Return a 200 OK immediately to verify the server is running
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # 3. Send back the status
        response = {"status": "success", "key_found": api_key is not None}
        self.wfile.write(json.dumps(response).encode())
