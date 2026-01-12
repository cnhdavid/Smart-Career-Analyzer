# OCR Setup for Image-Based PDFs

This application now supports extracting text from image-based/scanned PDFs using OCR.

## How It Works

The system uses a **two-tier approach**:

1. **Primary (Cloud-based)**: OpenAI Vision API (gpt-4o-mini)
   - Works in serverless environments (Vercel)
   - Requires `OPENAI_API_KEY` environment variable
   - Processes up to 5 pages per PDF to control costs
   - High accuracy for resumes/CVs

2. **Fallback (Local)**: Tesseract OCR
   - Only used if OpenAI API is unavailable
   - Requires local Tesseract installation (Windows only)
   - Processes all pages

## For Local Development

If you want to use local Tesseract OCR as a fallback:

1. Download Tesseract-OCR: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR`
3. Select English and German language packs during installation

## For Vercel Deployment

No additional setup needed! The application automatically uses OpenAI Vision API when deployed to Vercel.

**Requirements:**
- `OPENAI_API_KEY` must be set in Vercel environment variables
- PyMuPDF and Pillow are included in requirements.txt

## Cost Considerations

- OpenAI Vision API (gpt-4o-mini) costs approximately $0.00015 per image
- For a 5-page resume: ~$0.00075 per upload
- The system limits processing to 5 pages to control costs

## Dependencies

- `PyMuPDF` - PDF to image conversion (serverless-compatible)
- `Pillow` - Image processing
- `openai` - OpenAI API client

All dependencies work in serverless environments without system-level installations.
