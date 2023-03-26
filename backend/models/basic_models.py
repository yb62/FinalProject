from pydantic import BaseModel

class ActionSuccessResponse(BaseModel):
    success: bool