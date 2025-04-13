# Screen Reader Application

A powerful screen reader application that captures screen content and processes it using Optical Character Recognition (OCR) technology and Text-to-Speech capabilities. The application features an advanced image analysis mode, CustomTkinter-based modern UI, and enhanced text processing capabilities. It can detect code snippets, programming questions, and regular text, making it particularly useful for developers and technical users.

## Features

- Screen text capture and reading
- Advanced image analysis mode
- Text-to-Speech functionality with toggle controls
- Automatic code detection
- Modern CustomTkinter-based UI with theme support
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
     - customtkinter (latest)
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

2. The application will initialize with a modern CustomTkinter interface featuring:
   - Dark/Light theme support
   - Intuitive button layouts
   - Real-time OCR status indicators
   - Text-to-Speech controls with toggle functionality
   - Image analysis mode selection

## Features in Detail

### OCR Processing
- Captures screen content and converts it to text
- Specialized detection for code snippets and programming content
- Handles various programming languages and syntax
- Advanced image analysis mode for enhanced text recognition

### Text-to-Speech
- Natural-sounding voice output
- Toggle functionality for easy control
- Adjustable speech rate and volume
- Support for multiple languages
- Pause/Resume functionality

### Image Analysis
- Advanced mode for complex image processing
- Enhanced text recognition accuracy
- Support for various image formats
- Optimized for technical content

### Modern CustomTkinter UI
- Responsive design that adapts to window size
- Dark and light theme support
- Smooth animations and transitions
- Enhanced button feedback and interactions
- Accessibility-focused design elements
- Selection window for different modes

### Configuration
- Customizable settings through config.ini
- Adjustable hotkeys for various functions
- Theme preferences
- Speech settings customization

## Project Structure

```
├── app/
│   ├── core/              # Core functionality
│   │   ├── ocr.py         # OCR processing
│   │   ├── speech.py      # Text-to-speech handling
│   │   ├── api.py         # API integrations
│   │   ├── screenshot.py  # Screen capture
│   │   └── image_analysis.py # Image analysis
│   ├── ui/                # User interface components
│   │   ├── ctk_main_window.py    # Main application window
│   │   ├── ctk_selection_window.py # Mode selection window
│   │   ├── ctk_theme.py          # Theme management
│   │   └── dialogs.py            # Dialog windows
│   ├── utils/             # Utility functions
│   │   ├── config.py      # Configuration handling
│   │   └── hotkey.py      # Hotkey management
│   └── main.py           # Application entry point
├── setup.py              # Dependency installation
├── run.py               # Runner script
└── run_screen_reader.bat # Windows batch launcher
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.
