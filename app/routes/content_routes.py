from fastapi import FastAPI, HTTPException, APIRouter
from models import PromptRequest
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
content_router=APIRouter()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

@content_router.post("/content/generate")
async def generate_content_endpoint(request: PromptRequest):
    print("Hello")
    """
    Accept a prompt from the user, send it to Google Generative AI, and return the response.
    """
    try:
        response = model.generate_content(request.prompt)
       
        generated_text = response.candidates[0].content.parts[0].text 

        return {"prompt": request.prompt, "response": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")