from io import BytesIO


class PDFParser:
    def extract_text(self, pdf_bytes: bytes) -> str:
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError
        
        try:
            if not pdf_bytes or len(pdf_bytes) == 0:
                raise Exception("PDF file is empty or invalid")
            
            pdf_stream = BytesIO(pdf_bytes)
            
            try:
                reader = PdfReader(pdf_stream)
            except PdfReadError as e:
                raise Exception("PDF file is corrupted or in an unsupported format")
            except Exception as e:
                if "encrypt" in str(e).lower() or "password" in str(e).lower():
                    raise Exception("PDF is password-protected. Please upload an unencrypted PDF")
                raise Exception(f"Unable to read PDF: {str(e)}")
            
            if len(reader.pages) == 0:
                raise Exception("PDF has no pages")
            
            if reader.is_encrypted:
                raise Exception("PDF is password-protected. Please upload an unencrypted PDF")
            
            text = ""
            for page in reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    continue
            
            # If no text extracted, try OCR
            if not text or len(text.strip()) < 50:
                print("[PDF Parser] No text extracted with pypdf, attempting OCR...")
                text = self._extract_text_with_ocr(pdf_bytes)
            
            if not text or len(text.strip()) == 0:
                raise Exception("Could not extract any text from PDF. The PDF might be corrupted or empty.")
            
            return text.strip()
        
        except Exception as e:
            error_msg = str(e)
            if "PDF" in error_msg or "extract" in error_msg.lower() or "password" in error_msg.lower() or "encrypt" in error_msg.lower():
                raise Exception(error_msg)
            raise Exception(f"Could not read PDF: {error_msg}")
    
    def _extract_text_with_ocr(self, pdf_bytes: bytes) -> str:
        """Extract text from image-based PDF using OCR (cloud-based for serverless compatibility)"""
        import os
        
        # Try OpenAI Vision API first (works in serverless)
        if os.getenv("OPENAI_API_KEY"):
            try:
                return self._extract_with_openai_vision(pdf_bytes)
            except Exception as e:
                print(f"[OCR] OpenAI Vision failed: {str(e)}, trying local OCR...")
        
        # Fallback to local Tesseract OCR (for local development)
        try:
            return self._extract_with_tesseract(pdf_bytes)
        except Exception as e:
            print(f"[OCR ERROR] All OCR methods failed: {str(e)}")
            raise Exception("Could not extract text from image-based PDF. Please ensure the PDF contains selectable text or try converting it to a text-based PDF.")
    
    def _extract_with_openai_vision(self, pdf_bytes: bytes) -> str:
        """Extract text using OpenAI Vision API (serverless-compatible)"""
        try:
            import os
            from openai import OpenAI
            import fitz  # PyMuPDF
            import base64
            from io import BytesIO
            from PIL import Image
            
            print("[OCR] Using OpenAI Vision API for text extraction...")
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            page_count = len(pdf_document)
            print(f"[OCR] Processing {page_count} pages with OpenAI Vision...")
            
            text = ""
            # Limit to 5 pages to control costs
            for page_num in range(min(page_count, 5)):
                print(f"[OCR] Extracting text from page {page_num + 1}/{min(page_count, 5)}...")
                
                # Render page to image
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
                
                # Convert to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Convert image to base64
                buffered = BytesIO()
                img.save(buffered, format="JPEG", quality=85)
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Call OpenAI Vision API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Extract ALL text from this resume/CV page. Return ONLY the extracted text, preserving the structure and formatting as much as possible. Do not add any commentary or explanations."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}",
                                        "detail": "high"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=2000
                )
                
                page_text = response.choices[0].message.content
                if page_text:
                    text += page_text + "\n\n"
            
            pdf_document.close()
            
            if page_count > 5:
                print(f"[OCR] Note: Only processed first 5 pages out of {page_count} to control API costs")
            
            print(f"[OCR] Extracted {len(text)} characters using OpenAI Vision")
            return text.strip()
        
        except Exception as e:
            print(f"[OCR ERROR] OpenAI Vision extraction failed: {str(e)}")
            raise
    
    def _extract_with_tesseract(self, pdf_bytes: bytes) -> str:
        """Extract text using local Tesseract OCR (for local development only)"""
        try:
            import pytesseract
            import fitz  # PyMuPDF
            from PIL import Image
            import os
            import platform
            
            print("[OCR] Using local Tesseract OCR...")
            
            # Configure Tesseract path for Windows
            if platform.system() == 'Windows':
                tesseract_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                ]
                for path in tesseract_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        print(f"[OCR] Found Tesseract at: {path}")
                        break
            
            # Convert PDF to images using PyMuPDF
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            text = ""
            print(f"[OCR] Processing {len(pdf_document)} pages with Tesseract...")
            for page_num in range(len(pdf_document)):
                print(f"[OCR] Extracting text from page {page_num + 1}/{len(pdf_document)}...")
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 3x zoom for better OCR
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                page_text = pytesseract.image_to_string(img, lang='eng+deu')
                if page_text:
                    text += page_text + "\n"
            
            pdf_document.close()
            
            print(f"[OCR] Extracted {len(text)} characters with Tesseract")
            return text.strip()
        
        except ImportError as ie:
            print(f"[OCR ERROR] Tesseract dependencies not available: {str(ie)}")
            raise Exception("Local OCR not available. Please ensure OpenAI API key is configured for cloud-based OCR.")
        except Exception as e:
            print(f"[OCR ERROR] Tesseract extraction failed: {str(e)}")
            raise
