import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

client = None
db = None

async def connect():
    global client, db
    try:
        MONGO_URL = os.getenv("MONGODB_URL")
        client = AsyncIOMotorClient(MONGO_URL)
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        db = client.MemoraAI
    except Exception as e:
        print("❌ Failed to connect to MongoDB. Error:")
        print(e)



async def close():
    global client
    client.close()