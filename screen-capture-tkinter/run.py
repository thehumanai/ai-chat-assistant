import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import time
from datetime import datetime

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

def start_video_recording():
    # Placeholder: In a real app, use opencv or similar
    return True

def stop_video_recording():
    # Placeholder: In a real app, stop recording and save video
    return "demo_video.mp4"

# --- Settings ---
class Settings:
    def __init__(self):
        self.save_format = 'PNG'
        # Create screen-capture directory in user's home directory
        self.save_dir = os.path.join(os.path.expanduser('~'), 'screen-capture')
        # Ensure the directory exists
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.video_format = 'MP4'
        self.is_recording = False

# --- Main App ---
class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture & Recording App")
        self.root.geometry("800x500")
        self.settings = Settings()
        self.last_image = None
        self.last_image_path = None
        self.last_video_path = None
        self.preview_imgtk = None
        self.recording_start_time = None

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Screen Capture & Recording App", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 10))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Image capture tab
        self.create_image_tab()
        
        # Video recording tab
        self.create_video_tab()

        # File format and save location
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))
        self._add_options(options_frame)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def create_image_tab(self):
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text="Image Capture")
        
        # Image capture buttons
        img_btn_frame = ttk.LabelFrame(image_frame, text="Image Capture", padding="10")
        img_btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(img_btn_frame, text="Capture Full Screen", 
                  command=self.capture_full_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Capture Selected Area", 
                  command=self.capture_selected_area).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Capture Active Window", 
                  command=self.capture_active_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Save Screenshot", 
                  command=self.save_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Open Last Screenshot", 
                  command=self.open_last_screenshot).pack(side=tk.LEFT, padx=5)

        # Preview area
        preview_frame = ttk.LabelFrame(image_frame, text="Image Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(expand=True)

    def create_video_tab(self):
        video_frame = ttk.Frame(self.notebook)
        self.notebook.add(video_frame, text="Video Recording")
        
        # Video recording controls
        video_controls_frame = ttk.LabelFrame(video_frame, text="Video Recording", padding="10")
        video_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Recording buttons
        self.record_btn = ttk.Button(video_controls_frame, text="Start Recording", 
                                   command=self.start_recording)
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(video_controls_frame, text="Stop Recording", 
                                 command=self.stop_recording, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(video_controls_frame, text="Open Last Video", 
                  command=self.open_last_video).pack(side=tk.LEFT, padx=5)
        
        # Recording status
        self.recording_status_var = tk.StringVar(value="Not Recording")
        recording_status_label = ttk.Label(video_controls_frame, 
                                         textvariable=self.recording_status_var,
                                         font=('Arial', 10, 'bold'))
        recording_status_label.pack(side=tk.RIGHT, padx=5)
        
        # Recording timer
        self.timer_var = tk.StringVar(value="00:00")
        timer_label = ttk.Label(video_controls_frame, textvariable=self.timer_var,
                              font=('Arial', 12, 'bold'))
        timer_label.pack(side=tk.RIGHT, padx=5)
        
        # Video preview area
        video_preview_frame = ttk.LabelFrame(video_frame, text="Video Preview", padding="10")
        video_preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for video preview
        video_placeholder = ttk.Label(video_preview_frame, 
                                    text="Video preview will appear here\nwhen recording starts",
                                    font=('Arial', 12))
        video_placeholder.pack(expand=True)

    def _add_options(self, parent):
        # Image format
        ttk.Label(parent, text="Image Format:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value=self.settings.save_format)
        format_menu = ttk.Combobox(parent, textvariable=self.format_var, 
                                 values=["PNG", "JPG"], width=5, state="readonly")
        format_menu.pack(side=tk.LEFT, padx=5)
        format_menu.bind('<<ComboboxSelected>>', self.update_format)

        # Video format
        ttk.Label(parent, text="Video Format:").pack(side=tk.LEFT, padx=(20, 0))
        self.video_format_var = tk.StringVar(value=self.settings.video_format)
        video_format_menu = ttk.Combobox(parent, textvariable=self.video_format_var,
                                       values=["MP4", "AVI", "MOV"], width=5, state="readonly")
        video_format_menu.pack(side=tk.LEFT, padx=5)
        video_format_menu.bind('<<ComboboxSelected>>', self.update_video_format)

        # Save location
        ttk.Label(parent, text="Save Location:").pack(side=tk.LEFT, padx=(20, 0))
        self.save_dir_var = tk.StringVar(value=self.settings.save_dir)
        save_dir_entry = ttk.Entry(parent, textvariable=self.save_dir_var, width=30)
        save_dir_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_save_dir).pack(side=tk.LEFT, padx=5)

        # Settings and Exit buttons
        ttk.Button(parent, text="Settings", command=self.open_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(parent, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

    # --- Image Capture Actions ---
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
        path = filedialog.asksaveasfilename(defaultextension=default_ext, filetypes=filetypes, 
                                          initialdir=self.save_dir_var.get())
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

    # --- Video Recording Actions ---
    def start_recording(self):
        if not self.settings.is_recording:
            self.settings.is_recording = True
            self.recording_start_time = time.time()
            self.record_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.recording_status_var.set("Recording...")
            self.status_var.set("Started video recording")
            
            # Start recording timer
            self.update_recording_timer()
            
            # Start actual recording (placeholder)
            if start_video_recording():
                self.status_var.set("Video recording started successfully")

    def stop_recording(self):
        if self.settings.is_recording:
            self.settings.is_recording = False
            self.record_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.recording_status_var.set("Not Recording")
            self.timer_var.set("00:00")
            
            # Stop actual recording (placeholder)
            video_path = stop_video_recording()
            if video_path:
                self.last_video_path = os.path.join(self.save_dir_var.get(), video_path)
                self.status_var.set(f"Recording stopped. Saved as: {video_path}")
            else:
                self.status_var.set("Recording stopped")

    def update_recording_timer(self):
        if self.settings.is_recording and self.recording_start_time:
            elapsed = int(time.time() - self.recording_start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_var.set(f"{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_recording_timer)

    def open_last_video(self):
        if self.last_video_path and os.path.exists(self.last_video_path):
            os.startfile(self.last_video_path)
            self.status_var.set("Opened last video")
        else:
            self.status_var.set("No video to open")

    # --- Settings and Options ---
    def open_settings(self):
        settings_text = """Settings Dialog (Placeholder)

Available Settings:
• Image Quality
• Video Quality
• Recording Duration
• Hotkeys
• Auto-save options

This would open a proper settings dialog in a real implementation."""
        messagebox.showinfo("Settings", settings_text)

    def update_format(self, event=None):
        self.settings.save_format = self.format_var.get()
        self.status_var.set(f"Image format set to {self.format_var.get()}")

    def update_video_format(self, event=None):
        self.settings.video_format = self.video_format_var.get()
        self.status_var.set(f"Video format set to {self.video_format_var.get()}")

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
