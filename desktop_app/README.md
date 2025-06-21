# Desktop Application

A simple desktop application built with Python and tkinter that opens a window in Windows and can create a desktop shortcut.

## Features

- Modern GUI with tkinter
- Real-time clock display
- System information display
- Message dialogs
- Desktop shortcut creation
- Status bar with feedback
- Scrollable text area

## Requirements

- Python 3.6 or higher
- Windows operating system
- Required packages (installed automatically):
  - `pywin32` - For Windows COM automation
  - `winshell` - For accessing Windows shell folders

## Installation

### Option 1: Automatic Setup (Recommended)

1. Open Command Prompt or PowerShell in this directory
2. Run the setup script:
   ```bash
   python setup.py
   ```
3. The script will automatically:
   - Install required packages
   - Create a desktop shortcut

### Option 2: Manual Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python desktop_app.py
   ```

## Usage

### Running the Application

You can run the application in several ways:

1. **Desktop Shortcut**: Double-click "My Desktop App" on your desktop (after running setup)
2. **Command Line**: Run `python desktop_app.py`
3. **Batch File**: Double-click `run_app.bat`

### Application Features

- **Show Message**: Displays a simple message dialog
- **Get System Info**: Shows system information in the text area
- **Create Desktop Shortcut**: Creates a shortcut on your desktop (requires dependencies)

## File Structure

```
codebase/
├── desktop_app.py      # Main application file
├── requirements.txt    # Python dependencies
├── setup.py           # Setup script
├── run_app.bat        # Batch file to run the app
└── README.md          # This file
```

## Troubleshooting

### Common Issues

1. **Import Error for pywin32 or winshell**:
   - Run `pip install pywin32 winshell`
   - Or run the setup script: `python setup.py`

2. **Application won't start**:
   - Make sure Python is installed and in your PATH
   - Try running `python --version` to verify Python installation

3. **Shortcut creation fails**:
   - Make sure you're running on Windows
   - Run the application as administrator if needed
   - Check that pywin32 and winshell are installed

### Manual Shortcut Creation

If the automatic shortcut creation doesn't work, you can create a shortcut manually:

1. Right-click on your desktop
2. Select "New" → "Shortcut"
3. Enter: `python "C:\path\to\your\desktop_app.py"`
4. Name it "My Desktop App"

## Customization

You can customize the application by modifying `desktop_app.py`:

- Change the window title in the `__init__` method
- Modify the window size by changing the `geometry` call
- Add new buttons and functionality
- Change the theme by modifying the `style.theme_use()` call

## License

This project is open source and available under the MIT License. 