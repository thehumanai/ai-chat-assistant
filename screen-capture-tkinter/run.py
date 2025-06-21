import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import time
from datetime import datetime
import pyautogui
import threading
import json
import subprocess
from pathlib import Path
import sys
import cv2
import numpy as np

# --- Settings ---
class Settings:
    def __init__(self):
        self.config_file = "settings.json"
        self.save_format = "PNG"
        self.video_format = "MP4"
        self.save_dir = os.path.join(os.getcwd(), "saved")
        self.video_duration_seconds = 10  # Default 10 seconds for debugging
        
        # Resolution settings
        self.resolution_width = 1280  # 720p default
        self.resolution_height = 720
        self.resolution_preset = "720p"
        
        self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.save_format = data.get('save_format', self.save_format)
                    self.video_format = data.get('video_format', self.video_format)
                    self.save_dir = data.get('save_dir', self.save_dir)
                    self.video_duration_seconds = data.get('video_duration_seconds', self.video_duration_seconds)
                    self.resolution_width = data.get('resolution_width', self.resolution_width)
                    self.resolution_height = data.get('resolution_height', self.resolution_height)
                    self.resolution_preset = data.get('resolution_preset', self.resolution_preset)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        try:
            data = {
                'save_format': self.save_format,
                'video_format': self.video_format,
                'save_dir': self.save_dir,
                'video_duration_seconds': self.video_duration_seconds,
                'resolution_width': self.resolution_width,
                'resolution_height': self.resolution_height,
                'resolution_preset': self.resolution_preset
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def set_resolution_preset(self, preset):
        """Set resolution based on preset"""
        presets = {
            "480p": (854, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "1440p": (2560, 1440),
            "4K": (3840, 2160)
        }
        if preset in presets:
            self.resolution_width, self.resolution_height = presets[preset]
            self.resolution_preset = preset

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
        
        # Video recording attributes
        self.is_recording = False
        self.recording_thread = None
        self.frames_captured = 0
        self.frames_per_second = 24  # Changed from frames_per_minute to frames_per_second
        self.video_duration_seconds = self.settings.video_duration_seconds
        self.captured_frames = []
        self.current_video_start_time = None
        self.video_segments_created = 0  # Track number of video segments created

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
        
        # Video recording progress
        self.video_progress_var = tk.StringVar(value="Frames: 0 | Segments: 0")
        video_progress_label = ttk.Label(video_frame, textvariable=self.video_progress_var,
                                       font=('Arial', 8))
        video_progress_label.pack(pady=2)

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

        # Video duration
        duration_frame = ttk.Frame(options_frame)
        duration_frame.pack(fill=tk.X, pady=2)
        ttk.Label(duration_frame, text="Video Duration (seconds):").pack(side=tk.LEFT)
        duration_var = tk.StringVar(value=str(self.settings.video_duration_seconds))
        duration_entry = ttk.Entry(duration_frame, textvariable=duration_var, width=10)
        duration_entry.pack(side=tk.RIGHT)
        
        # Resolution preset
        resolution_preset_frame = ttk.Frame(options_frame)
        resolution_preset_frame.pack(fill=tk.X, pady=2)
        ttk.Label(resolution_preset_frame, text="Resolution Preset:").pack(side=tk.LEFT)
        resolution_preset_var = tk.StringVar(value=self.settings.resolution_preset)
        resolution_preset_menu = ttk.Combobox(resolution_preset_frame, textvariable=resolution_preset_var,
                                            values=["480p", "720p", "1080p", "1440p", "4K"], width=10, state="readonly")
        resolution_preset_menu.pack(side=tk.RIGHT)
        
        def on_preset_change(event):
            """Update width and height when preset changes"""
            preset = resolution_preset_var.get()
            self.settings.set_resolution_preset(preset)
            width_var.set(str(self.settings.resolution_width))
            height_var.set(str(self.settings.resolution_height))
        
        resolution_preset_menu.bind('<<ComboboxSelected>>', on_preset_change)

        # Custom resolution
        resolution_custom_frame = ttk.Frame(options_frame)
        resolution_custom_frame.pack(fill=tk.X, pady=2)
        ttk.Label(resolution_custom_frame, text="Custom Resolution:").pack(side=tk.LEFT)
        
        width_var = tk.StringVar(value=str(self.settings.resolution_width))
        height_var = tk.StringVar(value=str(self.settings.resolution_height))
        
        ttk.Label(resolution_custom_frame, text="W:").pack(side=tk.LEFT, padx=(5, 0))
        width_entry = ttk.Entry(resolution_custom_frame, textvariable=width_var, width=6)
        width_entry.pack(side=tk.LEFT, padx=(2, 5))
        
        ttk.Label(resolution_custom_frame, text="H:").pack(side=tk.LEFT)
        height_entry = ttk.Entry(resolution_custom_frame, textvariable=height_var, width=6)
        height_entry.pack(side=tk.LEFT, padx=(2, 0))

    # --- Image Capture Actions ---
    def capture_full_screen(self):
        """Capture the entire screen and resize to configured resolution"""
        try:
            # Add a small delay to let the UI update
            time.sleep(0.1)
            screenshot = pyautogui.screenshot()
            
            # Resize to configured resolution
            screenshot = screenshot.resize((self.settings.resolution_width, self.settings.resolution_height), Image.Resampling.LANCZOS)
            
            self.last_image = screenshot
            self._update_preview()
            self._auto_save_screenshot("full_screen")
            self.status_var.set("Captured and saved full screen")
        except Exception as e:
            print(f"Full screen capture failed: {e}")
            self.status_var.set("Full screen capture failed")

    def capture_selected_area(self):
        """Capture a selected area (simplified to center region for now)"""
        try:
            # For now, capture center region and resize to configured resolution
            screen_width, screen_height = pyautogui.size()
            capture_width = min(800, self.settings.resolution_width)
            capture_height = min(600, self.settings.resolution_height)
            left = (screen_width - capture_width) // 2
            top = (screen_height - capture_height) // 2
            
            time.sleep(0.1)
            screenshot = pyautogui.screenshot(region=(left, top, capture_width, capture_height))
            
            # Resize to configured resolution
            screenshot = screenshot.resize((self.settings.resolution_width, self.settings.resolution_height), Image.Resampling.LANCZOS)
            
            self.last_image = screenshot
            self._update_preview()
            self._auto_save_screenshot("selected_area")
            self.status_var.set("Captured and saved selected area (center region)")
        except Exception as e:
            print(f"Selected area capture failed: {e}")
            self.status_var.set("Selected area capture failed")

    def capture_active_window(self):
        """Capture the active window and resize to configured resolution"""
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
                
                # Resize to configured resolution
                screenshot = screenshot.resize((self.settings.resolution_width, self.settings.resolution_height), Image.Resampling.LANCZOS)
                
                self.last_image = screenshot
                self._update_preview()
                self._auto_save_screenshot("active_window")
                self.status_var.set("Captured and saved active window")
            else:
                # Fallback to full screen if no active window
                self.capture_full_screen()
        except Exception as e:
            print(f"Active window capture failed: {e}")
            self.status_var.set("Active window capture failed")

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
        """Start video recording by capturing screenshots at regular intervals"""
        if not self.is_recording:
            self.is_recording = True
            self.recording_start_time = time.time()
            self.current_video_start_time = time.time()
            self.frames_captured = 0
            self.captured_frames = []
            self.segments_created = 0  # Initialize segments counter
            
            # Update UI
            self.record_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.recording_status_var.set("Recording...")
            self.video_progress_var.set("Frames: 0 | Segments: 0")
            
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._recording_loop, daemon=True)
            self.recording_thread.start()
            
            # Start timer update
            self._update_timer()
            
            self.status_var.set(f"Recording started - capturing {self.frames_per_second} fps, saving {self.video_duration_seconds}-second segments")

    def stop_recording(self):
        """Stop video recording and save final video segment"""
        if self.is_recording:
            self.is_recording = False
            
            # Update UI
            self.record_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.recording_status_var.set("Not Recording")
            self.timer_var.set("00:00")
            
            # Save any remaining frames as final video
            if self.captured_frames:
                self._save_video_segment()
            
            self.status_var.set("Recording stopped")

    def _recording_loop(self):
        """Main recording loop that captures frames at regular intervals"""
        frame_interval = 1.0 / self.frames_per_second  # 1/24 second between frames (24 fps)
        
        while self.is_recording:
            try:
                # Capture screenshot
                screenshot = pyautogui.screenshot()
                
                # Resize to configured resolution
                screenshot = screenshot.resize((self.settings.resolution_width, self.settings.resolution_height), Image.Resampling.LANCZOS)
                
                timestamp = time.time()
                
                # Save frame to temporary file
                frame_path = self._save_frame(screenshot, timestamp)
                self.captured_frames.append(frame_path)
                self.frames_captured += 1
                
                # Update progress display
                self.video_progress_var.set(f"Frames: {self.frames_captured} | Segments: {self.segments_created}")
                
                # Check if we need to save a video segment (every X seconds = Y frames)
                frames_per_video = self.frames_per_second * self.video_duration_seconds  # 24 fps * seconds
                print(f"Debug: {len(self.captured_frames)} frames captured, need {frames_per_video} for segment")
                if len(self.captured_frames) >= frames_per_video:
                    print(f"Debug: Saving video segment {self.segments_created + 1} with {len(self.captured_frames)} frames")
                    self.status_var.set(f"Saving video segment {self.segments_created + 1}...")
                    self._save_video_segment()
                    self.segments_created += 1  # Increment segments counter
                    self.current_video_start_time = time.time()
                
                # Wait for next frame
                time.sleep(frame_interval)
                
            except Exception as e:
                print(f"Error in recording loop: {e}")
                self.status_var.set(f"Recording error: {str(e)}")
                time.sleep(1)

    def _save_frame(self, screenshot, timestamp):
        """Save a single frame to temporary storage"""
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.getcwd(), "temp_frames")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save frame with timestamp
        frame_filename = f"frame_{int(timestamp * 1000)}.png"
        frame_path = os.path.join(temp_dir, frame_filename)
        screenshot.save(frame_path)
        
        return frame_path

    def _save_video_segment(self):
        """Save captured frames as a video segment"""
        if not self.captured_frames:
            return
        
        try:
            # Create video filename with timestamp
            video_start_time = datetime.fromtimestamp(self.current_video_start_time)
            video_filename = f"screen_recording_{video_start_time.strftime('%Y%m%d_%H%M%S')}.mp4"
            
            # Ensure save directory exists
            save_dir = self.settings.save_dir
            os.makedirs(save_dir, exist_ok=True)
            video_path = os.path.join(save_dir, video_filename)
            
            # Use ffmpeg to create video from frames
            self._create_video_from_frames(video_path)
            
            # Update last video path
            self.last_video_path = video_path
            
            # Clear captured frames for next segment
            self._cleanup_frames()
            self.captured_frames = []
            
            self.status_var.set(f"Video segment saved: {video_filename}")
            
            # Update video progress
            self.video_progress_var.set(f"Frames: {self.frames_captured} | Segments: {self.segments_created}")
            
        except Exception as e:
            print(f"Error saving video segment: {e}")
            self.status_var.set("Error saving video segment")

    def _create_video_from_frames(self, output_path):
        """Create video from captured frames using OpenCV"""
        if not self.captured_frames:
            return
        
        try:
            print(f"Creating video from {len(self.captured_frames)} frames...")
            self.status_var.set(f"Creating video from {len(self.captured_frames)} frames...")
            
            # Get the first frame to determine video dimensions
            first_frame = cv2.imread(self.captured_frames[0])
            if first_frame is None:
                raise Exception("Could not read first frame")
            
            height, width, layers = first_frame.shape
            print(f"Video dimensions: {width}x{height}")
            
            # Try different codecs in order of preference
            codecs_to_try = [
                ('mp4v', '.mp4'),
                ('XVID', '.avi'),
                ('MJPG', '.avi'),
                ('H264', '.mp4')
            ]
            
            video_writer = None
            for codec, ext in codecs_to_try:
                try:
                    print(f"Trying codec: {codec}")
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    temp_path = output_path.replace('.mp4', ext)
                    video_writer = cv2.VideoWriter(temp_path, fourcc, self.frames_per_second, (width, height))
                    
                    if video_writer.isOpened():
                        print(f"Successfully opened video writer with codec: {codec}")
                        output_path = temp_path
                        break
                    else:
                        video_writer.release()
                        video_writer = None
                except Exception as e:
                    print(f"Failed with codec {codec}: {e}")
                    if video_writer:
                        video_writer.release()
                        video_writer = None
            
            if video_writer is None:
                raise Exception("Could not create video writer with any codec")
            
            # Add each frame to the video
            frames_written = 0
            for i, frame_path in enumerate(self.captured_frames):
                if os.path.exists(frame_path):
                    frame = cv2.imread(frame_path)
                    if frame is not None:
                        video_writer.write(frame)
                        frames_written += 1
                        
                        # Update progress every 10 frames
                        if i % 10 == 0:
                            progress = (i / len(self.captured_frames)) * 100
                            self.status_var.set(f"Creating video: {progress:.1f}% ({frames_written}/{len(self.captured_frames)} frames)")
                            self.root.update()
            
            # Release video writer
            video_writer.release()
            
            # Verify video was created
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                self.status_var.set(f"Video created: {os.path.basename(output_path)} ({file_size:.1f} MB)")
                print(f"Video created successfully: {output_path} ({file_size:.1f} MB)")
                
                # Update video progress
                self.video_progress_var.set(f"Frames: {self.frames_captured} | Segments: {self.segments_created}")
            else:
                raise Exception("Video file was not created or is empty")
                
        except Exception as e:
            print(f"Error creating video: {e}")
            self.status_var.set(f"Video creation failed: {str(e)}")
            # Fallback: save frames with instructions
            self._save_frames_with_instructions()
            raise

    def _cleanup_frames(self):
        """Clean up temporary frame files"""
        try:
            temp_dir = os.path.join(os.getcwd(), "temp_frames")
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    if file.startswith("frame_") and file.endswith(".png"):
                        os.remove(os.path.join(temp_dir, file))
        except Exception as e:
            print(f"Error cleaning up frames: {e}")

    def _update_timer(self):
        """Update the recording timer display"""
        if self.is_recording and self.recording_start_time:
            elapsed = time.time() - self.recording_start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.timer_var.set(f"{minutes:02d}:{seconds:02d}")
            
            # Schedule next update
            self.root.after(1000, self._update_timer)

    def open_last_video(self):
        """Open the last recorded video file"""
        if self.last_video_path and os.path.exists(self.last_video_path):
            try:
                # Use default system video player
                if sys.platform == "win32":
                    os.startfile(self.last_video_path)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", self.last_video_path])
                else:  # Linux
                    subprocess.run(["xdg-open", self.last_video_path])
                self.status_var.set(f"Opened video: {os.path.basename(self.last_video_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open video: {e}")
        else:
            messagebox.showinfo("Info", "No video has been recorded yet.")

    # --- Settings and Options ---
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (300 // 2)
        settings_window.geometry(f"400x300+{x}+{y}")
        
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Settings", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Save format
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill=tk.X, pady=5)
        ttk.Label(format_frame, text="Image Format:").pack(side=tk.LEFT)
        format_var = tk.StringVar(value=self.settings.save_format)
        format_menu = ttk.Combobox(format_frame, textvariable=format_var, 
                                 values=["PNG", "JPG"], width=10, state="readonly")
        format_menu.pack(side=tk.RIGHT)
        
        # Video format
        video_format_frame = ttk.Frame(main_frame)
        video_format_frame.pack(fill=tk.X, pady=5)
        ttk.Label(video_format_frame, text="Video Format:").pack(side=tk.LEFT)
        video_format_var = tk.StringVar(value=self.settings.video_format)
        video_format_menu = ttk.Combobox(video_format_frame, textvariable=video_format_var,
                                       values=["MP4", "AVI", "MOV"], width=10, state="readonly")
        video_format_menu.pack(side=tk.RIGHT)
        
        # Video duration
        duration_frame = ttk.Frame(main_frame)
        duration_frame.pack(fill=tk.X, pady=5)
        ttk.Label(duration_frame, text="Video Duration (seconds):").pack(side=tk.LEFT)
        duration_var = tk.StringVar(value=str(self.settings.video_duration_seconds))
        duration_entry = ttk.Entry(duration_frame, textvariable=duration_var, width=10)
        duration_entry.pack(side=tk.RIGHT)
        
        # Resolution preset
        resolution_preset_frame = ttk.Frame(main_frame)
        resolution_preset_frame.pack(fill=tk.X, pady=5)
        ttk.Label(resolution_preset_frame, text="Resolution Preset:").pack(side=tk.LEFT)
        resolution_preset_var = tk.StringVar(value=self.settings.resolution_preset)
        resolution_preset_menu = ttk.Combobox(resolution_preset_frame, textvariable=resolution_preset_var,
                                            values=["480p", "720p", "1080p", "1440p", "4K"], width=10, state="readonly")
        resolution_preset_menu.pack(side=tk.RIGHT)
        
        def on_preset_change(event):
            """Update width and height when preset changes"""
            preset = resolution_preset_var.get()
            self.settings.set_resolution_preset(preset)
            width_var.set(str(self.settings.resolution_width))
            height_var.set(str(self.settings.resolution_height))
        
        resolution_preset_menu.bind('<<ComboboxSelected>>', on_preset_change)
        
        # Custom resolution
        resolution_custom_frame = ttk.Frame(main_frame)
        resolution_custom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(resolution_custom_frame, text="Custom Resolution:").pack(side=tk.LEFT)
        
        width_var = tk.StringVar(value=str(self.settings.resolution_width))
        height_var = tk.StringVar(value=str(self.settings.resolution_height))
        
        ttk.Label(resolution_custom_frame, text="W:").pack(side=tk.LEFT, padx=(5, 0))
        width_entry = ttk.Entry(resolution_custom_frame, textvariable=width_var, width=6)
        width_entry.pack(side=tk.LEFT, padx=(2, 5))
        
        ttk.Label(resolution_custom_frame, text="H:").pack(side=tk.LEFT)
        height_entry = ttk.Entry(resolution_custom_frame, textvariable=height_var, width=6)
        height_entry.pack(side=tk.LEFT, padx=(2, 0))
        
        # Save location
        save_frame = ttk.Frame(main_frame)
        save_frame.pack(fill=tk.X, pady=5)
        ttk.Label(save_frame, text="Save Location:").pack(side=tk.LEFT)
        save_dir_var = tk.StringVar(value=self.settings.save_dir)
        save_dir_entry = ttk.Entry(save_frame, textvariable=save_dir_var, width=25)
        save_dir_entry.pack(side=tk.LEFT, padx=(5, 5))
        
        def browse_save_dir():
            directory = filedialog.askdirectory(initialdir=self.settings.save_dir)
            if directory:
                save_dir_var.set(directory)
        
        ttk.Button(save_frame, text="Browse", command=browse_save_dir).pack(side=tk.RIGHT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def save_settings():
            try:
                # Validate duration
                duration = int(duration_var.get())
                if duration < 1 or duration > 3600:
                    messagebox.showerror("Error", "Video duration must be between 1 and 3600 seconds (1 hour)")
                    return
                
                # Validate resolution
                width = int(width_var.get())
                height = int(height_var.get())
                if width < 320 or width > 7680 or height < 240 or height > 4320:
                    messagebox.showerror("Error", "Resolution must be between 320x240 and 7680x4320")
                    return
                
                # Handle preset changes
                preset = resolution_preset_var.get()
                if preset != self.settings.resolution_preset:
                    self.settings.set_resolution_preset(preset)
                    width_var.set(str(self.settings.resolution_width))
                    height_var.set(str(self.settings.resolution_height))
                
                # Update settings
                self.settings.save_format = format_var.get()
                self.settings.video_format = video_format_var.get()
                self.settings.save_dir = save_dir_var.get()
                self.settings.video_duration_seconds = duration
                self.settings.resolution_width = width
                self.settings.resolution_height = height
                self.settings.resolution_preset = preset
                
                # Update app variables
                self.video_duration_seconds = duration
                self.format_var.set(format_var.get())
                self.video_format_var.set(video_format_var.get())
                self.save_dir_var.set(save_dir_var.get())
                
                # Save to file
                self.settings.save_settings()
                
                # Ensure save directory exists
                os.makedirs(self.settings.save_dir, exist_ok=True)
                
                messagebox.showinfo("Success", "Settings saved successfully!")
                settings_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for duration and resolution")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {e}")
        
        def cancel():
            settings_window.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.RIGHT)

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

    def _save_frames_with_instructions(self):
        """Fallback method to save frames with instructions when video creation fails"""
        try:
            # Create a frames directory for this video segment
            video_start_time = datetime.fromtimestamp(self.current_video_start_time)
            frames_dir_name = f"frames_{video_start_time.strftime('%Y%m%d_%H%M%S')}"
            frames_dir = os.path.join(self.settings.save_dir, frames_dir_name)
            os.makedirs(frames_dir, exist_ok=True)
            
            # Copy frames to the frames directory with sequential numbering
            for i, frame_path in enumerate(self.captured_frames):
                if os.path.exists(frame_path):
                    new_frame_name = f"frame_{i:04d}.png"
                    new_frame_path = os.path.join(frames_dir, new_frame_name)
                    import shutil
                    shutil.copy2(frame_path, new_frame_path)
            
            # Create a README file with instructions
            readme_path = os.path.join(frames_dir, "README.txt")
            with open(readme_path, 'w') as f:
                f.write("Video Recording Frames\n")
                f.write("=====================\n\n")
                f.write(f"Recording started: {video_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total frames: {len(self.captured_frames)}\n")
                f.write(f"Frame rate: {self.frames_per_second} fps\n")
                f.write(f"Duration: {len(self.captured_frames) / self.frames_per_second:.1f} seconds\n\n")
                f.write("To create a video from these frames:\n")
                f.write("1. Install FFmpeg from https://ffmpeg.org/download.html\n")
                f.write("2. Open command prompt in this directory\n")
                f.write("3. Run: ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4\n\n")
                f.write("Or use any video editing software that supports image sequences.\n")
            
            # Update status
            self.status_var.set(f"Frames saved to: {frames_dir_name} (video creation failed)")
            
        except Exception as e:
            print(f"Error saving frames with instructions: {e}")
            self.status_var.set("Error saving video frames")

# --- Main Entrypoint ---
def main():
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
