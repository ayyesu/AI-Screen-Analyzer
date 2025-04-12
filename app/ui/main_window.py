import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import re

from app.ui.dialogs import PreferencesDialog, APISettingsDialog, HotkeyDialog
from app.ui.theme import ModernTheme
from app.core.screenshot import ScreenshotTaker
from app.core.ocr import OCRProcessor
from app.core.api import GeminiAPI
from app.core.speech import SpeechService

class MainWindow:
    def __init__(self, config_manager, hotkey_manager):
        self.config_manager = config_manager
        self.hotkey_manager = hotkey_manager

        # Initialize components
        self.root = tk.Tk()
        self.root.title("Screenshot Assistant")
        self.root.geometry("800x600")

        # Initialize UI components
        self.status_var = tk.StringVar()
        self.progress_var = tk.StringVar(value="")
        self.mode_var = tk.StringVar()

        # Apply modern theme
        self.theme = ModernTheme.apply(self.root)
        self.colors = self.theme['colors']
        self.fonts = self.theme['fonts']

        # Initialize API and Speech Service
        self.gemini_api = GeminiAPI(self.config_manager)
        self.speech_service = SpeechService()

        # Setup UI
        self.setup_ui()

        # Setup hotkey
        self.hotkey_manager.start_listening(self.take_screenshot)

    def setup_ui(self):
        # Menu bar with modern styling
        menu_bar = tk.Menu(self.root, bg=self.colors['background'], fg=self.colors['text'])
        self.root.config(menu=menu_bar)

        settings_menu = tk.Menu(menu_bar, tearoff=0, bg=self.colors['background'], fg=self.colors['text'])
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="API Configuration", command=self.open_api_settings)
        settings_menu.add_command(label="Change Hotkey", command=self.change_hotkey)
        settings_menu.add_command(label="Preferences", command=self.open_preferences)
        settings_menu.add_separator()
        settings_menu.add_command(label="Exit", command=self.root.quit)

        # Main container with modern styling
        main_frame = ttk.Frame(self.root, padding="20 15 20 15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with app title
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(header_frame, text="Screenshot Assistant",
                               font=self.fonts['heading'])
        title_label.pack(side=tk.LEFT)

        # Mode frame with modern styling
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        mode_label = ttk.Label(mode_frame, text="Mode:")
        mode_label.pack(side=tk.LEFT, padx=(0, 10))

        self.mode_var.set(self.config_manager.get('Settings', 'mode'))
        mode_options = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                   values=["auto", "code", "general"], width=15)
        mode_options.pack(side=tk.LEFT)
        mode_options.bind("<<ComboboxSelected>>", self.save_mode)

        # Action buttons with modern styling
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        screenshot_btn = ttk.Button(button_frame, text="Take Screenshot",
                                  command=self.take_screenshot, style='Accent.TButton')
        screenshot_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = ttk.Button(button_frame, text="Clear",
                              command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        copy_btn = ttk.Button(button_frame, text="Copy Response",
                             command=self.copy_response)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))

        speak_btn = ttk.Button(button_frame, text="Read Response",
                            command=self.speak_response)
        speak_btn.pack(side=tk.LEFT)

        # Notebook for different outputs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Text tab with modern styling
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="Extracted Text")

        self.text_output = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            height=12,
            font=self.fonts['text'],
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground=self.colors['background'],
            padx=10,
            pady=10
        )
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Response tab with modern styling
        response_frame = ttk.Frame(self.notebook)
        self.notebook.add(response_frame, text="AI Response")

        self.response_output = scrolledtext.ScrolledText(
            response_frame,
            wrap=tk.WORD,
            height=15,
            font=self.fonts['text'],
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground=self.colors['background'],
            padx=10,
            pady=10
        )
        self.response_output.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Progress indicator for API call
        self.progress_label = tk.Label(response_frame, textvariable=self.progress_var)
        self.progress_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Welcome message
        self.text_output.insert(tk.END, "Welcome to Screenshot Assistant!\n")
        self.text_output.insert(tk.END, f"Press {self.config_manager.get('API', 'hotkey')} to take a screenshot and analyze it.\n\n")
        self.text_output.insert(tk.END, "Mode descriptions:\n")
        self.text_output.insert(tk.END, "- auto: Automatically detects code questions and responds accordingly\n")
        self.text_output.insert(tk.END, "- code: Forces responses to focus on coding solutions\n")
        self.text_output.insert(tk.END, "- general: General purpose analysis\n")

        # Modern status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_var.set("Ready")
        status_bar = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            padding="10 5",
            background=self.colors['surface']
        )
        status_bar.pack(fill=tk.X)

    def save_mode(self, event=None):
        self.config_manager.set('Settings', 'mode', self.mode_var.get())
        self.status_var.set(f"Mode set to: {self.mode_var.get()}")

    def open_preferences(self):
        dialog = PreferencesDialog(self.root, self.config_manager, self.set_status)
        dialog.open()

    def open_api_settings(self):
        dialog = APISettingsDialog(self.root, self.config_manager, self.set_status)
        dialog.open()

    def change_hotkey(self):
        dialog = HotkeyDialog(self.root, self.config_manager, self.set_status)
        dialog.open()

    def set_status(self, message):
        self.status_var.set(message)

    def take_screenshot(self):
        self.status_var.set("Taking screenshot...")
        self.root.update()

        # Minimize the window before taking screenshot
        self.root.iconify()
        import time
        time.sleep(0.5)  # Give time for the window to minimize

        try:
            # Take the screenshot
            screenshot = ScreenshotTaker.take_screenshot()

            # Restore the window
            self.root.deiconify()

            # Process the screenshot
            self.process_screenshot(screenshot)

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.root.deiconify()

    def process_screenshot(self, screenshot):
        try:
            # Extract text from screenshot using OCR
            self.status_var.set("Extracting text...")
            self.root.update()

            text = OCRProcessor.extract_text(screenshot)

            if not text.strip():
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, "No text found in the screenshot.\n\n")
                self.status_var.set("Ready")
                return

            # Clear previous text
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, text + "\n\n")

            # Switch to text tab to show extracted content
            self.notebook.select(0)

            # If API key is configured, send to Gemini
            if self.config_manager.get('API', 'gemini_api_key').strip():
                # Clear previous response before generating a new one
                self.response_output.delete(1.0, tk.END)
                self.progress_var.set("Generating response...")
                self.notebook.select(1)  # Switch to response tab immediately to show progress
                self.status_var.set("Sending to Gemini API...")
                self.root.update()

                # Determine if the content is code-related
                mode = self.config_manager.get('Settings', 'mode')
                is_code_related = OCRProcessor.detect_code_content(text) if mode == "auto" else (mode == "code")

                # Start a thread to process the API request to avoid UI freezing
                threading.Thread(target=self.process_gemini_request,
                                args=(text, is_code_related)).start()
            else:
                messagebox.showwarning("API Key Missing",
                                     "Please set your Gemini API key in Settings > API Configuration")

        except Exception as e:
            self.text_output.insert(tk.END, f"Error processing screenshot: {str(e)}\n\n")
            self.status_var.set("Error")

    def process_gemini_request(self, text, is_code_related):
        try:
            response = self.gemini_api.query_gemini(text, is_code_related)

            # Use the after method to update UI from the main thread
            self.root.after(0, self.update_response_ui, response, is_code_related)

        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))

    def update_response_ui(self, response, is_code_related):
        """Update the UI with the Gemini response (called from main thread)"""
        try:
            # Clear previous response
            self.response_output.delete(1.0, tk.END)
            self.progress_var.set("")  # Clear progress indicator

            # Format the response for code if necessary
            if is_code_related and self.config_manager.getboolean('Settings', 'code_formatting'):
                self.format_code_response(response)
            else:
                self.response_output.insert(tk.END, response)

            self.status_var.set("Ready")

        except Exception as e:
            self.status_var.set(f"Error displaying response: {str(e)}")

    def format_code_response(self, response):
        """Format response to highlight code blocks."""
        # Split the response by code blocks marked with ```
        parts = re.split(r'(```[\s\S]*?```)', response)

        for part in parts:
            if part.startswith('```'):
                # This is a code block, format it accordingly
                code_content = part.strip('`').strip()

                # Check if the first line specifies a language
                lines = code_content.split('\n', 1)
                if len(lines) > 1 and not lines[0].strip().isspace():
                    language = lines[0].strip()
                    code = lines[1]
                else:
                    language = "code"
                    code = code_content

                self.response_output.insert(tk.END, f"# {language} code:\n", "code_language")
                self.response_output.insert(tk.END, code + "\n\n", "code_block")
            else:
                # Regular text
                self.response_output.insert(tk.END, part)

        # Apply tags for syntax highlighting
        self.response_output.tag_configure("code_language", foreground="blue", font=("Courier", 10, "bold"))
        self.response_output.tag_configure("code_block", background="#f5f5f5", font=("Courier", 10))

    def copy_response(self):
        """Copy the current response to clipboard."""
        response_text = self.response_output.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(response_text)
        self.status_var.set("Response copied to clipboard")

    def speak_response(self):
        """Read the AI response using text-to-speech."""
        response_text = self.response_output.get("1.0", tk.END).strip()
        if response_text:
            # Start speech in a separate thread to prevent UI freezing
            threading.Thread(target=self.speech_service.speak, args=(response_text,), daemon=True).start()
            self.set_status("Reading response...")
        else:
            self.set_status("No response to read")

    def clear_output(self):
        self.text_output.delete(1.0, tk.END)
        self.response_output.delete(1.0, tk.END)
        self.progress_var.set("")
        self.status_var.set("Output cleared")
        # Stop any ongoing speech
        self.speech_service.stop()

    def run(self):
        self.root.mainloop()
        self.hotkey_manager.stop_listening()
