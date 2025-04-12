import re
import pytesseract

class OCRProcessor:
    @staticmethod
    def extract_text(image):
        """Extract text from an image using OCR"""
        try:
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise Exception(f"OCR processing error: {str(e)}")

    @staticmethod
    def detect_code_content(text):
        """Detect if the text contains code or programming questions."""
        # Check for code patterns
        code_indicators = [
            # Programming language keywords
            r'\b(function|def|class|import|from|var|const|let|for|while|if|else)\b',
            # Common programming punctuation patterns
            r'[{};]\s*$',  # Lines ending with { } or ;
            # Common code patterns
            r'(\w+)\((.*?)\)',  # Function calls
            # Error messages
            r'(error|exception|traceback|undefined|null|nil)\b',
            # Coding questions indicators
            r'how (do|to|can) I (code|program|implement|debug|fix)',
            r'(syntax|runtime|compiler) error',
            r'(algorithm|function|method|api|library)',
            r'code (snippet|example|sample)',
        ]

        for pattern in code_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False
