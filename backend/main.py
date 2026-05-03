from fastapi import FastAPI, UploadFile, File
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware


from ocr.pdf_reader import process_pdf
from utils.text_cleaner import clean_text
from extraction.bidder_extractor import extract_bidder_info
from extraction.tender_extractor import extract_tender_criteria
from utils.normalizer import normalize_bidder_data
from evaluation.criteria_simplifier import simplify_criteria
from evaluation.evaluator import evaluate_bidder
from evaluation.explanation_engine import generate_final_output

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for hackathon)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/evaluate")
async def evaluate(tender: UploadFile = File(...), bidder: UploadFile = File(...)):
    
    tender_path = os.path.join(UPLOAD_DIR, tender.filename)
    bidder_path = os.path.join(UPLOAD_DIR, bidder.filename)

    # Save files
    with open(tender_path, "wb") as buffer:
        shutil.copyfileobj(tender.file, buffer)

    with open(bidder_path, "wb") as buffer:
        shutil.copyfileobj(bidder.file, buffer)

    # 🔹 Tender processing
    tender_text = process_pdf(tender_path)
    clean_tender = clean_text(tender_text)
    raw_criteria = extract_tender_criteria(clean_tender)
    simplified = simplify_criteria(raw_criteria)

    # 🔹 Bidder processing
    bidder_text = process_pdf(bidder_path)
    clean_bidder = clean_text(bidder_text)
    bidder_data = extract_bidder_info(clean_bidder)
    normalized = normalize_bidder_data(bidder_data)

    # 🔹 Evaluation
    results = evaluate_bidder(normalized, simplified)

    final_output = generate_final_output(
        bidder_name=normalized.get("company_name"),
        results=results
    )

    confidence = {
    "turnover": 0.9 if normalized.get("turnover") else 0.5,
    "projects": 0.9 if normalized.get("projects_completed") else 0.5,
    "gst": 1.0 if normalized.get("gst_number") else 0.0,
    "pan": 1.0 if normalized.get("pan_number") else 0.0
}

    summary = f"""
    Bidder {normalized.get("company_name")} has been evaluated.
    Turnover: {results['turnover']['status']}
    Projects: {results['projects']['status']}
    Overall: {final_output['final_status']}
    """
    return {
        "criteria": simplified,
        "bidder": normalized,
        "result": final_output,
        "confidence": confidence,
        "summary": summary
    }