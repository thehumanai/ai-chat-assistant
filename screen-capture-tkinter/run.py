import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

# --- Capture Logic Placeholder (to be implemented) ---
def capture_full_screen():
    # Placeholder: In a real app, use pyautogui or PIL.ImageGrab
    return Image.new('RGB', (400, 200), color='gray')

def capture_selected_area():
    # Placeholder: In a real app, implement area selection
    return Image.new('RGB', (200, 100), color='lightblue')

def capture_active_window():
    # Placeholder: In a real app, implement active window capture
    return Image.new('RGB', (300, 150), color='lightgreen')

# --- Settings ---
class Settings:
    def __init__(self):
        self.save_format = 'PNG'
        self.save_dir = os.path.expanduser('~')

# --- Main App ---
class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture App")
        self.root.geometry("700x400")
        self.settings = Settings()
        self.last_image = None
        self.last_image_path = None
        self.preview_imgtk = None

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Screen Capture App", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 10))

        # Button row
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        self._add_buttons(btn_frame)

        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(expand=True)

        # File format and save location
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))
        self._add_options(options_frame)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def _add_buttons(self, parent):
        ttk.Button(parent, text="Capture Full Screen", command=self.capture_full_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Capture Selected Area", command=self.capture_selected_area).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Capture Active Window", command=self.capture_active_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Save Screenshot", command=self.save_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Open Last Screenshot", command=self.open_last_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Settings", command=self.open_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

    def _add_options(self, parent):
        ttk.Label(parent, text="File Format:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value=self.settings.save_format)
        format_menu = ttk.Combobox(parent, textvariable=self.format_var, values=["PNG", "JPG"], width=5, state="readonly")
        format_menu.pack(side=tk.LEFT, padx=5)
        format_menu.bind('<<ComboboxSelected>>', self.update_format)

        ttk.Label(parent, text="Save Location:").pack(side=tk.LEFT, padx=(20, 0))
        self.save_dir_var = tk.StringVar(value=self.settings.save_dir)
        save_dir_entry = ttk.Entry(parent, textvariable=self.save_dir_var, width=30)
        save_dir_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_save_dir).pack(side=tk.LEFT, padx=5)

    # --- Button Actions ---
    def capture_full_screen(self):
        self.last_image = capture_full_screen()
        self._update_preview()
        self.status_var.set("Captured full screen")

    def capture_selected_area(self):
        self.last_image = capture_selected_area()
        self._update_preview()
        self.status_var.set("Captured selected area")

    def capture_active_window(self):
        self.last_image = capture_active_window()
        self._update_preview()
        self.status_var.set("Captured active window")

    def save_screenshot(self):
        if self.last_image is None:
            self.status_var.set("No screenshot to save")
            return
        filetypes = [(f"{self.format_var.get()} files", f"*.{self.format_var.get().lower()}")]
        default_ext = f".{self.format_var.get().lower()}"
        path = filedialog.asksaveasfilename(defaultextension=default_ext, filetypes=filetypes, initialdir=self.save_dir_var.get())
        if path:
            self.last_image.save(path, self.format_var.get())
            self.last_image_path = path
            self.status_var.set(f"Saved screenshot: {os.path.basename(path)}")
            self._update_preview(path)

    def copy_to_clipboard(self):
        if self.last_image is None:
            self.status_var.set("No screenshot to copy")
            return
        try:
            self.root.clipboard_clear()
            # Convert to Tk image and put on clipboard
            output = tk.PhotoImage(self.last_image)
            self.root.clipboard_append(output)
            self.status_var.set("Copied screenshot to clipboard")
        except Exception as e:
            self.status_var.set(f"Clipboard error: {e}")

    def open_last_screenshot(self):
        if self.last_image_path and os.path.exists(self.last_image_path):
            os.startfile(self.last_image_path)
            self.status_var.set("Opened last screenshot")
        else:
            self.status_var.set("No screenshot to open")

    def open_settings(self):
        messagebox.showinfo("Settings", "Settings dialog placeholder. (Add more options here!)")

    def update_format(self, event=None):
        self.settings.save_format = self.format_var.get()
        self.status_var.set(f"File format set to {self.format_var.get()}")

    def browse_save_dir(self):
        dir_selected = filedialog.askdirectory(initialdir=self.save_dir_var.get())
        if dir_selected:
            self.save_dir_var.set(dir_selected)
            self.settings.save_dir = dir_selected
            self.status_var.set(f"Save location set to {dir_selected}")

    def _update_preview(self, path=None):
        if self.last_image:
            # Resize for preview
            img = self.last_image.copy()
            img.thumbnail((300, 150))
            self.preview_imgtk = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self.preview_imgtk)
        else:
            self.preview_label.config(image='')

# --- Main Entrypoint ---
def main():
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
