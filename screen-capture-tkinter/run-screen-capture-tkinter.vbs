' Screen Capture App Launcher (Silent)
' This script runs the Python Screen Capture app without showing a console window

' Get the directory where this script is located
Set objShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strPath

' Run the Python Screen Capture application
objShell.Run "python run.py", 0, False

' Clean up
Set objShell = Nothing 