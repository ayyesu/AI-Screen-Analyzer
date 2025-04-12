import os
import sys

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Check if dependencies are installed
try:
    from PIL import ImageGrab, Image
    import pytesseract
    import keyboard
    import requests
except ImportError:
    # If not installed, try to install them
    print("Some dependencies are missing. Attempting to install...")
    try:
        # Run the setup script
        if os.path.exists('setup.py'):
            import setup
            setup.check_and_install_dependencies()
        else:
            # If setup.py doesn't exist, install directly
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "pytesseract", "keyboard", "requests"])

        # Try importing again
        from PIL import ImageGrab, Image
        import pytesseract
        import keyboard
        import requests
    except Exception as e:
        print(f"Error installing dependencies: {str(e)}")
        print("Please run 'pip install pillow pytesseract keyboard requests' manually.")
        sys.exit(1)

from app.utils.config import ConfigManager
from app.utils.hotkey import HotkeyManager
from app.ui.main_window import MainWindow

def main():
    # Initialize configuration
    config_manager = ConfigManager()

    # Initialize hotkey manager
    hotkey_manager = HotkeyManager(config_manager)

    # Initialize and run the main window
    app = MainWindow(config_manager, hotkey_manager)
    app.run()

if __name__ == "__main__":
    main()
