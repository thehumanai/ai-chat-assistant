import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from datetime import datetime

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Desktop Application")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Set window icon (optional)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # No icon file found
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Welcome to My Desktop App", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Current time display
        self.time_label = ttk.Label(main_frame, text="", font=("Arial", 12))
        self.time_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Action buttons
        ttk.Button(buttons_frame, text="Show Message", 
                  command=self.show_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Get System Info", 
                  command=self.show_system_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Create Desktop Shortcut", 
                  command=self.create_shortcut).pack(side=tk.LEFT, padx=5)
        
        # Text area
        self.text_area = tk.Text(main_frame, height=10, width=50, wrap=tk.WORD)
        self.text_area.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Start updating time
        self.update_time()
        
        # Welcome message
        self.text_area.insert(tk.END, "Welcome to My Desktop Application!\n\n")
        self.text_area.insert(tk.END, "This is a simple desktop application created with Python and tkinter.\n")
        self.text_area.insert(tk.END, "You can use the buttons above to interact with the application.\n\n")
        self.text_area.see(tk.END)
    
    def update_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)  # Update every second
    
    def show_message(self):
        """Show a simple message box"""
        messagebox.showinfo("Message", "Hello! This is a message from your desktop application.")
        self.text_area.insert(tk.END, "Message dialog was shown.\n")
        self.text_area.see(tk.END)
        self.status_var.set("Message shown")
    
    def show_system_info(self):
        """Display system information"""
        import platform
        
        info = f"System Information:\n"
        info += f"OS: {platform.system()} {platform.release()}\n"
        info += f"Architecture: {platform.machine()}\n"
        info += f"Python Version: {sys.version.split()[0]}\n"
        info += f"Current Directory: {os.getcwd()}\n"
        
        self.text_area.insert(tk.END, f"\n{info}\n")
        self.text_area.see(tk.END)
        self.status_var.set("System info displayed")
    
    def create_shortcut(self):
        """Create a desktop shortcut"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            # Get desktop path
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "My Desktop App.lnk")
            
            # Create shortcut
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{os.path.abspath(__file__)}"'
            shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(__file__))
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            self.text_area.insert(tk.END, f"Desktop shortcut created: {shortcut_path}\n")
            self.text_area.see(tk.END)
            self.status_var.set("Shortcut created successfully")
            messagebox.showinfo("Success", "Desktop shortcut created successfully!")
            
        except ImportError:
            error_msg = "Required packages not installed. Please install:\npip install pywin32 winshell"
            self.text_area.insert(tk.END, f"Error: {error_msg}\n")
            self.text_area.see(tk.END)
            self.status_var.set("Error: Missing dependencies")
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = f"Error creating shortcut: {str(e)}"
            self.text_area.insert(tk.END, f"Error: {error_msg}\n")
            self.text_area.see(tk.END)
            self.status_var.set("Error creating shortcut")
            messagebox.showerror("Error", error_msg)

def main():
    root = tk.Tk()
    app = DesktopApp(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 