from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class AIResponse(BaseModel):
    result: str
    type: str