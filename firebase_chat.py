from firebase_config import firebase_db
import time

def send_test_message(sender_id, receiver_id, text):
    room_id = f"room_{sender_id}_{receiver_id}"  # Simple deterministic room
    message_id = f"msg_{int(time.time())}"

    chat_ref = firebase_db.child("chats").child(room_id).child(message_id)

    chat_ref.set({
        "sender": sender_id,
        "receiver": receiver_id,
        "text": text,
        "timestamp": int(time.time())
    })

    print(f"✅ Message sent to room {room_id}")
