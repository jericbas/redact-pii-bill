Here is a comprehensive project plan and technical solution for your redaction application, tailored for a clean implementation on Ubuntu.
### **Project Plan: Document Redaction & AI Analysis App**
**Phase 1: Foundation & Backend (Weeks 1-2)**
 * Set up the development environment on Ubuntu.
 * Develop the Python backend using FastAPI to handle file uploads.
 * Integrate **Microsoft Presidio** for PII detection and **Tesseract OCR** for image-to-text processing.
 * Implement the blocklist logic (reading names/addresses from a configuration file or environment variables).
**Phase 2: Frontend Development (Weeks 3-4)**
 * Scaffold a React front end using TypeScript.
 * Build the user interface for file uploading, selecting the desired output format (PDF, CSV, or Markdown), and displaying processing status.
**Phase 3: AI Integration & Storage (Week 5)**
 * Integrate a local AI layer via Ollama for advanced, context-aware PII detection (catching entities that pattern matching might miss).
 * Set up the local directory routing so redacted files are automatically saved to the designated output folder.
**Phase 4: Testing & Deployment (Week 6)**
 * Test with sample utility bills and credit card statements.
 * Containerize the application using Docker to ensure seamless deployment and execution on Ubuntu.
### **Suggested Solution & Architecture**
To make this highly performant, secure, and completely free, here is the recommended tech stack:
 * **Frontend:** **React + TypeScript**, built and managed using **Bun** for ultra-fast dependency resolution and serving.
 * **Backend:** **FastAPI (Python)**. It's fast, handles asynchronous file uploads beautifully, and plays natively with Python-based AI and NLP tools.
 * **Redaction Engine:** **Microsoft Presidio** (Analyzer and Anonymizer modules) combined with **spaCy** for natural language processing.
 * **OCR Engine:** **Tesseract OCR** (to extract text from image-based bills).
 * **Advanced AI Analysis:** **Ollama** running a local model (like Llama 3 or Mistral). Keeping the AI local ensures that sensitive bill information never leaves your machine, maintaining strict security.
 * **Deployment:** **Docker & Docker Compose** to bundle the frontend, backend, and OCR dependencies into a single, easily runnable package on Ubuntu.
### **Implementation Guide (Ubuntu)**
Here is how to set up the foundation of the project on your Ubuntu machine.
**1. Install System Prerequisites (OCR & Dependencies)**
Open your terminal and install Tesseract and Python tools:
```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev python3-pip python3-venv

```
**2. Set up the Backend (FastAPI + Presidio)**
Create a project directory and set up a Python virtual environment:
```bash
mkdir bill-redactor && cd bill-redactor
python3 -m venv venv
source venv/bin/activate

```
Install the required Python libraries:
```bash
pip install fastapi uvicorn presidio-analyzer presidio-anonymizer pytesseract pdf2image python-multipart

```
Download the necessary spaCy language model for Presidio:
```bash
python -m spacy download en_core_web_lg

```
**3. Set up the Frontend (React + TypeScript)**
In a new terminal tab (within your project folder), initialize the frontend. Using Bun makes this incredibly fast:
```bash
bun create vite frontend --template react-ts
cd frontend
bun install

```
### **How to Use and Run the Application**
**Configuration**
 1. **The Blocklist:** Create a file named blocklist.env in your backend directory. Add the specific names and addresses you want prioritized for removal:
   ```env
   TARGET_NAMES="John Doe, Jane Smith"
   TARGET_ADDRESSES="123 Main St, 456 Elm St"
   
   ```
 2. **The Output Directory:** Create a folder named redacted_outputs in the root of your project. The backend will be programmed to save all processed CSV, Markdown, or PDF files directly into this directory.
**Running the Stack**
During development, you will run the backend and frontend simultaneously.
 1. **Start the Backend (API):**
   From your backend directory with the virtual environment activated:
   ```bash
   uvicorn main:app --reload --port 8000
   
   ```
 2. **Start the Frontend (UI):**
   From your frontend directory:
   ```bash
   bun run dev
   
   ```
**Usage Flow**
 1. Open your browser to the local React address (usually http://localhost:5173).
 2. Upload your electric bill, credit card statement, or internet bill (PDF, JPG, or PNG).
 3. Select your desired output format from a dropdown (PDF, Markdown, or CSV).
 4. Click "Redact".
 5. The backend will use Tesseract to read the file, Presidio (and potentially Ollama) to scrub the text against standard PII patterns and your blocklist.env, and then automatically save the safe file to your redacted_outputs directory.
