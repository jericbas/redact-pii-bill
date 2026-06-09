from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from typing import List
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import pytesseract
from pdf2image import convert_from_bytes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
analyzer_engines = AnalyzerEngine()
anonymizer_engines = AnonymizerEngine()

OUTPUT_DIR = "redacted_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.post("/redact")
async def redact_document(file: UploadFile = File(...)):
    content = await file.read()
    
    # Simple logic for now: treat everything as text
    # In a real app, we'd handle PDF vs Image differently
    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = pytesseract.image_to_string(content)
    else:
        # Basic PDF text extraction for now
        images = convert_from_bytes(content)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)

    # Analyze PII
    results = analyzer_engines.analyze(text=text, entities=["PERSON", "LOCATION", "EMAIL_ADDRESS", "PHONE_NUMBER", "IBAN", "CREDIT_CARD"], language='en')
    
    # Anonymize
    anonymized_result = anonymizer_engines.anonymize(text=text, analyzer_results=results)
    redacted_text = anonymized_result.text

    # Save output
    output_filename = f"redacted_{file.filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_path, "w") as f:
        f.write(redacted_text)

    return {"message": "Success", "redacted_text": redacted_text, "path": output_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
