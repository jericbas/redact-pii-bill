import React, { useState } from 'react';

const ResultDisplay = ({ result, status }) => {
  return (
    <div className="result-section">
      <h3>Result</h3>
      <p>Status: {status}</p>
      {result && (
        <div className="result-content">
          <p><strong>Redacted Text:</strong></p>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
