# Smart Portfolio Analyzer - API Documentation

## Overview

The Smart Portfolio Analyzer is a FastAPI-based web application that provides intelligent resume analysis and career guidance. It uses AI to analyze resumes, extract skills, suggest career paths, and provide personalized recommendations.

## Architecture

The application consists of three main components:
- **Backend API** (FastAPI): Provides REST endpoints for resume analysis
- **AI Analyzer**: Uses OpenAI's GPT models or mock analysis for intelligent insights
- **PDF Parser**: Extracts text content from PDF resumes

---

## Backend API (`backend/main.py`)

### Main Application

#### `app = FastAPI(title="Smart Career & Skill-Gap Analyzer API")`
- **Purpose**: Creates the FastAPI application instance
- **Returns**: FastAPI application object
- **Configuration**: Sets up CORS middleware for frontend communication

#### Global Exception Handler
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception)
```
- **Purpose**: Handles all unhandled exceptions globally
- **Parameters**:
  - `request`: The incoming HTTP request
  - `exc`: The exception that occurred
- **Returns**: JSON response with error details and CORS headers
- **Features**: Logs full traceback for debugging

### Pydantic Models

#### `AnalysisRequest`
- **Purpose**: Defines the request structure for text-based resume analysis
- **Fields**:
  - `text_resume` (Optional[str]): Resume text content
  - `target_role` (Optional[str]): Desired job role
  - `job_description` (Optional[str]): Target job description

#### `AnalysisResponse`
- **Purpose**: Defines the response structure for resume analysis results
- **Fields**:
  - `skills` (List[str]): Extracted skills from resume
  - `experience_years` (float): Estimated years of experience
  - `current_field` (str): Current professional field
  - `role_matches` (Dict[str, float]): Match percentages for suggested roles
  - `skill_gaps` (Dict[str, List[str]]): Missing skills for each role
  - `radar_data` (Dict): Data for radar chart visualization
  - `recommendations` (List[Dict[str, str]]): Learning recommendations
  - `trending_industries` (List[str]): Relevant trending industries
  - `summary` (str): Professional summary/verdict
  - `ats_feedback` (List[str]): ATS optimization tips

### API Endpoints

#### `GET /`
- **Purpose**: Root endpoint to check API status
- **Returns**: Status information including AI mode (mock/live)
- **Response Example**:
```json
{
  "status": "online",
  "message": "Smart Career & Skill-Gap Analyzer API",
  "version": "1.0.0",
  "ai_mode": "live"
}
```

#### `POST /api/analyze-resume`
- **Purpose**: Analyze resume from uploaded PDF file
- **Parameters**:
  - `file` (Optional[UploadFile]): PDF resume file
  - `target_role` (Optional[str]): Target job role
  - `job_description` (Optional[str]): Job description text
- **Returns**: `AnalysisResponse` with comprehensive analysis
- **Validation**:
  - Only PDF files are supported
  - Minimum 50 characters of extracted text required
- **Error Handling**: Returns HTTP 400 for invalid files, 500 for processing errors

#### `POST /api/analyze-text`
- **Purpose**: Analyze resume from text input
- **Parameters**: `AnalysisRequest` object
- **Returns**: `AnalysisResponse` with comprehensive analysis
- **Validation**: Minimum 50 characters of text required
- **Error Handling**: Returns HTTP 400 for short text, 500 for processing errors

#### `GET /api/health`
- **Purpose**: Health check endpoint
- **Returns**: Health status and AI mode
- **Response Example**:
```json
{
  "status": "healthy",
  "ai_mode": "live"
}
```

---

## AI Analyzer (`backend/services/ai_analyzer.py`)

### Main Classes

#### `Recommendation` (Pydantic BaseModel)
- **Purpose**: Defines structure for learning recommendations
- **Fields**:
  - `skill` (str): Skill to learn
  - `priority` (str): Priority level (High/Medium/Low)
  - `resource` (str): Learning resource name
  - `timeframe` (str): Estimated learning time
  - `learning_tip` (str): One-sentence learning tip

#### `ResumeAnalysis` (Pydantic BaseModel)
- **Purpose**: Defines complete structure for resume analysis results
- **Fields**: All analysis components matching `AnalysisResponse`

#### `AIAnalyzer`
Main class for resume analysis with AI capabilities.

### Constructor
```python
def __init__(self)
```
- **Purpose**: Initialize the AI analyzer
- **Features**:
  - Checks for OpenAI API key
  - Sets up mock mode if no API key
  - Initializes ChatOpenAI model for live analysis
- **Mock Mode**: Provides rule-based analysis when API key is missing

### Core Methods

#### `analyze(resume_text, target_role=None, job_description=None)`
- **Purpose**: Main analysis method that routes to appropriate analysis type
- **Parameters**:
  - `resume_text` (str): Resume text content
  - `target_role` (Optional[str]): Target job role
  - `job_description` (Optional[str]): Job description
- **Returns**: Dictionary with complete analysis results
- **Logic**: Routes to `_mock_analysis()` or `_ai_analysis()` based on API key availability

#### `_mock_analysis(resume_text, target_role=None, job_description=None)`
- **Purpose**: Provides rule-based analysis without AI
- **Features**:
  - Extracts skills using keyword matching
  - Estimates experience years from text patterns
  - Detects professional field
  - Calculates role match percentages
  - Generates recommendations and feedback
- **Returns**: Complete analysis dictionary

#### `_ai_analysis(resume_text, target_role=None, job_description=None)`
- **Purpose**: Provides AI-powered analysis using OpenAI
- **Features**:
  - Uses LangChain for structured output
  - Handles job description matching
  - Generates dynamic career suggestions
  - Provides personalized insights
- **Fallback**: Falls back to mock analysis on AI failure

### Helper Methods

#### Skill Extraction
```python
def _extract_skills_universal(self, text: str) -> List[str]
```
- **Purpose**: Extract skills from resume text using keyword matching
- **Database**: 100+ universal skills across tech, business, healthcare, etc.
- **Returns**: List of detected skills (max 20)

#### Experience Detection
```python
def _extract_experience_simple(self, text: str) -> float
```
- **Purpose**: Extract years of experience from text
- **Patterns**: Matches "X years experience" patterns
- **Returns**: Float representing years of experience (default: 2.0)

#### Field Detection
```python
def _detect_field(self, text: str, skills: List[str]) -> str
```
- **Purpose**: Identify professional field based on keywords and skills
- **Fields**: 11 predefined fields (Software Development, Data Science, etc.)
- **Returns**: Detected field name

#### Role Suggestions
```python
def _suggest_roles(self, current_field: str, exclude_role: Optional[str] = None) -> List[str]
```
- **Purpose**: Suggest 3 logical career next steps
- **Logic**: Field-specific role mappings
- **Returns**: List of 3 role suggestions

#### Role Requirements
```python
def _get_role_requirements(self, role: str, field: str) -> List[str]
```
- **Purpose**: Get required skills for a specific role
- **Logic**: Combines generic role skills with field-specific skills
- **Returns**: List of required skills (max 10)

#### Radar Chart Categories
```python
def _get_field_categories(self, field: str) -> List[str]
```
- **Purpose**: Get radar chart categories for visualization
- **Returns**: 5 field-specific categories

#### Score Calculation
```python
def _calculate_universal_scores(self, skills: List[str], categories: List[str]) -> List[float]
```
- **Purpose**: Calculate competency scores for radar chart
- **Returns**: List of 5 scores (0-100)

#### Trending Industries
```python
def _identify_trending_industries(self, skills: List[str], current_field: str) -> List[str]
```
- **Purpose**: Identify relevant trending industries
- **Industries**: 10 trending sectors (FinTech, HealthTech, etc.)
- **Returns**: List of matching industries (max 5)

#### Learning Resources
```python
def _get_learning_resource(self, skill: str) -> str
```
- **Purpose**: Get learning resource for a skill
- **Database**: 50+ curated resources
- **Returns**: Resource name or generic suggestion

#### Timeframes
```python
def _get_timeframe(self, skill: str) -> str
```
- **Purpose**: Get estimated learning time for a skill
- **Returns**: Timeframe string (e.g., "2-3 months")

#### Learning Tips
```python
def _get_learning_tip(self, skill: str) -> str
```
- **Purpose**: Get learning tip for a skill
- **Database**: 70+ skill-specific tips
- **Returns**: One-sentence learning advice

#### Summary Generation
```python
def _generate_summary(self, skills: List[str], experience_years: float, top_role: str, match_score: float) -> str
```
- **Purpose**: Generate professional summary
- **Logic**: Based on skill count, experience, and match score
- **Returns**: Two-sentence professional verdict

#### Job Description Processing
```python
def _extract_skills_from_job_description(self, job_description: str) -> List[str]
def _extract_role_from_job_description(self, job_description: str) -> str
```
- **Purpose**: Extract skills and role from job description
- **Features**: Keyword matching and role pattern detection

#### ATS Feedback
```python
def _generate_ats_feedback(self, resume_text: str, skills: List[str], job_description: Optional[str] = None) -> List[str]
```
- **Purpose**: Generate ATS optimization feedback
- **Checks**: Contact info, section headings, quantifiable achievements, keywords
- **Returns**: List of 3-5 actionable tips

---

## PDF Parser (`backend/services/pdf_parser.py`)

### `PDFParser` Class

#### `extract_text(pdf_bytes: bytes) -> str`
- **Purpose**: Extract text content from PDF files
- **Parameters**:
  - `pdf_bytes` (bytes): PDF file content as bytes
- **Returns**: Extracted text as string
- **Library**: Uses PyMuPDF (fitz) for text extraction
- **Error Handling**:
  - Validates PDF file existence and content
  - Checks for empty or invalid PDFs
  - Handles image-based or encrypted PDFs
  - Provides descriptive error messages
- **Process**:
  1. Creates BytesIO stream from bytes
  2. Opens PDF with fitz
  3. Iterates through pages extracting text
  4. Combines and cleans text
  5. Returns stripped text

---

## Configuration and Environment

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for AI analysis (optional)
- **Mock Mode**: Activated when API key is missing

### CORS Configuration
- **Allowed Origins**: http://localhost:3000, http://localhost:3001
- **Methods**: All HTTP methods
- **Headers**: All headers
- **Credentials**: Supported

### Dependencies
- **FastAPI**: Web framework
- **PyMuPDF**: PDF text extraction
- **LangChain**: AI/LLM integration
- **OpenAI**: AI model API
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

---

## Usage Examples

### Analyzing PDF Resume
```python
import requests

