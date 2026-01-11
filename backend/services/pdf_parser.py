import fitz
from io import BytesIO


class PDFParser:
    def extract_text(self, pdf_bytes: bytes) -> str:
        try:
            if not pdf_bytes or len(pdf_bytes) == 0:
                raise Exception("PDF file is empty or invalid")
            
            pdf_stream = BytesIO(pdf_bytes)
            doc = fitz.open(stream=pdf_stream, filetype="pdf")
            
            if doc.page_count == 0:
                doc.close()
                raise Exception("PDF has no pages")
            
            text = ""
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
            
            doc.close()
            
            if not text or len(text.strip()) == 0:
                raise Exception("Could not extract any text from PDF. The PDF might be image-based or encrypted.")
            
            return text.strip()
        
        except Exception as e:
            if "PDF" in str(e) or "extract" in str(e).lower():
                raise Exception(str(e))
            raise Exception(f"Could not read PDF text: {str(e)}")
