import os
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import List, Dict

# Load configuration from environment
BLOCKLIST_PATH = os.getenv("BLOCKLIST_PATH", "backend/blocklist.env")

def get_pii_processor():
    # Initialize the analyzer and anonymizer
    # In a real app, we'd load specific entities or models based on config
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    return analyzer, anonymizer

def redact_text(text: str) -> str:
    """
    Detects and redacts PII from the provided text.
    """
    if not text:
        return ""
    
    analyzer, anonymizer = get_pii_processor()
    
    # Analyze text for PII entities
    results = analyzer.analyze(text=text, entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION", "IBAN", "CREDIT_CARD"])
    
    # Anonymize the results
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        anonymize_loc_dict={
            "LOCATION": {"type": "LOCATION", "original_value": "REDACTED_LOCATION"},
            "PERSON": {"type": "PERSON", "original_value": "REDACTED_NAME"},
            "EMAIL_ADDRESS": {"type": "EMAIL_ADDRESS", "original_value": "REDACTED_EMAIL"},
            "PHONE_NUMBER": {"type": "PHONE_NUMBER", "original_value": "REDACTED_PHONE"},
            "CREDIT_CARD": {"type": "CREDIT_CARD", "original_value": "REDACTED_CARD"},
            "IBAN": {"type": "IBAN", "original_value": "REDACTED_IBAN"}
        }
    )
    
    return anonymized_result.text

if __name__ == "__main__":
    sample_text = "My name is Jeric Bas and my email is jeric.raye.bas@gmail.com. I live in Manila."
    redacted = redact_text(sample_text)
    print(f"Original: {sample_text}")
    print(f"Redacted: {redacted}")