# Upload PDF file
files = {'file': open('resume.pdf', 'rb')}
data = {'target_role': 'Software Engineer'}

response = requests.post('http://localhost:8000/api/analyze-resume', 
                        files=files, data=data)
analysis = response.json()
```

### Analyzing Text Resume
```python
import requests

data = {
    'text_resume': 'John Doe\nSoftware Engineer with 5 years experience...',
    'target_role': 'Senior Software Engineer'
}

response = requests.post('http://localhost:8000/api/analyze-text', json=data)
analysis = response.json()
```

### Health Check
```python
response = requests.get('http://localhost:8000/api/health')
status = response.json()
```

---

## Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid file, short text)
- **500**: Internal Server Error (processing failures)

### Error Response Format
```json
{
  "message": "Error description",
  "type": "ExceptionType",
  "traceback": "Full traceback (in development)"
}
```

### Common Errors
- PDF file validation failures
- Text extraction issues
- AI service unavailability
- Invalid input formats

---

## Development Notes

### Mock Mode vs Live Mode
- **Mock Mode**: Rule-based analysis, no API key required
- **Live Mode**: AI-powered analysis with OpenAI integration
- **Fallback**: Automatic fallback to mock mode on AI failures

### Extending the System
- Add new skills to universal skills list
- Extend field mappings for new industries
- Customize role requirements per field
- Add new learning resources and timeframes

### Performance Considerations
- PDF processing is memory-intensive
- AI analysis has token limits (3000 chars)
- Response times vary by analysis complexity
- Consider caching for repeated analyses
