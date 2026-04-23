from pydantic import BaseModel

class UserSignup(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    receiver_id: int
    encrypted_message: str
    
class MessageCreate(BaseModel):
    receiver_id: int
    encrypted_message: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    encrypted_message: str

    class Config:
        from_attributes = True   # ✅ instead of orm_mode        
        
class GroupCreate(BaseModel):
    name: str
    members: list[int]


class GroupMessageResponse(BaseModel):
    id: int
    group_id: int
    sender_id: int
    message: str

    class Config:
        from_attributes = True        