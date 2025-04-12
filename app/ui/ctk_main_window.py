import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import re
from PIL import Image, ImageTk

from app.ui.dialogs import PreferencesDialog, APISettingsDialog, HotkeyDialog
from app.ui.ctk_theme import CTkTheme
from app.ui.ctk_selection_window import CTkSelectionWindow
from app.core.screenshot import ScreenshotTaker
from app.core.ocr import OCRProcessor
from app.core.api import GeminiAPI
from app.core.speech import SpeechService

class CTkMainWindow:
    def __init__(self, config_manager, hotkey_manager):
        self.config_manager = config_manager
        self.hotkey_manager = hotkey_manager

        # Set appearance mode based on system settings
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Initialize components
        self.root = ctk.CTk()
        self.root.title("Screenshot Assistant")
        self.root.geometry("800x600")

        # Initialize UI components
        self.status_var = tk.StringVar()
        self.progress_var = tk.StringVar(value="")
        self.mode_var = tk.StringVar()

        # Apply modern theme
        self.theme = CTkTheme.apply()
        self.colors = self.theme['colors']
        self.fonts = self.theme['fonts']
        self.animations = CTkTheme.configure_animations()

        # Initialize API and Speech Service
        self.gemini_api = GeminiAPI(self.config_manager)
        self.speech_service = SpeechService()

        # Setup UI
        self.setup_ui()

        # Setup hotkey
        self.hotkey_manager.start_listening(self.take_screenshot)

    def setup_ui(self):
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Header with app title and logo
        self.header_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.header_frame.grid_columnconfigure(1, weight=1)

        # App title with animation
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Screenshot Assistant",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors['primary']
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Mode selection frame
        self.mode_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        self.mode_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.mode_label = ctk.CTkLabel(self.mode_frame, text="Mode:")
        self.mode_label.grid(row=0, column=0, padx=(0, 10), pady=10)

        self.mode_var.set(self.config_manager.get('Settings', 'mode'))
        self.mode_options = ctk.CTkOptionMenu(
            self.mode_frame,
            values=["auto", "code", "general"],
            variable=self.mode_var,
            command=self.save_mode,
            width=120,
            dynamic_resizing=False
        )
        self.mode_options.grid(row=0, column=1, padx=5, pady=10)

        # Action buttons with modern styling
        self.button_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="e", padx=20)

        self.screenshot_btn = ctk.CTkButton(
            self.button_frame,
            text="Take Screenshot",
            command=self.take_screenshot,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark'],
            corner_radius=8,
            height=36
        )
        self.screenshot_btn.grid(row=0, column=0, padx=(0, 10), pady=10)

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_output,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_light'],
            corner_radius=8,
            height=36
        )
        self.clear_btn.grid(row=0, column=1, padx=(0, 10), pady=10)

        self.copy_btn = ctk.CTkButton(
            self.button_frame,
            text="Copy Response",
            command=self.copy_response,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_light'],
            corner_radius=8,
            height=36
        )
        self.copy_btn.grid(row=0, column=2, padx=(0, 10), pady=10)

        self.speak_btn = ctk.CTkButton(
            self.button_frame,
            text="Read Response",
            command=self.speak_response,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary_light'],
            corner_radius=8,
            height=36
        )
        self.speak_btn.grid(row=0, column=3, padx=(0, 10), pady=10)

        # Tabview for different outputs
        self.tabview = ctk.CTkTabview(self.root, corner_radius=10)
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))

        # Create tabs
        self.text_tab = self.tabview.add("Extracted Text")
        self.response_tab = self.tabview.add("AI Response")

        # Configure tab grid
        self.text_tab.grid_columnconfigure(0, weight=1)
        self.text_tab.grid_rowconfigure(0, weight=1)
        self.response_tab.grid_columnconfigure(0, weight=1)
        self.response_tab.grid_rowconfigure(0, weight=1)

        # Text output with modern styling
        self.text_output = ctk.CTkTextbox(
            self.text_tab,
            wrap="word",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            corner_radius=8,
            border_width=1,
            border_color=self.colors['border']
        )
        self.text_output.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Response output with modern styling
        self.response_output = ctk.CTkTextbox(
            self.response_tab,
            wrap="word",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            corner_radius=8,
            border_width=1,
            border_color=self.colors['border']
        )
        self.response_output.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Progress indicator for API call
        self.progress_frame = ctk.CTkFrame(self.response_tab, fg_color="transparent")
        self.progress_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.progress_label = ctk.CTkLabel(self.progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky="w")

        # Welcome message
        self.text_output.insert("0.0", "Welcome to Screenshot Assistant!\n")
        self.text_output.insert("end", f"Press {self.config_manager.get('API', 'hotkey')} to take a screenshot and analyze it.\n\n")
        self.text_output.insert("end", "Mode descriptions:\n")
        self.text_output.insert("end", "- auto: Automatically detects code questions and responds accordingly\n")
        self.text_output.insert("end", "- code: Forces responses to focus on coding solutions\n")
        self.text_output.insert("end", "- general: General purpose analysis\n")

        # Modern status bar
        self.status_frame = ctk.CTkFrame(self.root, corner_radius=0, height=30, fg_color=self.colors['surface'])
        self.status_frame.grid(row=3, column=0, sticky="ew")
        self.status_frame.grid_propagate(False)

        self.status_var.set("Ready")
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            textvariable=self.status_var,
            anchor="w",
            padx=20
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        # Settings button in status bar
        self.settings_btn = ctk.CTkButton(
            self.status_frame,
            text="Settings",
            command=self.show_settings_menu,
            fg_color="transparent",
            hover_color=self.colors['surface_variant'],
            corner_radius=6,
            width=80,
            height=24,
            border_width=1,
            border_color=self.colors['border']
        )
        self.settings_btn.grid(row=0, column=1, padx=(0, 20), pady=3, sticky="e")

        # Create settings menu
        self.settings_menu = tk.Menu(self.root, tearoff=0, bg=self.colors['surface'], fg=self.colors['text'])
        self.settings_menu.add_command(label="API Configuration", command=self.open_api_settings)
        self.settings_menu.add_command(label="Change Hotkey", command=self.change_hotkey)
        self.settings_menu.add_command(label="Preferences", command=self.open_preferences)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Exit", command=self.root.quit)

    def show_settings_menu(self):
        # Display the settings menu at the settings button position
        x = self.settings_btn.winfo_rootx()
        y = self.settings_btn.winfo_rooty()
        self.settings_menu.post(x, y)

    def save_mode(self, choice=None):
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
        self.status_var.set("Select area for screenshot...")
        self.root.update()

        # Minimize the window before taking screenshot
        self.root.iconify()
        import time
        time.sleep(0.5)  # Give time for the window to minimize

        try:
            # Create selection window and wait for region selection
            def handle_selection(region):
                if region:
                    # Take screenshot of selected region
                    screenshot = ScreenshotTaker.take_screenshot(region=region)
                    # Process the screenshot before restoring the window
                    self.process_screenshot(screenshot)
                    # Restore window after processing
                    self.root.after(100, self.root.deiconify)
                else:
                    # Restore window with a slight delay if cancelled
                    self.root.after(100, self.root.deiconify)
                    self.status_var.set("Screenshot cancelled")

            CTkSelectionWindow(self.root, handle_selection)
        except Exception as e:
            self.root.deiconify()
            self.status_var.set(f"Error: {str(e)}")

    def process_screenshot(self, screenshot):
        try:
            # Extract text from screenshot using OCR
            self.status_var.set("Extracting text...")
            self.root.update()

            text = OCRProcessor.extract_text(screenshot)

            if not text.strip():
                self.text_output.delete("0.0", "end")
                self.text_output.insert("0.0", "No text found in the screenshot.\n\n")
                self.status_var.set("Ready")
                return

            # Clear previous text
            self.text_output.delete("0.0", "end")
            self.text_output.insert("0.0", text + "\n\n")

            # Switch to text tab to show extracted content
            self.tabview.set("Extracted Text")

            # If API key is configured, send to Gemini
            if self.config_manager.get('API', 'gemini_api_key').strip():
                # Clear previous response before generating a new one
                self.response_output.delete("0.0", "end")
                self.progress_var.set("Generating response...")
                self.tabview.set("AI Response")  # Switch to response tab immediately to show progress
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
            self.text_output.insert("end", f"Error processing screenshot: {str(e)}\n\n")
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
            self.response_output.delete("0.0", "end")
            self.progress_var.set("")  # Clear progress indicator

            # Format the response for code if necessary
            if is_code_related and self.config_manager.getboolean('Settings', 'code_formatting'):
                self.format_code_response(response)
            else:
                self.response_output.insert("0.0", response)

            self.status_var.set("Ready")

            # Add a subtle animation to indicate new content
            self.animate_response_tab()

        except Exception as e:
            self.status_var.set(f"Error displaying response: {str(e)}")

    def animate_response_tab(self):
        """Create a subtle animation to draw attention to the response tab"""
        original_color = self.response_tab.cget("fg_color")
        highlight_color = self.colors['primary_light']

        def animate_color(step=0, max_steps=5):
            if step <= max_steps:
                # Alternate between highlight and original color
                color = highlight_color if step % 2 == 0 else original_color
                self.response_tab.configure(fg_color=color)
                self.root.after(150, lambda: animate_color(step + 1, max_steps))
            else:
                # Reset to original color
                self.response_tab.configure(fg_color=original_color)

        animate_color()

    def format_code_response(self, response):
        """Format response to highlight code blocks with improved styling."""
        # Configure text tags for different elements
        text_widget = self.response_output._textbox
        text_widget.tag_configure(
            "heading",
            font=("Segoe UI", 12, "bold"),
            spacing1=10,
            spacing3=5
        )
        text_widget.tag_configure(
            "code_block",
            font=("Consolas", 10),
            background="#F7F9FA",
            foreground="#2C3E50",
            spacing1=10,
            spacing3=10,
            relief="solid",
            borderwidth=1
        )
        text_widget.tag_configure(
            "language_tag",
            font=("Segoe UI", 10, "italic"),
            foreground="#666666"
        )

        # Split the response into sections
        sections = re.split(r'(#{1,6}\s.*?\n|```[\s\S]*?```|\d+\.\s.*?\n|•\s.*?\n|-\s.*?\n)', response)

        for section in sections:
            if not section or section.isspace():
                continue

            # Handle headers
            if re.match(r'#{1,6}\s', section):
                cleaned_header = re.sub(r'#{1,6}\s', '', section).strip()
                self.response_output.insert("end", cleaned_header + "\n", "heading")

            # Handle code blocks
            elif section.startswith('```'):
                code_content = section.strip('`').strip()
                lines = code_content.split('\n', 1)

                if len(lines) > 1 and not lines[0].strip().isspace():
                    language = lines[0].strip()
                    code = lines[1].rstrip()
                else:
                    language = "code"
                    code = code_content.rstrip()

                self.response_output.insert("end", "\n")
                if language != "code":
                    self.response_output.insert("end", f"Language: {language}\n", "language_tag")

                # Insert code with styling
                self.response_output.insert("end", code + "\n", "code_block")
                self.response_output.insert("end", "\n")

            # Handle bullet points and numbered lists
            elif re.match(r'(\d+\.|-|•)\s', section):
                self.response_output.insert("end", section)

            # Regular text
            else:
                cleaned_text = section.strip()
                if cleaned_text:
                    self.response_output.insert("end", cleaned_text + "\n")

    def copy_response(self):
        """Copy the current response to clipboard."""
        response_text = self.response_output.get("0.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(response_text)
        self.status_var.set("Response copied to clipboard")

        # Add a brief flash animation to confirm copy
        original_color = self.copy_btn.cget("fg_color")
        self.copy_btn.configure(fg_color=self.colors['success'])
        self.root.after(500, lambda: self.copy_btn.configure(fg_color=original_color))

    def speak_response(self):
        """Toggle between reading and stopping the AI response using text-to-speech."""
        if self.speech_service.is_speaking:
            self.speech_service.stop()
            self.speak_btn.configure(text="Read Response", fg_color=self.colors['accent'])
            self.set_status("Stopped reading")
            return

        response_text = self.response_output.get("0.0", "end").strip()
        if response_text:
            # Start speech in a separate thread to prevent UI freezing
            threading.Thread(target=self.speech_service.speak, args=(response_text,), daemon=True).start()
            self.speak_btn.configure(text="Stop Reading", fg_color=self.colors['primary'])
            self.set_status("Reading response...")

            # Add animation to the speak button
            self.animate_speak_button()
        else:
            self.set_status("No response to read")

    def animate_speak_button(self):
        """Create a pulsing animation for the speak button while speaking"""
        original_color = self.colors['primary']  # Use primary color as base for stop button

        def pulse(count=0):
            if self.speech_service.is_speaking:
                # Toggle between original and highlight color
                color = self.colors['primary_light'] if count % 2 == 0 else original_color
                self.speak_btn.configure(fg_color=color)
                self.root.after(500, lambda: pulse(count + 1))
            else:
                # Reset to accent color when stopped
                self.speak_btn.configure(text="Read Response", fg_color=self.colors['accent'])

        pulse()

    def clear_output(self):
        self.text_output.delete("0.0", "end")
        self.response_output.delete("0.0", "end")
        self.progress_var.set("")
        self.status_var.set("Output cleared")
        # Stop any ongoing speech
        self.speech_service.stop()

        # Add a brief animation to confirm clear
        original_color = self.clear_btn.cget("fg_color")
        self.clear_btn.configure(fg_color=self.colors['error'])
        self.root.after(300, lambda: self.clear_btn.configure(fg_color=original_color))

    def run(self):
        self.root.mainloop()
        self.hotkey_manager.stop_listening()
