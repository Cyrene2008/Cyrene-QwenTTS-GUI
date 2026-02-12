import os
import sys
import subprocess
import shutil
import stat
import time

def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"Failed to remove {path}: {e}")

def run_command(command):
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        sys.exit(1)

def clean_build():
    print("Cleaning build/ and dist/ folders...")
    if os.path.exists('build'):
        shutil.rmtree('build', onerror=remove_readonly)
    
    if os.path.exists('dist'):
        try:
            for item in os.listdir('dist'):
                item_path = os.path.join('dist', item)
                if item == 'QwenTTS-Cyrene-GUI-ENV':
                    print("Skipping QwenTTS-Cyrene-GUI-ENV to save time...")
                    continue
                
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path, onerror=remove_readonly)
                    
        except PermissionError:
            print("Permission denied when cleaning dist/. A process might be using it.")
            print("Attempting to kill lingering python processes (server.py)...")
            try:
                subprocess.run("taskkill /F /IM python.exe", shell=True)
                time.sleep(2) 
                
                for item in os.listdir('dist'):
                    item_path = os.path.join('dist', item)
                    if item == 'QwenTTS-Cyrene-GUI-ENV':
                        continue
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path, onerror=remove_readonly)
                        
            except Exception as e:
                print(f"Failed to force clean dist/: {e}")
                print("Please manually close any running instances of the application or python.")
                sys.exit(1)
    
    # Remove spec file if exists
    if os.path.exists('CyreneUI.spec'):
        os.remove('CyreneUI.spec')

def copy_app_source():
    """Copy app source code to dist/app for external python access"""
    print("Copying app source code to dist/app...")
    dist_app = os.path.join('dist', 'app')
    if os.path.exists(dist_app):
        shutil.rmtree(dist_app, onerror=remove_readonly)
    
    # Ignore __pycache__ and other non-source files
    shutil.copytree('app', dist_app, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
    print("App source copied.")

def build_onefile():
    print("========================================")
    print("               Building EXE             ")
    print("========================================")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '-n', 'QwenTTS-Cyrene-GUI',
        '-F',
        '-w',
        '-i', 'app/resource/images/Cyrene.ico',
        '--add-data', 'app;app',
        '--hidden-import', 'pkg_resources.extern',
        '--hidden-import', 'six',
        '--hidden-import', 'appdirs',
        '--hidden-import', 'packaging',
        '--hidden-import', 'packaging.version',
        '--hidden-import', 'packaging.specifiers',
        '--hidden-import', 'packaging.requirements',
        '--collect-all', 'psutil',
        '--copy-metadata', 'packaging',
        '--copy-metadata', 'setuptools',
        '--runtime-hook', 'rthook_fix.py',
        '--exclude-module', 'torch',
        '--exclude-module', 'torchaudio',
        '--exclude-module', 'torchvision',
        '--exclude-module', 'qwen_tts',
        '--exclude-module', 'modelscope',
        '--exclude-module', 'transformers',
        '--exclude-module', 'accelerate',
        '--exclude-module', 'gradio',
        '--exclude-module', 'numpy',
        '--exclude-module', 'pandas',
        '--exclude-module', 'matplotlib',
        '--clean',
        '-y',
        'main.py'
    ]
    
    run_command(cmd)
    
    if os.path.exists('requirements.txt'):
        shutil.copy('requirements.txt', 'dist/requirements.txt')
        print("Copied requirements.txt to dist/")
    else:
        print("Warning: requirements.txt not found in root, skipping copy.")
        
    print("\nBuild Complete! Executable is in dist/CyreneUI.exe")

def check_dependencies():
    print("Checking dependencies...")

    if sys.version_info >= (3, 13):
        print(f"WARNING: Current Python version {sys.version} is 3.13+, which may be unstable with PyInstaller.")
        print("Recommended version: Python 3.10 - 3.12")
        print("If packaging fails, try running with: py -3.11 package.py")
        time.sleep(2)

    required = ['pyinstaller', 'psutil', 'pywin32-ctypes']
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing missing dependency: {package}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception as e:
                print(f"Failed to install {package}: {e}")
                print("Please install it manually or switch to a stable Python environment (e.g. 3.11).")
                if package == 'pywin32-ctypes':
                    print("Critical dependency missing. Exiting.")
                    sys.exit(1)

if __name__ == '__main__':
    check_dependencies()
    args = sys.argv[1:]
    
    if args and args[0] == 'clean':
        clean_build()
    elif args and args[0] == 'check-deps':
        print("Dependencies OK.")
    else:
        clean_build()
        build_onefile()
