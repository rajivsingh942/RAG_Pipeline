"""
Simple Local Web Server for Smart RAG App
Serves the frontend on http://localhost:3000 (or custom PORT)
"""

import http.server
import socketserver
import os
import webbrowser
import time
from pathlib import Path

# Get port from environment or use default
PORT = int(os.getenv("PORT", 3000))
IS_RENDER = "RENDER" in os.environ
FRONTEND_DIR = Path(__file__).parent / "frontend"


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        """Add headers to prevent caching"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.address_string()}] {format % args}")


def start_server():
    """Start the web server"""
    
    print("\n" + "=" * 70)
    print("Smart RAG App - Local Web Server")
    print("=" * 70)
    print(f"\n📂 Serving files from: {FRONTEND_DIR}")
    print(f"🌐 Open your browser at: http://localhost:{PORT}")
    print(f"\n✨ Features:")
    print(f"   - Modern web interface")
    print(f"   - Real-time chat with your documents")
    print(f"   - Streaming AI responses")
    print(f"   - Beautiful UI with animations")
    print(f"\n📋 Make sure backend is running:")
    print(f"   python backend/run.py")
    print(f"\n" + "=" * 70)
    print("\nStarting server...\n")
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ Server running on http://localhost:{PORT}")
            
            if not IS_RENDER:
                print(f"\n🌐 Opening in browser...")
                time.sleep(1)
                webbrowser.open(f"http://localhost:{PORT}")
            
            print(f"\n📌 Press Ctrl+C to stop the server\n")
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48 or e.errno == 98:  # Address already in use
            print(f"\n❌ ERROR: Port {PORT} is already in use!")
            print(f"\nTry one of these solutions:")
            print(f"  1. Close the other application using port {PORT}")
            print(f"  2. Wait a few seconds and try again")
            print(f"  3. Use a different port (edit this file and change PORT = {PORT})")
        else:
            print(f"\n❌ ERROR: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n\n✅ Server stopped")
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    start_server()
