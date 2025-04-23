import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import openai

# Debug print (optional)
print("MONGO_URI:", os.getenv("MONGO_URI"))

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["resumate"]
records = db["entries"]

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI setup
app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class ResumeInput(BaseModel):
    text: str

# POST /analyze: Analyze and store resume
@app.post("/analyze")
def analyze_resume(data: ResumeInput):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a resume analysis assistant."},
                {"role": "user", "content": f"Analyze this resume:\n\n{data.text}\n\nGive strengths, weaknesses, and ideal job roles."}
            ]
        )
        result = response['choices'][0]['message']['content']

        records.insert_one({
            "type": "analyze",
            "resume_text": data.text,
            "summary": result,
            "timestamp": datetime.utcnow()
        })

        return {"summary": result}
    except Exception as e:
        return {"error": str(e)}

# GET /history: Retrieve recent resume analyses
@app.get("/history")
def get_history():
    try:
        entries = list(records.find({"type": "analyze"}).sort("timestamp", -1).limit(10))
        for entry in entries:
            entry["_id"] = str(entry["_id"])
            entry["timestamp"] = entry["timestamp"].isoformat()
        return JSONResponse(content={"history": entries})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
