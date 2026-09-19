from fastapi import FastAPI
from database import connect,close
from models import NoteCreate
app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect()
@app.on_event("shutdown")
async def shutdown():
    await close()

@app.get("/health")
async def health():
    return {"status": "ok", "message": "MemoraAI backend is running!"}

@app.post("/api/document")
async def create_note(note: NoteCreate):
    return note