from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
class NoteCreate(BaseModel):
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Noteresponse(NoteCreate):
    id: str = Field(alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders = {"ObjectId":str}
    )