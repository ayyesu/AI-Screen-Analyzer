import time
from PIL import ImageGrab

class ScreenshotTaker:
    @staticmethod
    def take_screenshot():
        """Take a screenshot of the entire screen"""
        try:
            # Take the screenshot
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            raise Exception(f"Error taking screenshot: {str(e)}")
