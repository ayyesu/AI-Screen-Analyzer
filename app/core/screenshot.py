import time
from PIL import ImageGrab

class ScreenshotTaker:
    @staticmethod
    def take_screenshot(region=None):
        """Take a screenshot of the specified region or entire screen

        Args:
            region (tuple): Optional tuple of (x1, y1, x2, y2) coordinates for region selection
        """
        try:
            # Take the screenshot of specified region or full screen
            screenshot = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
            return screenshot
        except Exception as e:
            raise Exception(f"Error taking screenshot: {str(e)}")
