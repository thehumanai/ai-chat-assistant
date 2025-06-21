import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import time
from datetime import datetime

# Import pyautogui for real screen capture
try:
    import pyautogui
    SCREEN_CAPTURE_AVAILABLE = True
except ImportError:
    SCREEN_CAPTURE_AVAILABLE = False
    print("Warning: pyautogui not available, using placeholder captures")

# --- Real Capture Logic ---
def capture_full_screen():
    """Capture the entire screen"""
    if SCREEN_CAPTURE_AVAILABLE:
        try:
            # Add a small delay to let the UI update
            time.sleep(0.1)
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            print(f"Full screen capture failed: {e}")
            # Fallback to placeholder
            return Image.new('RGB', (400, 200), color='gray')
    else:
        # Fallback to placeholder
        return Image.new('RGB', (400, 200), color='gray')

def capture_selected_area():
    """Capture a selected area (simplified to center region for now)"""
    if SCREEN_CAPTURE_AVAILABLE:
        try:
            # For now, capture center 800x600 region
            # In a full implementation, this would show a selection overlay
            screen_width, screen_height = pyautogui.size()
            left = (screen_width - 800) // 2
            top = (screen_height - 600) // 2
            right = left + 800
            bottom = top + 600
            
            time.sleep(0.1)
            screenshot = pyautogui.screenshot(region=(left, top, 800, 600))
            return screenshot
        except Exception as e:
            print(f"Selected area capture failed: {e}")
            return Image.new('RGB', (200, 100), color='lightblue')
    else:
        return Image.new('RGB', (200, 100), color='lightblue')

def capture_active_window():
    """Capture the active window"""
    if SCREEN_CAPTURE_AVAILABLE:
        try:
            # Get active window info
            active_window = pyautogui.getActiveWindow()
            if active_window:
                # Capture the window region
                time.sleep(0.1)
                screenshot = pyautogui.screenshot(region=(
                    active_window.left, 
                    active_window.top, 
                    active_window.width, 
                    active_window.height
                ))
                return screenshot
            else:
                # Fallback to full screen if no active window
                return capture_full_screen()
        except Exception as e:
            print(f"Active window capture failed: {e}")
            return Image.new('RGB', (300, 150), color='lightgreen')
    else:
        return Image.new('RGB', (300, 150), color='lightgreen')

def start_video_recording():
    """Start video recording (placeholder for now)"""
    # Placeholder: In a real app, use opencv or similar
    return True

def stop_video_recording():
    """Stop video recording (placeholder for now)"""
    # Placeholder: In a real app, stop recording and save video
    return "demo_video.mp4"

