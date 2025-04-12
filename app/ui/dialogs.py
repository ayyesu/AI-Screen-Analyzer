import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import keyboard
from app.ui.ctk_theme import CTkTheme

class PreferencesDialog:
    def __init__(self, parent, config_manager, status_callback):
        self.parent = parent
        self.config_manager = config_manager
        self.status_callback = status_callback

    def open(self):
        pref_window = tk.Toplevel(self.parent)
        pref_window.title("Preferences")
        pref_window.geometry("400x300")
        pref_window.transient(self.parent)
        pref_window.grab_set()

        # Apply theme
        theme = CTkTheme.apply()
        colors = CTkTheme.COLORS

        # Main container
        main_frame = ttk.Frame(pref_window, padding="20 15 20 15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, text="General Settings", font=('Helvetica', 14, 'bold'))
        header.pack(pady=(0, 20))

        # Settings container
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.BOTH, expand=True)

        # Code formatting option
        code_format_var = tk.BooleanVar(value=self.config_manager.getboolean('Settings', 'code_formatting'))
        code_format_check = ttk.Checkbutton(
            settings_frame,
            text="Apply syntax highlighting to code",
            variable=code_format_var
        )
        code_format_check.pack(anchor=tk.W, pady=5)

        # Button container
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # Save button
        def save_preferences():
            self.config_manager.set('Settings', 'code_formatting', str(code_format_var.get()))
            pref_window.destroy()
            self.status_callback("Preferences saved")

        save_btn = ttk.Button(
            button_frame,
            text="Save",
            command=save_preferences,
            style='Accent.TButton'
        )
        save_btn.pack(side=tk.RIGHT)

class APISettingsDialog:
    def __init__(self, parent, config_manager, status_callback):
        self.parent = parent
        self.config_manager = config_manager
        self.status_callback = status_callback

    def open(self):
        api_key = simpledialog.askstring("API Configuration",
                                        "Enter your Gemini API Key:",
                                        initialvalue=self.config_manager.get('API', 'gemini_api_key'))
        if api_key:
            self.config_manager.set('API', 'gemini_api_key', api_key)
            self.status_callback("API key updated")

class HotkeyDialog:
    def __init__(self, parent, config_manager, status_callback):
        self.parent = parent
        self.config_manager = config_manager
        self.status_callback = status_callback

    def open(self):
        # Show dialog explaining how to set a new hotkey
        messagebox.showinfo("Change Hotkey",
                          f"Current hotkey is: {self.config_manager.get('API', 'hotkey')}\n\n"
                          "Please press the new key combination you want to use.\n"
                          "For example: ctrl+shift+a")

        # Record the new hotkey
        def on_hotkey(e):
            # Convert the key event to a string representation
            key_combo = []
            if e.event_type == keyboard.KEY_DOWN:
                if keyboard.is_pressed('ctrl'):
                    key_combo.append('ctrl')
                if keyboard.is_pressed('alt'):
                    key_combo.append('alt')
                if keyboard.is_pressed('shift'):
                    key_combo.append('shift')

                # Add the main key if it's not a modifier
                if e.name not in ['ctrl', 'alt', 'shift']:
                    key_combo.append(e.name)

                if key_combo:
                    new_hotkey = '+'.join(key_combo)
                    self.config_manager.set('API', 'hotkey', new_hotkey)
                    messagebox.showinfo("Hotkey Changed", f"New hotkey set to: {new_hotkey}")
                    keyboard.unhook_all()
                    return False

        # Hook for recording the new hotkey
        keyboard.hook(on_hotkey)
