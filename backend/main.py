from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from typing import List
from backend.pii_processor import redact_text
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Redact PII Bill API")

OUTPUT_DIR = "redacted_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.get("/")
async def root():
    return {"message": "Redact PII Bill API is running"}

@app.post("/redact")
async def redact_pii(text_data: dict):
    # Supporting a simple JSON text input first for testing the logic
    text = text_data.get("text", "")
    if not text:
        return {"error": "No text provided"}
    
    redacted_text = redact_text(text)
    return {"original": text, "redacted": redacted_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
