import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app

# Export the Flask app for Vercel
# Vercel will automatically handle WSGI
app = app
