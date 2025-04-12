import customtkinter as ctk
import tkinter as tk

class CTkSelectionWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback

        # Create fullscreen transparent window
        self.window = ctk.CTkToplevel(parent)
        self.window.state('zoomed')  # Ensure window is maximized

        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Configure window to cover entire screen
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.lift()  # Lift window to top
        self.window.attributes('-alpha', 0.3, '-topmost', True, '-fullscreen', True)
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.configure(fg_color="black")  # Darker background for better contrast

        # Initialize selection coordinates
        self.start_x = None
        self.start_y = None
        self.current_rect = None

        # Bind mouse events
        self.window.bind('<Button-1>', self.on_click)
        self.window.bind('<B1-Motion>', self.on_drag)
        self.window.bind('<ButtonRelease-1>', self.on_release)
        self.window.bind('<Escape>', self.cancel)

        # Create canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.window, highlightthickness=0)
        self.canvas.configure(bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set crosshair cursor
        self.canvas.configure(cursor='crosshair')

        # Add instruction label
        self.instruction_frame = ctk.CTkFrame(self.window, fg_color="#000000", corner_radius=10)
        self.instruction_frame.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.instruction_label = ctk.CTkLabel(
            self.instruction_frame,
            text="Click and drag to select an area for screenshot",
            font=("Segoe UI", 14),
            text_color="white",
            padx=20,
            pady=10
        )
        self.instruction_label.pack()

        # Add cancel button
        self.cancel_button = ctk.CTkButton(
            self.window,
            text="Cancel",
            command=lambda: self.cancel(),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            corner_radius=8,
            font=("Segoe UI", 12),
            width=100,
            height=35
        )
        self.cancel_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        # Add animation effect for instruction
        self.animate_instruction()

    def animate_instruction(self):
        """Create a subtle pulsing animation for the instruction label"""
        def pulse(direction=1, alpha=0.9):
            if not hasattr(self, 'instruction_frame'):
                return  # Stop if window is closed

            # Update alpha
            alpha += direction * 0.01
            if alpha >= 1.0:
                direction = -1
                alpha = 1.0
            elif alpha <= 0.7:
                direction = 1
                alpha = 0.7

            # Use a semi-transparent black color
            self.instruction_frame.configure(fg_color="gray10")

            # Schedule next update
            self.window.after(50, lambda: pulse(direction, alpha))

        # Start animation
        pulse()

    def on_click(self, event):
        # Store initial coordinates
        self.start_x = event.x
        self.start_y = event.y

        # Create initial rectangle
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='#2563eb', width=2
        )

        # Create a semi-transparent fill
        self.current_fill = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='', fill='#2563eb', stipple='gray25'
        )

    def on_drag(self, event):
        # Update rectangle as mouse is dragged
        if self.current_rect:
            self.canvas.coords(
                self.current_rect,
                self.start_x, self.start_y,
                event.x, event.y
            )
            self.canvas.coords(
                self.current_fill,
                self.start_x, self.start_y,
                event.x, event.y
            )

    def on_release(self, event):
        if self.start_x is not None and self.start_y is not None:
            # Get the selection coordinates
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)

            # Minimum size check
            if (x2 - x1) < 10 or (y2 - y1) < 10:
                # Selection too small, ignore
                return

            # Flash effect before closing
            self.flash_selection()

            # Schedule callback after animation
            self.window.after(300, lambda: self.finish_selection((x1, y1, x2, y2)))

    def flash_selection(self):
        """Create a flash effect on the selection"""
        # Change to a highlight color
        self.canvas.itemconfig(self.current_rect, outline='#10b981', width=3)
        self.canvas.itemconfig(self.current_fill, fill='#10b981')

    def finish_selection(self, coords):
        # Close window and return coordinates
        self.window.destroy()
        self.callback(coords)

    def cancel(self, event=None):
        # Cancel selection with fade out effect
        self.fade_out()

    def fade_out(self, alpha=1.0):
        """Create a fade out effect when canceling"""
        if alpha > 0:
            self.window.attributes('-alpha', alpha)
            self.window.after(20, lambda: self.fade_out(alpha - 0.1))
        else:
            # Close window and return None
            self.window.destroy()
            self.callback(None)
