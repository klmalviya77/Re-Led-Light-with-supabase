
import sys
import os

# Add the Re-Led-Light-with-supabase directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Re-Led-Light-with-supabase'))

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
