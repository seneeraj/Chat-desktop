from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from .database import Base


# =========================
# 👤 USER
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    public_key = Column(Text, nullable=True)
    approval_status = Column(String, default="PENDING")
    role = Column(String, default="USER")
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# 💬 MESSAGE
# =========================
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer)
    encrypted_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    file_url = Column(String, nullable=True)
    file_type = Column(String, nullable=True)  # image / pdf / file
    file_name = Column(String, nullable=True)


# =========================
# 👥 GROUP
# =========================
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


# =========================
# 👥 GROUP MEMBERS
# =========================
class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer)
    user_id = Column(Integer)
    role = Column(String, default="MEMBER")  # ADMIN / MEMBER


# =========================
# 💬 GROUP MESSAGE
# =========================
class GroupMessage(Base):
    __tablename__ = "group_messages"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer)
    sender_id = Column(Integer)
    message = Column(String)