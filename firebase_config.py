import os
import json
import firebase_admin
from firebase_admin import credentials, db, storage

firebase_cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
firebase_cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")

if firebase_cred_json:
    cred = credentials.Certificate(json.loads(firebase_cred_json))
elif firebase_cred_path:
    cred = credentials.Certificate(firebase_cred_path)
else:
    cred = credentials.Certificate(r"E:\Django\jobfusion\config\fir-chat-e3c87-firebase-adminsdk-fbsvc-0eba3f02b8.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get("FIREBASE_DATABASE_URL", "https://fir-chat-e3c87-default-rtdb.asia-southeast1.firebasedatabase.app"),
})

firebase_db = db.reference()
