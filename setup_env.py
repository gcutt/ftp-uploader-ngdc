
import os
import subprocess
import sys

VENV_DIR = ".venv"

def create_venv():
    if not os.path.exists(VENV_DIR):
        print("🔧 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("✅ Virtual environment already exists.")

def install_requirements():
    pip_path = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "pip")
    if os.path.exists("requirements.txt"):
        print("📦 Installing dependencies...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    else:
        print("⚠️ No requirements.txt found. Skipping install.")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    print("🚀 Environment setup complete.")