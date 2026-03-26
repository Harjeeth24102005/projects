import subprocess
import sys

def install_requirements():
    """Install required packages"""
    requirements = [
        "opencv-python==4.8.1.78",
        "face-recognition==1.3.0", 
        "numpy==1.24.3",
        "pillow==10.0.0"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
    
    print("\nAll dependencies installed successfully!")

if __name__ == "__main__":
    install_requirements()