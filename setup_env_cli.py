import sys
import os
import time
from pathlib import Path
from PySide6.QtCore import QObject

# Mock signals
class MockSignal:
    def connect(self, func):
        self.func = func
    def emit(self, *args):
        if hasattr(self, 'func'):
            self.func(*args)

# Add app to path
sys.path.append(os.getcwd())

from app.core.env_manager import EnvManager

def on_progress(msg, val):
    print(f"[PROGRESS {val}%] {msg}")

def on_finished(success, msg):
    print(f"[FINISHED] Success: {success}, Msg: {msg}")
    if not success:
        sys.exit(1)

def main():
    print("Starting Environment Setup CLI...")
    manager = EnvManager()
    
    # Mock signals
    manager.progress = MockSignal()
    manager.finished = MockSignal()
    
    manager.progress.connect(on_progress)
    manager.finished.connect(on_finished)
    
    # Force check first
    print("Checking existing environment...")
    valid, msg = manager.check_env()
    print(f"Check result: {valid}, {msg}")
    
    # If valid, we might still want to ensure dependencies are installed?
    # But check_env checks for qwen_tts and torch.
    
    if not valid:
        print("Environment invalid or missing. Starting installation...")
        # Use Aliyun mirror as default for this CLI
        manager.set_install_mode("https://mirrors.aliyun.com/pypi/simple/")
        manager.cpu_mode = False # Default to GPU
        
        # Run installation synchronously
        manager.run()
    else:
        print("Environment is already ready.")

if __name__ == "__main__":
    main()
