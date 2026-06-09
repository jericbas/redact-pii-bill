import React, { useState } from 'react';

const FileUpload = ({ onFileSelected }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      onFileSelected(selectedFile);
    }
  };

  return (
    <div className="upload-section">
      <h3>Upload Document (PDF, Image)</h3>
      <input type="file" accept="image/*, .pdf" onChange={handleFileChange} />
      {file && <p>Selected: {file.name}</p>}
    </div>
  );
};

export default FileUpload;
