# Screen Reader Application

A powerful screen reader application that captures screen content and processes it using Optical Character Recognition (OCR) technology and Text-to-Speech capabilities. The application can detect code snippets, programming questions, and regular text, making it particularly useful for developers and technical users. With its modern UI and enhanced accessibility features, it provides a seamless user experience.

## Features

- Screen text capture and reading
- Text-to-Speech functionality
- Automatic code detection
- Modern, responsive UI with theme support
- Customizable hotkeys
- Enhanced button interactions
- Support for programming-related content

## Prerequisites

- Python 3.x
- Tesseract OCR ([Download from UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki))

## Installation

1. Clone or download this repository
2. Run the setup script to install dependencies:
   ```bash
   python setup.py
   ```
   This will automatically:
   - Create requirements.txt if not present
   - Install required Python packages:
     - Pillow (10.2.0)
     - pytesseract (0.3.10)
     - keyboard (0.13.5)
     - requests (2.31.0)
     - pyttsx3 (latest)
   - Check for Tesseract OCR installation

3. Make sure Tesseract OCR is properly installed and added to your system PATH

## Usage

1. Start the application using the provided batch file:
   ```bash
   run_screen_reader.bat
   ```
   Or run directly with Python:
   ```bash
   python run.py
   ```

2. The application will initialize with a modern user interface featuring:
   - Dark/Light theme support
   - Intuitive button layouts
   - Real-time OCR status indicators
   - Text-to-Speech controls

## Features in Detail

### OCR Processing
- Captures screen content and converts it to text
- Specialized detection for code snippets and programming content
- Handles various programming languages and syntax

### Text-to-Speech
- Natural-sounding voice output
- Adjustable speech rate and volume
- Support for multiple languages
- Pause/Resume functionality

### Code Detection
Automatically identifies:
- Programming language keywords
- Function definitions and calls
- Error messages and exceptions
- Programming questions and discussions

### Modern UI
- Responsive design that adapts to window size
- Dark and light theme support
- Smooth animations and transitions
- Enhanced button feedback and interactions
- Accessibility-focused design elements

### Configuration
- Customizable settings through config.ini
- Adjustable hotkeys for various functions
- Theme preferences
- Speech settings customization

## Project Structure

```
├── app/
│   ├── core/         # Core functionality
│   │   ├── ocr.py    # OCR processing
│   │   ├── speech.py # Text-to-speech handling
│   │   └── api.py    # API integrations
│   ├── ui/           # User interface components
│   │   ├── main_window.py # Main application window
│   │   ├── theme.py      # Theme management
│   │   └── dialogs.py    # Dialog windows
│   ├── utils/        # Utility functions
│   └── main.py       # Application entry point
├── setup.py          # Dependency installation
├── run.py            # Runner script
└── run_screen_reader.bat  # Windows batch launcher
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.
