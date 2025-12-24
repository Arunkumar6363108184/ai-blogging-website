#!/usr/bin/env python3
"""
Proper startup script for AUTO-blogger
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    venv_python = script_dir / "auto_blogger_venv_2344a2a5" / "bin" / "python"
    gui_script = script_dir / "gui_blogger.py"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("Please run the installation script first.")
        return
    
    if not gui_script.exists():
        print("❌ GUI script not found!")
        return
    
    print("🚀 Starting AUTO-blogger...")
    
    # Change to the project directory
    os.chdir(script_dir)
    
    # Start the GUI with the virtual environment
    subprocess.run([str(venv_python), str(gui_script)])

if __name__ == "__main__":
    main()
