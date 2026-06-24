import sys
import os

# Adds the root project folder to Python's path
# so pytest can find app.py, db.py, models/ etc.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
