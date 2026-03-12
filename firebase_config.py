import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate(r"E:\Django\jobfusion\config\fir-chat-e3c87-firebase-adminsdk-fbsvc-0eba3f02b8.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-chat-e3c87-default-rtdb.asia-southeast1.firebasedatabase.app',
})

firebase_db = db.reference()
