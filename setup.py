import subprocess
import sys
import os

def check_and_install_dependencies():
    """Check if required packages are installed and install them if needed."""
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("Creating requirements.txt file...")
            with open('requirements.txt', 'w') as f:
                f.write("pillow==10.2.0\n")
                f.write("pytesseract==0.3.10\n")
                f.write("keyboard==0.13.5\n")
                f.write("requests==2.31.0\n")
                f.write("pyttsx3 == 2.98\n")

        # Install dependencies
        print("Checking and installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies installed successfully!")

        # Check for Tesseract OCR
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            print("Tesseract OCR is installed and working.")
        except Exception:
            print("\nWARNING: Tesseract OCR may not be installed on your system.")
            print("Please install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("After installation, make sure it's added to your PATH or set the path in your code.")
            input("Press Enter to continue anyway...")

        return True
    except Exception as e:
        print(f"Error installing dependencies: {str(e)}")
        return False

if __name__ == "__main__":
    if check_and_install_dependencies():
        print("Setup completed successfully!")
    else:
        print("Setup failed. Please install dependencies manually.")
