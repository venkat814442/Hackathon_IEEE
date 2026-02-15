from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

from extractor import extract_text
from classifier import process_document
from schemas import DirectiveResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

@app.post("/analyze/", response_model=DirectiveResponse)
async def analyze(file: UploadFile = File(...)):
    text = extract_text(file.file)
    result = process_document(text)
    return result
