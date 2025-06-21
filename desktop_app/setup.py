#!/usr/bin/env python3
"""
Setup script for the Desktop Application
Installs required dependencies and creates a desktop shortcut
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False

def create_shortcut():
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
        shortcut.Arguments = f'"{os.path.abspath("desktop_app.py")}"'
        shortcut.WorkingDirectory = os.path.dirname(os.path.abspath("desktop_app.py"))
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print(f"✓ Desktop shortcut created: {shortcut_path}")
        return True
        
    except ImportError:
        print("✗ Required packages not installed. Please run setup again.")
        return False
    except Exception as e:
        print(f"✗ Error creating shortcut: {e}")
        return False

def main():
    print("=== Desktop Application Setup ===")
    print()
    
    # Install requirements
    if install_requirements():
        # Create shortcut
        if create_shortcut():
            print()
            print("=== Setup Complete! ===")
            print("You can now:")
            print("1. Run the application by double-clicking 'My Desktop App' on your desktop")
            print("2. Run 'python desktop_app.py' from the command line")
            print("3. Double-click 'run_app.bat' to run the application")
        else:
            print("Setup completed with warnings. You can still run the application manually.")
    else:
        print("Setup failed. Please check your Python installation and try again.")

if __name__ == "__main__":
    main() 