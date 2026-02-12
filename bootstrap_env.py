import os
import sys
import urllib.request
import tarfile
import shutil
import subprocess

def main():
    print("Bootstrapping Python Environment...")
    target_dir = os.path.join(os.getcwd(), "QwenTTS-Cyrene-GUI-ENV")
    
    # Clean target dir if exists
    if os.path.exists(target_dir):
        print(f"Cleaning existing directory: {target_dir}")
        shutil.rmtree(target_dir, ignore_errors=True)
    
    os.makedirs(target_dir, exist_ok=True)
    
    # URL for Python 3.10 Standalone
    url = "https://gh-proxy.org/https://github.com/indygreg/python-build-standalone/releases/download/20240224/cpython-3.10.13+20240224-x86_64-pc-windows-msvc-shared-install_only.tar.gz"
    temp_tar = os.path.join(os.getcwd(), "python_runtime.tar.gz")
    
    print(f"Downloading Python from {url}...")
    try:
        urllib.request.urlretrieve(url, temp_tar)
    except Exception as e:
        print(f"Download failed: {e}")
        # Try backup URL
        url = "https://github.com/indygreg/python-build-standalone/releases/download/20240224/cpython-3.10.13+20240224-x86_64-pc-windows-msvc-shared-install_only.tar.gz"
        print(f"Trying backup URL: {url}...")
        urllib.request.urlretrieve(url, temp_tar)
        
    print("Extracting Python...")
    with tarfile.open(temp_tar, "r:gz") as tar:
        tar.extractall(path=target_dir)
        
    os.remove(temp_tar)
    
    # Move files from 'python' subdir if exists
    extracted_root = os.path.join(target_dir, "python")
    if os.path.exists(extracted_root):
        print("Moving files from 'python' subdirectory...")
        for item in os.listdir(extracted_root):
            shutil.move(os.path.join(extracted_root, item), target_dir)
        os.rmdir(extracted_root)
        
    python_exe = os.path.join(target_dir, "python.exe")
    if not os.path.exists(python_exe):
        # Maybe in Scripts?
        python_exe = os.path.join(target_dir, "Scripts", "python.exe")
        
    if not os.path.exists(python_exe):
        print("Error: python.exe not found after extraction.")
        sys.exit(1)
        
    print(f"Python installed at: {python_exe}")
    
    # Install pip
    print("Installing pip...")
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = os.path.join(target_dir, "get-pip.py")
    try:
        urllib.request.urlretrieve(get_pip_url, get_pip_path)
        subprocess.check_call([python_exe, get_pip_path])
    except Exception as e:
        print(f"Failed to install pip: {e}")
        sys.exit(1)
        
    print("Environment setup complete.")

if __name__ == "__main__":
    main()
