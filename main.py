from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ResumeInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_resume(data: ResumeInput):
    return {"summary": f"Received resume with {len(data.text)} characters."}
