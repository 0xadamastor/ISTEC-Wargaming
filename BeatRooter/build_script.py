import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_build(cmd):
    print("Running PyInstaller...")
    try:
        subprocess.run(cmd, check=True)
        print("Build completed!")
    except Exception as e:
        print(f"Build failed: {e}")

def build_windows(project_root):
    print("=== Building for WINDOWS (.exe) ===")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=BeatRooter",
        "--windowed",
        "--onefile",
        "--add-data=core;core",
        "--add-data=models;models",
        "--add-data=ui;ui",
        "--collect-all=PyQt6",
        "--clean",
        "main.py"
    ]

    run_build(cmd)

def build_linux(project_root):
    print("=== Building for LINUX (sem .exe) ===")

    cmd = [
        "pyinstaller",
        "--name=BeatRooter",
        "--windowed",
        "--onefile",
        "--add-data=core:core",
        "--add-data=models:models",
        "--add-data=ui:ui",
        "--collect-all=PyQt6",
        "--clean",
        "main.py"
    ]

    run_build(cmd)

def main():
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    system = platform.system().lower()

    print(f"Detected OS: {system}")

    try:
        import PyQt6
        print("PyQt6 found.")
    except ImportError:
        print("PyQt6 NOT FOUND in this environment!")
        return
    
    if "windows" in system:
        build_windows(project_root)
    elif "linux" in system:
        build_linux(project_root)
    else:
        print("Unsupported OS for auto-build.")

if __name__ == "__main__":
    main()
