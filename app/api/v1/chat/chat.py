from app.api.v1 import v1_router
from app.schema import ChatMessageResponse, ChatMessageRequest


@v1_router.post("/chat")
async def chat(request: ChatMessageRequest):
    pass