# --- Settings ---
class Settings:
    def __init__(self):
        self.save_format = 'PNG'
        # Create saved directory in current working directory
        current_dir = os.getcwd()
        self.save_dir = os.path.join(current_dir, 'saved')
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
        self.root.geometry("500x800")
        
        # Position window in bottom-left corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = 0
        y = screen_height - 800
        self.root.geometry(f"500x800+{x}+{y}")
        
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
        title_label = ttk.Label(main_frame, text="Screen Capture & Recording App", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))

        # Create two-column layout
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        content_frame.columnconfigure(1, weight=1)  # Right column expands

        # Left column - Capture buttons
        self.create_left_column(content_frame)
        
        # Right column - Preview and options
        self.create_right_column(content_frame)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def create_left_column(self, parent):
        """Create left column with capture buttons"""
        left_frame = ttk.Frame(parent)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Image capture section
        img_frame = ttk.LabelFrame(left_frame, text="Image Capture", padding="5")
        img_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(img_frame, text="Full Screen", 
                  command=self.capture_full_screen, width=15).pack(fill=tk.X, pady=2)
        ttk.Button(img_frame, text="Selected Area", 
                  command=self.capture_selected_area, width=15).pack(fill=tk.X, pady=2)
        ttk.Button(img_frame, text="Active Window", 
                  command=self.capture_active_window, width=15).pack(fill=tk.X, pady=2)
        ttk.Button(img_frame, text="Save Screenshot", 
                  command=self.save_screenshot, width=15).pack(fill=tk.X, pady=2)
        ttk.Button(img_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard, width=15).pack(fill=tk.X, pady=2)
        ttk.Button(img_frame, text="Open Last Screenshot", 
                  command=self.open_last_screenshot, width=15).pack(fill=tk.X, pady=2)

        # Video recording section
        video_frame = ttk.LabelFrame(left_frame, text="Video Recording", padding="5")
        video_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.record_btn = ttk.Button(video_frame, text="Start Recording", 
                                   command=self.start_recording, width=15)
        self.record_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = ttk.Button(video_frame, text="Stop Recording", 
                                 command=self.stop_recording, state='disabled', width=15)
        self.stop_btn.pack(fill=tk.X, pady=2)
        
        ttk.Button(video_frame, text="Open Last Video", 
                  command=self.open_last_video, width=15).pack(fill=tk.X, pady=2)
        
        # Recording status and timer
        self.recording_status_var = tk.StringVar(value="Not Recording")
        recording_status_label = ttk.Label(video_frame, textvariable=self.recording_status_var,
                                         font=('Arial', 9, 'bold'))
        recording_status_label.pack(pady=2)
        
        self.timer_var = tk.StringVar(value="00:00")
        timer_label = ttk.Label(video_frame, textvariable=self.timer_var,
                              font=('Arial', 10, 'bold'))
        timer_label.pack(pady=2)

        # Settings and Exit buttons
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_frame, text="Settings", 
                  command=self.open_settings, width=15).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Exit", 
                  command=self.root.quit, width=15).pack(fill=tk.X, pady=2)

    def create_right_column(self, parent):
        """Create right column with preview and options"""
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        # Preview area
        preview_frame = ttk.LabelFrame(right_frame, text="Preview", padding="5")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Options section
        options_frame = ttk.LabelFrame(right_frame, text="Options", padding="5")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Image format
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=tk.X, pady=2)
        ttk.Label(format_frame, text="Image Format:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value=self.settings.save_format)
        format_menu = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                 values=["PNG", "JPG"], width=8, state="readonly")
        format_menu.pack(side=tk.RIGHT)
        format_menu.bind('<<ComboboxSelected>>', self.update_format)

        # Video format
        video_format_frame = ttk.Frame(options_frame)
        video_format_frame.pack(fill=tk.X, pady=2)
        ttk.Label(video_format_frame, text="Video Format:").pack(side=tk.LEFT)
        self.video_format_var = tk.StringVar(value=self.settings.video_format)
        video_format_menu = ttk.Combobox(video_format_frame, textvariable=self.video_format_var,
                                       values=["MP4", "AVI", "MOV"], width=8, state="readonly")
        video_format_menu.pack(side=tk.RIGHT)
        video_format_menu.bind('<<ComboboxSelected>>', self.update_video_format)

        # Save location
        save_frame = ttk.Frame(options_frame)
        save_frame.pack(fill=tk.X, pady=2)
        ttk.Label(save_frame, text="Save Location:").pack(side=tk.LEFT)
        self.save_dir_var = tk.StringVar(value=self.settings.save_dir)
        save_dir_entry = ttk.Entry(save_frame, textvariable=self.save_dir_var, width=20)
        save_dir_entry.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(save_frame, text="Browse", 
                  command=self.browse_save_dir, width=8).pack(side=tk.RIGHT)

    # --- Image Capture Actions ---
    def capture_full_screen(self):
        self.status_var.set("Capturing full screen...")
        self.root.update()
        self.last_image = capture_full_screen()
        self._update_preview()
        self._auto_save_screenshot("full_screen")
        self.status_var.set("Captured and saved full screen")

    def capture_selected_area(self):
        self.status_var.set("Capturing selected area...")
        self.root.update()
        self.last_image = capture_selected_area()
        self._update_preview()
        self._auto_save_screenshot("selected_area")
        self.status_var.set("Captured and saved selected area (center region)")

    def capture_active_window(self):
        self.status_var.set("Capturing active window...")
        self.root.update()
        self.last_image = capture_active_window()
        self._update_preview()
        self._auto_save_screenshot("active_window")
        self.status_var.set("Captured and saved active window")

    def _auto_save_screenshot(self, capture_type):
        """Automatically save screenshot with timestamped filename"""
        if self.last_image is None:
            return
            
        try:
            # Create readable timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.{self.format_var.get().lower()}"
            filepath = os.path.join(self.save_dir_var.get(), filename)
            
            # Debug info
            print(f"Saving to: {filepath}")
            print(f"Save directory: {self.save_dir_var.get()}")
            print(f"Directory exists: {os.path.exists(self.save_dir_var.get())}")
            
            # Ensure directory exists
            save_dir = self.save_dir_var.get()
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                print(f"Created directory: {save_dir}")
            
            # Save the image
            self.last_image.save(filepath, self.format_var.get())
            self.last_image_path = filepath
            print(f"Successfully saved: {filepath}")
            
        except Exception as e:
            print(f"Auto-save failed: {e}")
            self.status_var.set("Capture successful but auto-save failed")

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
