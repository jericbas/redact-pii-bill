import React, { useState } from 'react';

const TextRedactor = ({ onTextChanged }) => {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    setText(e.target.value);
    onTextChanged(e.target.value);
  };

  return (
    <div className="text-redactor-section">
      <h3>Input Text for Redaction</h3>
      <textarea
        rows="10"
        cols="50"
        placeholder="Enter sensitive text here..."
        value={text}
        onChange={handleChange}
      />
    </div>
  );
};

export default TextRedactor;
