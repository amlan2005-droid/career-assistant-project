import subprocess
import sys

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    # Bcrypt 4.1.0+ breaks passlib 1.7.4
    # Downgrade to 4.0.1
    try:
        install_package("bcrypt==4.0.1")
        print("Successfully installed bcrypt==4.0.1")
    except Exception as e:
        print(f"Failed to install bcrypt: {e}")
