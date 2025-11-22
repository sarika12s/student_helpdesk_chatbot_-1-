# Student Helpdesk Chatbot (AI-Based)

This project is an AI-powered Student Helpdesk Chatbot that answers college-related questions using a Retrieval-Augmented Generation (RAG) pipeline.  
It includes voice input, text-to-speech output, and a clean modern user interface.

---

## Features
- Voice Input (Speech-to-Text)
- Voice Output (Text-to-Speech)
- Modern UI (Blue Header + Chat Bubbles)
- Retrieval system using Sentence-Transformers
- BERT Question Answering model
- FAISS vector search
- Supports multiple FAQ documents
- Works fully offline after model download

---

## Project Structure
project/
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
├── static/
│ ├── style.css
│ └── script.js
├── data/
│ └── docs/
│ └── sample_faq.txt
└── utils/
├── retriever.py
├── qa_reader.py
└── convo_manager.py
## How to Run (Windows)

### 1. Create Virtual Environment
python -m venv venv

shell
Copy code

### 2. Activate Virtual Environment
venv\Scripts\activate

shell
Copy code

### 3. Install Dependencies
pip install -r requirements.txt

shell
Copy code

### 4. Start the Chatbot
python app.py

shell
Copy code

### 5. Open in Browser
http://localhost:5000

yaml
Copy code

---

## Voice Input (Microphone)
If voice input does not work:
- Allow microphone permission in browser
- Use Chrome or Edge browser
- Enable microphone access in Windows Privacy Settings

---

## Adding More FAQs
Add any `.txt` files to this folder:
data/docs/

yaml
Copy code
The chatbot will automatically use them to improve accuracy.

---

## Notes
- First run will automatically download AI model files.
- `sample_faq.txt` contains a large FAQ dataset for high accuracy.
- The UI includes mic, send, and speaker buttons.

---

## Purpose
This chatbot helps automate student queries related to:
- Fees  
- Attendance  
- Scholarships  
- Hostels  
- Transport  
- Academics  
- Exams  
- Campus Facilities  
- Placements  

Developed for **Student Helpdesk Automation using AI and NLP**.

---

