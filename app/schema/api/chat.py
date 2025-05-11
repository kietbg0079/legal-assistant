from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

# Request schema
class ChatMessageRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier of the user")
    conversation_id: UUID = Field(..., description="UUID of the conversation")
    message: str = Field(..., min_length=1, description="Message content from the user")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "conversation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "message": "What are the legal requirements for starting an LLC in California?",
            }
        }

class AssistantMessage(BaseModel):
    message_id: UUID = Field(..., description="Unique identifier for the message")
    content: str = Field(..., description="Message content from the assistant")
    created_at: datetime = Field(..., description="Timestamp when message was created")
    
    # Sources/citations for legal advice
    citations: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Legal citations and references for the information provided"
    )
    
    # Additional helpful properties
    confidence_score: Optional[float] = Field(
        default=None, 
        description="Confidence score of the AI's response (0.0-1.0)"
    )
    suggested_follow_ups: Optional[List[str]] = Field(
        default=None,
        description="Suggested follow-up questions for the user"
    )

class ChatMessageResponse(BaseModel):
    conversation_id: UUID = Field(..., description="UUID of the conversation")
    user_message: Dict[str, Any] = Field(..., description="Original user message details")
    assistant_message: AssistantMessage = Field(..., description="Assistant's response")

