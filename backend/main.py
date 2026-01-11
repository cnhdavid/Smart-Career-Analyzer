from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import os
import traceback
from dotenv import load_dotenv
import uvicorn

from services.pdf_parser import PDFParser
from services.ai_analyzer import AIAnalyzer

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY is missing! Running in mock mode.")
else:
    print("INFO: OPENAI_API_KEY found. Running in live AI mode.")

app = FastAPI(title="Smart Career & Skill-Gap Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_parser = PDFParser()
ai_analyzer = AIAnalyzer()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[GLOBAL ERROR HANDLER] Caught exception: {type(exc).__name__}")
    print(f"[GLOBAL ERROR HANDLER] Error message: {str(exc)}")
    print(f"[GLOBAL ERROR HANDLER] Full traceback:")
    print(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc()
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )


class AnalysisRequest(BaseModel):
    text_resume: Optional[str] = None
    target_role: Optional[str] = None
    job_description: Optional[str] = None


class AnalysisResponse(BaseModel):
    skills: List[str]
    experience_years: float
    current_field: str
    role_matches: Dict[str, float]
    skill_gaps: Dict[str, List[str]]
    radar_data: Dict
    recommendations: List[Dict[str, str]]
    trending_industries: List[str]
    summary: str
    ats_feedback: List[str]


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Smart Career & Skill-Gap Analyzer API",
        "version": "1.0.0",
        "ai_mode": "mock" if not os.getenv("OPENAI_API_KEY") else "live"
    }


@app.post("/api/analyze-resume", response_model=AnalysisResponse)
async def analyze_resume(file: Optional[UploadFile] = File(None), target_role: Optional[str] = None, job_description: Optional[str] = None):
    if file:
        print(f"Received file: {file.filename}")
        
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        try:
            print(f"[DEBUG] Starting to process file: {file.filename}")
            contents = await file.read()
            print(f"[DEBUG] File read successfully, size: {len(contents)} bytes")
            
            extracted_text = pdf_parser.extract_text(contents)
            print(f"[DEBUG] Text extracted, length: {len(extracted_text) if extracted_text else 0} characters")
            
            if not extracted_text or len(extracted_text.strip()) < 50:
                raise HTTPException(status_code=400, detail="Could not extract meaningful text from PDF")
            
            print(f"[DEBUG] Calling AI analyzer with target_role: {target_role}, job_description: {'Yes' if job_description else 'No'}")
            analysis = ai_analyzer.analyze(extracted_text, target_role=target_role, job_description=job_description)
            print(f"[DEBUG] Analysis complete, returning results")
            
            return analysis
        
        except HTTPException as he:
            print(f"[ERROR] HTTP Exception: {he.detail}")
            raise he
        except Exception as e:
            print(f"[ERROR] Unexpected error occurred:")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="No file provided")


@app.post("/api/analyze-text", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    if not request.text_resume or len(request.text_resume.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume text is too short or empty")
    
    try:
        print(f"[DEBUG] Analyzing text resume with target_role: {request.target_role}, job_description: {'Yes' if request.job_description else 'No'}")
        analysis = ai_analyzer.analyze(request.text_resume, target_role=request.target_role, job_description=request.job_description)
        print(f"[DEBUG] Analysis complete, returning results")
        return analysis
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_mode": "mock" if not os.getenv("OPENAI_API_KEY") else "live"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
