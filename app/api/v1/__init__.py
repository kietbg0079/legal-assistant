from fastapi import APIRouter
from http import HTTPStatus
from app.schema import (
    ChatMessageRequest, 
    UserInfoSchema
)
from pydantic import BaseModel
from datetime import date
from app.schema import UserInfoSchema
from app.core import LegalAssistant
from app.constant import MONGO_DB

v1_router = APIRouter(prefix="/v1")

@v1_router.get("/")
async def root():
    return {
        "status": HTTPStatus.OK,
    }

@v1_router.post("/chat")
async def chat(request: ChatMessageRequest):
    conversation_id_str = str(request.conversation_id)
    assistant = LegalAssistant(
        user_id=request.user_id,
        conversation_id=conversation_id_str
    )
    
    response = await assistant.chat(request.message)
    return {
            "message": response["response"],
            "conversation_id": conversation_id_str
        }

class CreateConversationSchema(BaseModel):
    user_id: str

@v1_router.post("/create_conversation")
async def create_conversation(request: CreateConversationSchema):
    conversation_id = MONGO_DB.init_conversation(
        user_id=request.user_id
    )
    return {
            "conversation_id": conversation_id,
            "welcome_message": "Welcome to the chatbot! How can I help you today?"
        }

class CreateConversationSchema(BaseModel):
    conversation_id: str

@v1_router.post("/get_conversation")
async def get_conversation(request: CreateConversationSchema):
    messages = MONGO_DB.get_messages_from_conversation_id(
        conversation_id=request.conversation_id
    )
    return {
            "messages": messages
        }

class RegisterUserSchema(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    birth: date
    gender: str
    nationality: str

@v1_router.post("/register_user")
async def register_user(request: RegisterUserSchema):
    user_info = UserInfoSchema(
        first_name=request.first_name,
        last_name=request.last_name,
        birth=request.birth,
        gender=request.gender,
        nationality=request.nationality
    )

    cursor = MONGO_DB.add_user(
        user_id=request.user_id,
        user_info=user_info
    )
    if cursor:
        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": "john_doe123"
        }
    else:
        return  {
            "success": False,
            "message": "User ID already exists or invalid data provided"
        }
        
class CheckUserIDSchema(BaseModel):
    user_id: str

@v1_router.post("/check_user_id")
async def check_user_id(request: CheckUserIDSchema):
    user_info = MONGO_DB.query_user_by_id(user_id=request.user_id)
    if user_info:
        conversation_ids = MONGO_DB.get_conversation_ids_from_user_id(
            user_id=request.user_id
        )
        return {
            "existed": True, 
            "conversation_ids": conversation_ids,
            **user_info.__dict__
        }
    else:
        return {
            "existed": False
        }