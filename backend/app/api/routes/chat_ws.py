from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from datetime import datetime

from backend.app.core.encryption import encrypt_message
from backend.app.db.database import SessionLocal
from backend.app.db import models

router = APIRouter()

# Active connections
active_connections: Dict[int, WebSocket] = {}


# ==============================
# 🔥 Broadcast online users
# ==============================
async def broadcast_online_users():
    online_users = list(active_connections.keys())

    for user_id, ws in list(active_connections.items()):
        try:
            await ws.send_json({
                "type": "online_users",
                "users": online_users
            })
        except Exception:
            active_connections.pop(user_id, None)


# ==============================
# 🔌 WebSocket Endpoint
# ==============================
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):

    await websocket.accept()
    active_connections[user_id] = websocket

    print(f"✅ User {user_id} connected")

    await broadcast_online_users()

    try:
        while True:
            data = await websocket.receive_json()
            print("📩 Received:", data)

            event_type = data.get("type")
            receiver_id = data.get("receiver_id")

            # =========================
            # 💬 MESSAGE
            # =========================
            if event_type == "message":

                if not receiver_id:
                    print("⚠️ Missing receiver_id")
                    continue

                raw_message = data.get("message") or ""

                db = SessionLocal()

                try:
                    encrypted = encrypt_message(raw_message) if raw_message else ""

                    new_msg = models.Message(
                        sender_id=user_id,
                        receiver_id=receiver_id,
                        encrypted_message=encrypted,
                        file_url=data.get("file_url"),
                        file_type=data.get("file_type"),
                        file_name=data.get("file_name"),
                    )

                    db.add(new_msg)
                    db.commit()
                    db.refresh(new_msg)

                    print(f"✅ Message saved: {new_msg.id}")

                    payload = {
                        "type": "message",
                        "id": new_msg.id,
                        "sender_id": user_id,
                        "receiver_id": receiver_id,
                        "message": raw_message,
                        "file_url": data.get("file_url"),
                        "file_type": data.get("file_type"),
                        "file_name": data.get("file_name"),
                        "timestamp": str(datetime.utcnow())
                    }

                    # Send to receiver
                    if receiver_id in active_connections:
                        try:
                            await active_connections[receiver_id].send_json(payload)
                            print("📨 Sent to receiver")
                        except Exception:
                            active_connections.pop(receiver_id, None)
                    else:
                        print("📴 Receiver offline")

                    # Send back to sender
                    try:
                        await websocket.send_json(payload)
                    except Exception:
                        print("⚠️ Failed to send to sender")

                except Exception as e:
                    print("❌ DB ERROR:", e)

                finally:
                    db.close()

            # =========================
            # ✍️ TYPING
            # =========================
            elif event_type == "typing":

                if receiver_id in active_connections:
                    try:
                        await active_connections[receiver_id].send_json({
                            "type": "typing",
                            "sender_id": user_id
                        })
                    except Exception:
                        active_connections.pop(receiver_id, None)

            # =========================
            # 👁️ SEEN
            # =========================
            elif event_type == "seen":

                message_id = data.get("message_id")

                if receiver_id in active_connections:
                    try:
                        await active_connections[receiver_id].send_json({
                            "type": "seen",
                            "message_id": message_id
                        })
                    except Exception:
                        active_connections.pop(receiver_id, None)

    except WebSocketDisconnect:
        print(f"❌ User {user_id} disconnected")
        active_connections.pop(user_id, None)
        await broadcast_online_users()

    except Exception as e:
        print("❌ WebSocket ERROR:", e)
        active_connections.pop(user_id, None)
        await broadcast_online_users()
