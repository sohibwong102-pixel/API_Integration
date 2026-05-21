from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    model: str
    messages: list


@router.post("/v1/chat/completions")
async def chat(req: ChatRequest):

    user_message = req.messages[-1]["content"]

    return {
        "choices": [
            {
                "message": {
                    "content": f"HALO GOBLIN 😭🔥\n\nLu bilang:\n{user_message}"
                }
            }
        ]
    }
