import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import TextRedactor from './components/TextRedactor';
import ResultDisplay from './components/ResultDisplay';

const App = () => {
  const [redactedText, setRedactedText] = useState('');
  const [fileResult, setFileResult] = useState(null);
  const [status, setStatus] = useState('Idle');
  const [inputText, setInputText] = useState('');

  const handleTextRedact = async () => {
    setStatus('Processing text...');
    try {
      const response = await fetch('http://localhost:8000/redact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setRedactedText(data.redacted_text);
      setStatus('Success');
    } catch (error) {
      console.error('Error:', error);
      setStatus('Error');
    }
  };

  const handleFileUpload = async (file) => {
    setStatus('Processing file...');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/redact-file', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setFileResult(data.redacted_text);
      setStatus('Success');
    } catch (error) {
      console.error('Error:', error);
      setStatus('Error');
    }
  };

  return (
    <div className="container">
      <h1>PII Redaction Tool</h1>
      
      <div className="input-group">
        <FileUpload onFileSelected={handleFileUpload} />
        <hr />
        <TextRedactor onTextChanged={(val) => setInputText(val)} />
        <button onClick={handleTextRedact}>Redact Text</button>
      </div>

      <hr />
      
      <div className="output-group">
        {inputText && <ResultDisplay result={redactedText} status={status} />}
        {fileResult && <ResultDisplay result={fileResult} status={status} />}
      </div>
    </div>
  );
};

export default App;
