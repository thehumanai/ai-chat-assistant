import tkinter as tk
from tkinter import ttk, messagebox
import math

class SimpleGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Python GUI App")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Welcome to Python GUI App!", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Calculator section
        self.create_calculator_section(main_frame)
        
        # Text input/output section
        self.create_text_section(main_frame)
        
        # Buttons section
        self.create_buttons_section(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_calculator_section(self, parent):
        # Calculator frame
        calc_frame = ttk.LabelFrame(parent, text="Simple Calculator", padding="10")
        calc_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        calc_frame.columnconfigure(1, weight=1)
        
        # Calculator display
        self.calc_var = tk.StringVar()
        self.calc_var.set("0")
        calc_display = ttk.Entry(calc_frame, textvariable=self.calc_var, 
                                font=('Arial', 12), justify='right', state='readonly')
        calc_display.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Calculator buttons
        calc_buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('√', 5, 1), ('^2', 5, 2), ('Clear', 5, 3)
        ]
        
        for (text, row, col) in calc_buttons:
            btn = ttk.Button(calc_frame, text=text, 
                           command=lambda t=text: self.calc_button_click(t))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky=(tk.W, tk.E))
        
        # Store calculator state
        self.calc_expression = ""
        self.calc_result = 0
    
    def create_text_section(self, parent):
        # Text input/output frame
        text_frame = ttk.LabelFrame(parent, text="Text Input/Output", padding="10")
        text_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Input label and entry
        ttk.Label(text_frame, text="Enter text:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.text_input = ttk.Entry(text_frame, font=('Arial', 10))
        self.text_input.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.text_input.bind('<Return>', self.process_text)
        
        # Output text area
        ttk.Label(text_frame, text="Output:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.text_output = tk.Text(text_frame, height=6, width=50, font=('Arial', 10))
        self.text_output.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Text processing buttons
        text_btn_frame = ttk.Frame(text_frame)
        text_btn_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(text_btn_frame, text="Process Text", 
                  command=self.process_text).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(text_btn_frame, text="Clear Output", 
                  command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(text_btn_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
    
    def create_buttons_section(self, parent):
        # Buttons frame
        btn_frame = ttk.LabelFrame(parent, text="Actions", padding="10")
        btn_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Action buttons
        ttk.Button(btn_frame, text="Show Info", 
                  command=self.show_info).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Change Theme", 
                  command=self.change_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Get Current Time", 
                  command=self.get_time).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.RIGHT, padx=(5, 0))
    
    def calc_button_click(self, button):
        if button == 'C':
            self.calc_expression = ""
            self.calc_var.set("0")
        elif button == 'Clear':
            self.calc_expression = ""
            self.calc_var.set("0")
        elif button == '=':
            try:
                result = eval(self.calc_expression)
                self.calc_var.set(str(result))
                self.calc_expression = str(result)
                self.status_var.set(f"Calculated: {result}")
            except:
                self.calc_var.set("Error")
                self.calc_expression = ""
        elif button == '√':
            try:
                result = math.sqrt(float(self.calc_var.get()))
                self.calc_var.set(str(result))
                self.calc_expression = str(result)
                self.status_var.set(f"Square root: {result}")
            except:
                self.calc_var.set("Error")
        elif button == '^2':
            try:
                result = float(self.calc_var.get()) ** 2
                self.calc_var.set(str(result))
                self.calc_expression = str(result)
                self.status_var.set(f"Squared: {result}")
            except:
                self.calc_var.set("Error")
        else:
            if self.calc_var.get() == "0" and button not in ['+', '-', '*', '/', '.']:
                self.calc_expression = button
                self.calc_var.set(button)
            else:
                self.calc_expression += button
                self.calc_var.set(self.calc_expression)
    
    def process_text(self, event=None):
        text = self.text_input.get()
        if text:
            # Process the text (convert to uppercase and add some formatting)
            processed = f"Original: {text}\n"
            processed += f"Uppercase: {text.upper()}\n"
            processed += f"Length: {len(text)} characters\n"
            processed += f"Words: {len(text.split())}\n"
            processed += "-" * 30 + "\n"
            
            self.text_output.insert(tk.END, processed)
            self.text_input.delete(0, tk.END)
            self.status_var.set(f"Processed text: {text}")
    
    def clear_output(self):
        self.text_output.delete(1.0, tk.END)
        self.status_var.set("Output cleared")
    
    def copy_to_clipboard(self):
        try:
            text = self.text_output.get(1.0, tk.END).strip()
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.status_var.set("Text copied to clipboard")
            else:
                self.status_var.set("No text to copy")
        except:
            self.status_var.set("Failed to copy to clipboard")
    
    def show_info(self):
        info_text = """Simple Python GUI App
        
Features:
• Calculator with basic operations
• Text processing and display
• Modern tkinter interface
• Status bar updates
• Copy to clipboard functionality

Built with Python and tkinter"""
        messagebox.showinfo("App Information", info_text)
        self.status_var.set("Info dialog shown")
    
    def change_theme(self):
        themes = ['clam', 'alt', 'default', 'classic']
        current_theme = ttk.Style().theme_use()
        try:
            next_theme = themes[(themes.index(current_theme) + 1) % len(themes)]
            ttk.Style().theme_use(next_theme)
            self.status_var.set(f"Theme changed to: {next_theme}")
        except:
            self.status_var.set("Failed to change theme")
    
    def get_time(self):
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_output.insert(tk.END, f"Current time: {current_time}\n")
        self.status_var.set(f"Time retrieved: {current_time}")

def main():
    root = tk.Tk()
    app = SimpleGUIApp(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
