import requests
import json
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai

class VisionAnalyzer:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self._setup_gemini()

    def _setup_gemini(self):
        """Initialize Gemini API with configuration"""
        api_key = self.config_manager.get('API', 'gemini_api_key')
        if not api_key:
            raise ValueError("Gemini API key not found in config.ini")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_image_content(self, image):
        """Analyze image content using Gemini Vision API

        Args:
            image: PIL Image object

        Returns:
            str: Detailed description of the image content
        """
        try:
            # Ensure image is in correct format
            if not isinstance(image, Image.Image):
                raise ValueError("Input must be a PIL Image object")

            # Prepare the prompt
            prompt = (
                "Please analyze this image and provide a detailed description of its content. Include:"
                "\n1. Main subjects or objects in the image"
                "\n2. Scene description and setting"
                "\n3. Notable visual elements (colors, lighting, composition)"
                "\n4. Any text or symbols if present"
                "\n5. Overall context and purpose of the image"
            )

            # Generate content using Gemini Vision API
            response = self.model.generate_content([prompt, image])

            if response.text:
                return response.text
            else:
                return "No description could be generated for this image."

        except ValueError as ve:
            return f"Invalid input: {str(ve)}"
        except genai.types.generation_types.BlockedPromptException:
            return "Content analysis was blocked due to safety concerns."
        except Exception as e:
            return f"Error analyzing image content: {str(e)}"

    def combine_analysis(self, image):
        """Combine traditional image analysis with AI-powered content description

        Args:
            image: PIL Image object

        Returns:
            dict: Combined analysis results
        """
        from .image_analysis import ImageAnalyzer

        # Get traditional image analysis
        basic_analysis = ImageAnalyzer.analyze_image(image)

        # Get AI-powered content description
        content_description = self.analyze_image_content(image)

        # Combine results
        return {
            **basic_analysis,
            'content_description': content_description
        }
