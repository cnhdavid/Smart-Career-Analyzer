# Backend - Smart Career Analyzer API

FastAPI backend for resume analysis and skill gap detection.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment (optional):
```bash
copy .env.example .env
# Add your OPENAI_API_KEY to .env
```

4. Run server:
```bash
python main.py
```

Server runs on `http://localhost:8000`

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Mock Mode

The API automatically runs in mock mode if no OpenAI API key is provided. This allows full functionality for demonstrations without incurring API costs.
