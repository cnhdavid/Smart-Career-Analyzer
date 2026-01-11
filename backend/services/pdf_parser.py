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
            
            if not text or len(text.strip()) == 0:
                raise Exception("Could not extract any text from PDF. The PDF might be image-based or scanned. Please upload a text-based PDF")
            
            return text.strip()
        
        except Exception as e:
            error_msg = str(e)
            if "PDF" in error_msg or "extract" in error_msg.lower() or "password" in error_msg.lower() or "encrypt" in error_msg.lower():
                raise Exception(error_msg)
            raise Exception(f"Could not read PDF: {error_msg}")
