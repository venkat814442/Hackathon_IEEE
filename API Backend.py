from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import spacy
import pdfplumber
import io
import re

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_sm")

# -----------------------
# Your Processing Logic
# -----------------------

def classify_sentence(sentence):
    s = sentence.lower()

    if any(word in s for word in ["must not", "shall not", "prohibited"]):
        return "DONT"

    if any(word in s for word in ["must", "shall", "required to"]):
        return "DO"

    if any(word in s for word in ["recommended", "encouraged", "may"]):
        return "GUIDELINE"

    return None


def process_document(text):
    doc = nlp(text)

    dos, donts, guidelines = [], [], []

    for sent in doc.sents:
        category = classify_sentence(sent.text.strip())

        if category == "DO":
            dos.append(sent.text.strip())
        elif category == "DONT":
            donts.append(sent.text.strip())
        elif category == "GUIDELINE":
            guidelines.append(sent.text.strip())

    return {
        "dos": dos,
        "donts": donts,
        "guidelines": guidelines
    }


def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text


# -----------------------
# API Endpoint
# -----------------------

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    result = process_document(text)
    return result
