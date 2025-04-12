import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class ModernTheme:
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
    def apply(cls, root, dark_mode=False):
        colors = cls.DARK_COLORS if dark_mode else cls.COLORS

        # Configure fonts
        default_font = tkfont.nametofont('TkDefaultFont')
        default_font.configure(family='Segoe UI', size=10)

        text_font = tkfont.Font(family='Segoe UI', size=10)
        heading_font = tkfont.Font(family='Segoe UI', size=12, weight='bold')

        # Configure styles
        style = ttk.Style(root)
        style.configure('.',
            background=colors['background'],
            foreground=colors['text'],
            font=default_font)

        # Notebook style
        style.configure('TNotebook',
            background=colors['background'],
            tabmargins=[2, 5, 2, 0])

        style.configure('TNotebook.Tab',
            padding=[12, 6],
            background=colors['surface_variant'],
            foreground=colors['text_secondary'])

        style.map('TNotebook.Tab',
            background=[('selected', colors['primary']), ('active', colors['primary_light'])],
            foreground=[('selected', colors['background']), ('active', colors['text'])])

        # Button style with enhanced visibility
        style.configure('TButton',
            padding=[12, 8],
            background=colors['primary'],
            foreground=colors['text'],
            relief='flat',
            borderwidth=0,
            font=('Segoe UI', 10, 'bold'))

        style.map('TButton',
            background=[('active', colors['primary_dark']), ('disabled', colors['secondary_light'])],
            foreground=[('active', '#ffffff'), ('disabled', colors['text_secondary'])],
            relief=[('pressed', 'sunken'), ('active', 'flat')])

        # Accent button style for primary actions
        style.configure('Accent.TButton',
            padding=[12, 8],
            background=colors['accent'],
            foreground=colors['text'],
            relief='flat',
            borderwidth=0,
            font=('Segoe UI', 10, 'bold'))

        style.map('Accent.TButton',
            background=[('active', colors['accent']), ('disabled', colors['secondary_light'])],
            foreground=[('active', '#ffffff'), ('disabled', colors['text_secondary'])],
            relief=[('pressed', 'sunken'), ('active', 'flat')])

        # Entry style
        style.configure('TEntry',
            padding=[8, 4],
            fieldbackground=colors['surface'],
            foreground=colors['text'],
            bordercolor=colors['border'],
            relief='solid',
            borderwidth=1)

        # Combobox style
        style.configure('TCombobox',
            padding=[5, 3],
            fieldbackground=colors['surface'],
            foreground=colors['text'],
            arrowcolor=colors['primary'])

        # Frame style
        style.configure('TFrame',
            background=colors['background'])

        # Label style
        style.configure('TLabel',
            background=colors['background'],
            foreground=colors['text'])

        # Apply colors to non-ttk widgets
        root.configure(bg=colors['background'])

        # Return theme info for custom widgets
        return {
            'colors': colors,
            'fonts': {
                'default': default_font,
                'text': text_font,
                'heading': heading_font
            }
        }
