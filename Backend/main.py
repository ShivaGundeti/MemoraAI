from fastapi import HTTPException
from fastapi import FastAPI
import database
from models import NoteCreate
from bson import ObjectId
from bson.errors import InvalidId
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.close()

@app.get("/health")
async def health():
    return {"status": "ok", "message": "MemoraAI backend is running!"}

@app.post("/api/document")
async def create_note(note: NoteCreate):
    note_dict = note.model_dump()
    note_dict["userid"] = "user_123"
    await database.db.notes.insert_one(note_dict)
    return {"message": "Notes Saved!!"} 

@app.get("/api/document/{userid}")
async def get_note(userid: str):
 
        cursor = database.db.notes.find({"userid": userid})
        documents = await cursor.to_list(length=100)
        print(len(documents))
        if len(documents) == 0:
            raise HTTPException(status_code=404,detail="Notes not found")
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return {"Notes": documents}



@app.put("/api/document/{id}")
async def update_notes(note: NoteCreate,id: str):
    try:
        updateNotes = await database.db.notes.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"title":note.title}}
        )
        if updateNotes.modified_count == 0:
            raise HTTPException(status_code=404,detail="Notes Not Found!!")
        return {"Message":"Updated Notes successfully"}
    except InvalidId:
        raise HTTPException(status_code=400,detail="Invalid Notes ID")

@app.delete("/api/document/{id}")
async def delete_note(id:str):
    try: 
        deleteNote = await database.db.notes.delete_one({"_id":ObjectId(id)})
        if deleteNote.deleted_count == 0:
            raise HTTPException(status_code=404,detail="Notes not found")
        return {"Message":"Deleted Successfully"}
    except InvalidId:
        raise HTTPException(status_code=400,detail="Invalid ID")