' Python GUI App Launcher (Silent)
' This script runs the Python GUI app without showing a console window

' Get the directory where this script is located
Set objShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strPath

' Run the Python GUI application
objShell.Run "python run.py", 0, False

' Clean up
Set objShell = Nothing 