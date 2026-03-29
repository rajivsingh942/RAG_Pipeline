#!/usr/bin/env python
"""
Smart RAG - Startup Script for Render Deployment
Handles both local and cloud deployment
"""
import os
import sys
import subprocess
import time
import signal
from pathlib import Path

# Get environment variables with defaults
PORT = int(os.getenv('PORT', '8000'))
API_HOST = os.getenv('API_HOST', '0.0.0.0')
FRONTEND_PORT = int(os.getenv('FRONTEND_PORT', '3000'))

# For Render, use the same port for both services
IS_RENDER = 'RENDER' in os.environ
if IS_RENDER:
    FRONTEND_PORT = PORT  # Use same port as API

print("\n" + "="*70)
print("Smart RAG - Application Startup")
print("="*70)
print(f"\n📍 Environment: {'Render Cloud' if IS_RENDER else 'Local'}")
print(f"🌐 API Host: {API_HOST}")
print(f"🔌 API Port: {PORT}")
print(f"🖥️  Frontend Port: {FRONTEND_PORT if not IS_RENDER else PORT}")

# Verify requirements are installed
print("\n✅ Checking dependencies...")
try:
    import fastapi
    import uvicorn
    import sentence_transformers
    print("✅ All dependencies installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Create data directories if they don't exist
data_dir = Path("backend/data")
data_dir.mkdir(parents=True, exist_ok=True)
print(f"✅ Data directory ready: {data_dir}")

# Process tracking
processes = []
stop_event = False

def signal_handler(sig, frame):
    """Handle SIGINT to gracefully shutdown"""
    global stop_event
    stop_event = True
    print("\n\n🛑 Shutting down...")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()
    print("✅ All services stopped")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Start backend
print(f"\n🚀 Starting Backend API...")
print(f"   Command: python backend/run.py")
backend_cmd = [
    sys.executable, 
    'backend/run.py'
]

# For Render, start backend in background
if IS_RENDER:
    backend_process = subprocess.Popen(backend_cmd)
    processes.append(backend_process)
    print(f"✅ Backend started (PID: {backend_process.pid})")
else:
    backend_process = subprocess.Popen(backend_cmd)
    processes.append(backend_process)
    print(f"✅ Backend started")

# Wait for backend to be ready
print("\n⏳ Waiting for backend to initialize...")
time.sleep(3)

# Start frontend
print(f"\n🚀 Starting Frontend Server...")
if IS_RENDER:
    # On Render, serve static files directly without opening browser
    frontend_cmd = [sys.executable, 'frontend_server.py']
    frontend_process = subprocess.Popen(
        frontend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
else:
    frontend_cmd = [sys.executable, 'frontend_server.py']
    frontend_process = subprocess.Popen(frontend_cmd)

processes.append(frontend_process)
print(f"✅ Frontend started")

# Display service URLs
print("\n" + "="*70)
if IS_RENDER:
    print("✨ Smart RAG is running on Render!")
    print("="*70)
    print(f"\n🌐 Your application URL:")
    print(f"   https://<your-render-url>.onrender.com")
    print(f"\n📊 API Documentation:")
    print(f"   https://<your-render-url>.onrender.com/docs")
    print(f"\n✅ Backend: http://0.0.0.0:{PORT}")
else:
    print("✨ Smart RAG is running locally!")
    print("="*70)
    print(f"\n🌐 Access the application:")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Backend:  http://localhost:8000")
    print(f"   API Docs: http://localhost:8000/docs")

print(f"\n📝 Press Ctrl+C to stop all services")
print("="*70 + "\n")

# Keep the main process alive
try:
    while not stop_event:
        time.sleep(1)
        # Check if any process died
        for proc in processes:
            if proc.poll() is not None:
                print(f"\n⚠️  A process has exited. Main loop continuing...")
except KeyboardInterrupt:
    signal_handler(None, None)
