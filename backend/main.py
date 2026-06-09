from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from typing import List
from backend.pii_processor import redact_text
from backend.ocr_service import extract_text_from_file
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
async def redact_pii_text(text_data: dict):
    """Endpoint for redacting text provided as JSON."""
    text = text_data.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    redacted_text = redact_text(text)
    return {"original": text, "redacted": redacted_text}

@app.post("/redact-file")
async def redact_pii_file(file: UploadFile = File(...)):
    """Endpoint for redacting text from an uploaded image or PDF file."""
    # Save the uploaded file temporarily
    temp_path = os.path.join(OUTPUT_DIR, "temp_" + file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Extract text using OCR service
        raw_text = extract_text_from_file(temp_path)
        
        # Redact text
        redacted_text = redact_text(raw_text)
        
        # Save redacted output
        output_filename = f"redacted_{file.filename}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(redacted_text)
            
        return {"filename": output_filename, "redacted_text": redacted_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
