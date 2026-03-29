# ============================================================================
# PROCFILE - Alternative deployment configuration (if not using Docker)
# ============================================================================
# This Procfile is used by Render for native (non-Docker) deployment
# Only needed if you don't deploy via Docker
# ============================================================================

# Start backend API on the port assigned by Render ($PORT)
web: cd backend && python run.py --host 0.0.0.0 --port $PORT
