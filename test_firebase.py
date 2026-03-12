import sys, os

# ✅ Ensure the folder containing manage.py is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Import directly, because firebase_config.py is in the same directory
from firebase_config import firebase_db

def test_firebase():
    test_ref = firebase_db.child('test_connection')
    test_ref.set({
        'status': 'connected',
        'message': 'Firebase connection successful!'
    })
    print("✅ Data written to Firebase successfully.")
