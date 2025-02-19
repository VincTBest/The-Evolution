import os
import sys
import subprocess

# List of required modules
REQUIRED_MODULES = ["pygame"]

def install_packages():
    """Checks and installs missing packages."""
    for module in REQUIRED_MODULES:
        try:
            __import__(module)  # Try importing the module
        except ImportError:
            print(f"{module} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
