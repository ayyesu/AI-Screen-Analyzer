import cv2
import numpy as np
from PIL import Image

class ImageAnalyzer:
    @staticmethod
    def analyze_image(image, use_ai=True):
        """Analyze image content and provide insights

        Args:
            image: PIL Image object
            use_ai: bool, whether to use AI-powered content analysis

        Returns:
            dict: Analysis results including colors, objects, composition and AI description
        """
        # Convert PIL image to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        analysis = {
            'color_analysis': ImageAnalyzer._analyze_colors(cv_image),
            'composition': ImageAnalyzer._analyze_composition(cv_image),
            'objects': ImageAnalyzer._detect_objects(cv_image)
        }

        # Add AI-powered content analysis if requested
        if use_ai:
            from .vision_analysis import VisionAnalyzer
            from ..utils.config import ConfigManager

            config = ConfigManager()
            vision_analyzer = VisionAnalyzer(config)
            ai_analysis = vision_analyzer.analyze_image_content(image)
            analysis['content_description'] = ai_analysis

        return analysis

    @staticmethod
    def _analyze_colors(image):
        """Analyze the color distribution in the image"""
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Calculate color histogram
        hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])

        # Find dominant colors
        dominant_colors = []
        threshold = 0.1 * image.shape[0] * image.shape[1]  # 10% of image pixels

        for i in range(len(hist)):
            if hist[i] > threshold:
                # Convert HSV value back to color name
                hue = i * 2  # Scale back to 0-360 range
                if 0 <= hue <= 30 or 330 <= hue <= 360:
                    dominant_colors.append('red')
                elif 30 < hue <= 90:
                    dominant_colors.append('yellow')
                elif 90 < hue <= 150:
                    dominant_colors.append('green')
                elif 150 < hue <= 210:
                    dominant_colors.append('cyan')
                elif 210 < hue <= 270:
                    dominant_colors.append('blue')
                elif 270 < hue < 330:
                    dominant_colors.append('magenta')

        return {
            'dominant_colors': list(set(dominant_colors)),
            'brightness': ImageAnalyzer._calculate_brightness(image)
        }

    @staticmethod
    def _analyze_composition(image):
        """Analyze the composition and layout of the image"""
        height, width = image.shape[:2]

        # Detect edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.count_nonzero(edges) / (height * width)

        # Analyze image complexity
        complexity = 'high' if edge_density > 0.1 else 'medium' if edge_density > 0.05 else 'low'

        return {
            'aspect_ratio': f'{width}:{height}',
            'complexity': complexity,
            'orientation': 'landscape' if width > height else 'portrait' if height > width else 'square'
        }

    @staticmethod
    def _detect_objects(image):
        """Detect common objects in the image using pre-trained models"""
        # Initialize YOLO or similar object detection model here
        # For now, return basic shape detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect circles
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, 1, 20,
            param1=50, param2=30, minRadius=0, maxRadius=0
        )

        # Detect other shapes
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shapes = []
        if circles is not None:
            shapes.append('circles')

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
            if len(approx) == 3:
                shapes.append('triangle')
            elif len(approx) == 4:
                shapes.append('rectangle')
            elif len(approx) > 8:
                shapes.append('circle')

        return {
            'detected_shapes': list(set(shapes))
        }

    @staticmethod
    def _calculate_brightness(image):
        """Calculate the overall brightness of the image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)

        if brightness < 85:
            return 'dark'
        elif brightness > 170:
            return 'bright'
        else:
            return 'medium'
