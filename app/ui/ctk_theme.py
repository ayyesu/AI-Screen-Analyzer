import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class CTkTheme:
    # Modern color scheme with enhanced contrast and visual hierarchy
    COLORS = {
        'primary': '#2563eb',      # Vibrant Blue - Primary actions
        'primary_light': '#60a5fa', # Light Blue - Hover states
        'primary_dark': '#1d4ed8',  # Dark Blue - Active states
        'secondary': '#4b5563',    # Cool Gray - Secondary elements
        'secondary_light': '#9ca3af', # Light Gray - Disabled states
        'accent': '#8b5cf6',       # Purple - Accent elements
        'success': '#059669',      # Green - Success states
        'warning': '#d97706',      # Orange - Warning states
        'error': '#dc2626',        # Red - Error states
        'background': '#ffffff',    # White - Main background
        'surface': '#f8fafc',      # Lighter Gray - Card/Dialog background
        'surface_variant': '#f1f5f9', # Subtle Gray - Alternative surfaces
        'text': '#0f172a',         # Almost Black - Primary text
        'text_secondary': '#475569', # Dark Gray - Secondary text
        'border': '#e2e8f0'        # Border color
    }

    # Dark mode colors with improved contrast and readability
    DARK_COLORS = {
        'primary': '#3b82f6',      # Bright Blue - Primary actions
        'primary_light': '#60a5fa', # Light Blue - Hover states
        'primary_dark': '#2563eb',  # Dark Blue - Active states
        'secondary': '#9ca3af',    # Light Gray - Secondary elements
        'secondary_light': '#d1d5db', # Lighter Gray - Disabled states
        'accent': '#a78bfa',       # Light Purple - Accent elements
        'success': '#10b981',      # Light Green - Success states
        'warning': '#f59e0b',      # Light Orange - Warning states
        'error': '#ef4444',        # Light Red - Error states
        'background': '#0f172a',   # Dark Blue-Gray - Main background
        'surface': '#1e293b',      # Lighter Blue-Gray - Card/Dialog background
        'surface_variant': '#334155', # Medium Blue-Gray - Alternative surfaces
        'text': '#f8fafc',         # Almost White - Primary text
        'text_secondary': '#cbd5e1', # Light Gray - Secondary text
        'border': '#334155'        # Border color
    }

    @classmethod
    def apply(cls, dark_mode=False):
        colors = cls.DARK_COLORS if dark_mode else cls.COLORS

        # Configure CustomTkinter appearance mode and color theme
        ctk.set_appearance_mode("dark" if dark_mode else "light")

        # Create a custom color theme
        ctk.set_default_color_theme("blue")  # Base theme

        # Configure fonts
        default_font = ("Segoe UI", 10)
        text_font = ("Segoe UI", 10)
        heading_font = ("Segoe UI", 12, "bold")

        # Return theme info for custom widgets
        return {
            'colors': colors,
            'fonts': {
                'default': default_font,
                'text': text_font,
                'heading': heading_font
            }
        }

    @classmethod
    def configure_animations(cls):
        # Animation configuration
        return {
            'duration': 300,  # milliseconds
            'curve': 'ease_out'
        }

    @classmethod
    def get_button_hover_animation(cls, button, hover_color, normal_color):
        """Create hover animation for buttons"""
        def on_enter(e):
            button.configure(fg_color=hover_color)

        def on_leave(e):
            button.configure(fg_color=normal_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    @classmethod
    def get_frame_animation(cls, frame, start_value, end_value, duration=300):
        """Create animation for frame transitions"""
        steps = 20
        step_time = duration / steps
        step_size = (end_value - start_value) / steps

        def animate(step=0):
            if step <= steps:
                value = start_value + (step * step_size)
                # Convert numeric value to hex color string
                hex_value = f'#{int(value):02x}{int(value):02x}{int(value):02x}'
                frame.configure(fg_color=hex_value)
                frame.after(int(step_time), lambda: animate(step + 1))

        return animate
