from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class ResumeInput(BaseModel):
    text: str

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
        return {"summary": result}
    except Exception as e:
        return {"error": str(e)}
