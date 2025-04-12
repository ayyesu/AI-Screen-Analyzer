import tkinter as tk

class SelectionWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback

        # Create fullscreen transparent window
        self.window = tk.Toplevel(parent)
        self.window.attributes('-alpha', 0.3, '-fullscreen', True, '-topmost', True)
        self.window.configure(bg='gray')

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

    def on_click(self, event):
        # Store initial coordinates
        self.start_x = event.x
        self.start_y = event.y

        # Create initial rectangle
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='white', width=2
        )

    def on_drag(self, event):
        # Update rectangle as mouse is dragged
        if self.current_rect:
            self.canvas.coords(
                self.current_rect,
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

            # Close window and return coordinates
            self.window.destroy()
            self.callback((x1, y1, x2, y2))

    def cancel(self, event=None):
        # Cancel selection
        self.window.destroy()
        self.callback(None)
