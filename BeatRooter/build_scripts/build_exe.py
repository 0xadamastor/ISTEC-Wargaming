import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_guaranteed():
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("Building BeatRooter...")
    
    try:
        import PyQt6
        pyqt6_dir = Path(PyQt6.__file__).parent
        print(f"PyQt6 directory: {pyqt6_dir}")
    except ImportError as e:
        print(f"Cannot find PyQt6: {e}")
        return

    cmd = [
    sys.executable, "-m", "PyInstaller",
    '--name=BeatRooter',
    '--windowed',
    '--onefile',
    '--add-data=core;core',
    '--add-data=models;models',
    '--add-data=ui;ui',
    '--collect-all=PyQt6',
    '--clean',
    'main.py'
]
    
    try:
        print("Running PyInstaller...")
        result = subprocess.run(cmd, check=True)
        print("Build completed!")
        
    except Exception as e:
        print(f"Build failed: {e}")
        build_alternative()

def build_alternative():
    """Alternative build method"""
    print("Trying alternative build method...")
    
    cmd = [
        'pyinstaller',
        '--name=BeatRooter',
        '--windowed',
        '--onefile',
        '--paths=C:\\Users\\Samur\\AppData\\Roaming\\Python\\Python311\\site-packages',
        '--add-data=core;core',
        '--add-data=models;models', 
        '--add-data=ui;ui',
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Alternative build completed!")
    except Exception as e:
        print(f"Alternative build also failed: {e}")

if __name__ == "__main__":
    build_guaranteed()