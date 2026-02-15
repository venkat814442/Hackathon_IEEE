import spacy
import re

nlp = spacy.load("en_core_web_sm")

def classify_sentence(sentence):
    s = sentence.lower()

    if any(word in s for word in [
        "must not",
        "shall not",
        "prohibited",
        "not allowed",
        "no person shall"
    ]):
        return "DONT"

    if any(word in s for word in [
        "must",
        "shall",
        "required to",
        "should",
        "are required to"
    ]):
        return "DO"

    if any(word in s for word in [
        "recommended",
        "encouraged",
        "advised",
        "may"
    ]):
        return "GUIDELINE"

    return None


def extract_deadlines(sentence):
    pattern = r"\b\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b"
    return re.findall(pattern, sentence)


def process_document(text):
    doc = nlp(text)

    dos = []
    donts = []
    guidelines = []
    deadlines = []

    for sent in doc.sents:
        category = classify_sentence(sent.text.strip())

        if category == "DO":
            dos.append(sent.text.strip())
        elif category == "DONT":
            donts.append(sent.text.strip())
        elif category == "GUIDELINE":
            guidelines.append(sent.text.strip())

        found_dates = extract_deadlines(sent.text)
        if found_dates:
            deadlines.extend(found_dates)

    return {
        "dos": dos,
        "donts": donts,
        "guidelines": guidelines,
        "deadlines": list(set(deadlines))
    }
