import re
import pytesseract
from PIL import Image
from .image_analysis import ImageAnalyzer

class OCRProcessor:
    @staticmethod
    def process_image(image, mode='auto'):
        """Process image based on selected mode

        Args:
            image: PIL Image object
            mode: Processing mode ('auto', 'code', 'general', 'image')

        Returns:
            dict: Processing results with type and content
        """
        try:
            # For image mode, skip OCR and do direct image analysis
            if mode == 'image':
                analysis = ImageAnalyzer.analyze_image(image)
                return {
                    'type': 'image_analysis',
                    'content': analysis
                }

            # For other modes, attempt OCR first
            text = pytesseract.image_to_string(image)

            # If no text found in auto mode, fallback to image analysis
            if mode == 'auto' and (not text.strip() or len(text.strip()) < 10):
                analysis = ImageAnalyzer.analyze_image(image)
                return {
                    'type': 'image_analysis',
                    'content': analysis
                }

            return {
                'type': 'text',
                'content': text,
                'is_code': mode == 'code' or (mode == 'auto' and OCRProcessor.detect_code_content(text))
            }
        except Exception as e:
            raise Exception(f"Image processing error: {str(e)}")

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
