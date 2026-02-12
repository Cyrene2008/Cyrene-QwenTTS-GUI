import os
import sys
import subprocess
import venv
import urllib.request
import zipfile
import shutil
from pathlib import Path
from PySide6.QtCore import QThread, Signal
from .config import ROOT_PATH

class EnvManager(QThread):
    progress = Signal(str, int)
    finished = Signal(bool, str)
    
    def __init__(self, target_dir="QwenTTS-Cyrene-GUI-ENV"):
        super().__init__()
        self.target_dir = ROOT_PATH / target_dir
        self.python_exe = self.target_dir / "python.exe" # Standalone puts python.exe in root
        if os.name != 'nt':
             self.python_exe = self.target_dir / "bin" / "python"
        
        # Check if it is a venv (Scripts/python.exe) or standalone (python.exe)
        if not self.python_exe.exists():
             self.python_exe = self.target_dir / "Scripts" / "python.exe"
             
        # Check for system python override
        self.use_system_python = False
        # marker_file = ROOT_PATH / "use_system_python.marker"
        # if marker_file.exists():
        #     self.use_system_python = True
        #     self.python_exe = Path(sys.executable)

        self.mode = "check" # check, install
        self.mirror = "https://pypi.org/simple"
        self.skip_cuda_check = False
        self.cpu_mode = False
        
        # Python Standalone URL (Windows x64)
        self.python_urls = [
            "https://gh-proxy.org/https://github.com/indygreg/python-build-standalone/releases/download/20240224/cpython-3.10.13+20240224-x86_64-pc-windows-msvc-shared-install_only.tar.gz",
            "https://github.com/indygreg/python-build-standalone/releases/download/20240224/cpython-3.10.13+20240224-x86_64-pc-windows-msvc-shared-install_only.tar.gz"
        ]
        
    def set_install_mode(self, mirror_url):
        self.mode = "install"
        self.mirror = mirror_url
        
    def check_env(self):
        # if self.use_system_python:
        #     # Use current system python
        #     self.python_exe = Path(sys.executable)
        # else:
        
        # Determine python path again
        if (self.target_dir / "python.exe").exists():
            self.python_exe = self.target_dir / "python.exe"
        elif (self.target_dir / "Scripts" / "python.exe").exists():
            self.python_exe = self.target_dir / "Scripts" / "python.exe"
        else:
            return False, "环境未找到 (Environment not found)"
        
        if not self.python_exe.is_file():
            return False, "环境未找到 (Environment not found)"
        
        # Optimization: Check for verified marker to skip heavy pip checks
        verified_marker = self.target_dir / "env_verified.marker"
        if verified_marker.exists() and self.mode == "check":
            return True, "环境已验证 (Environment Verified)"

        # Check for key packages
        try:
            # Hide console window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Check for key packages using pip show which is faster than import
            # Checking qwen_tts and torch
            subprocess.check_call(
                [str(self.python_exe), "-m", "pip", "show", "qwen_tts", "torch"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo
            )
            
            # Verify torch import and version
            try:
                result = subprocess.check_output(
                    [str(self.python_exe), "-c", "import torch; print(torch.__version__)"],
                    startupinfo=startupinfo,
                    text=True,
                    stderr=subprocess.STDOUT
                )
                if "+cpu" in result:
                     if not self.skip_cuda_check:
                         # Return True even if CPU detected, but with a warning in msg?
                         # Or just return False to force wizard?
                         # User says: "After selecting CPU, reboot still prompts no Torch GPU, repeating loop"
                         # This implies we should ALLOW CPU version if it's installed.
                         # The performance warning is handled in MainWindow.
                         # So we should just accept it.
                         return True, "检测到 Torch CPU 版本 (Torch CPU detected)"
            except subprocess.CalledProcessError as e:
                # If import fails, it returns non-zero exit code
                return False, f"Torch 验证失败 (Torch verification failed): {e.output if e.output else str(e)}"
            except Exception as e:
                return False, f"Torch 验证出错 (Torch check error): {str(e)}"

            return True, "环境就绪 (Environment ready)"
        except subprocess.CalledProcessError:
            # If check fails, it means deps are missing.
            return False, "依赖缺失 (Dependencies missing)"
        except Exception as e:
            return False, str(e)

    def run(self):
        # Ensure we don't block the thread initialization
        if self.mode == "check":
            valid, msg = self.check_env()
            self.finished.emit(valid, msg)
        elif self.mode == "install":
            self.install_env()
            # After install, verify
            try:
                (self.target_dir / "env_verified.marker").touch()
            except:
                pass

    def download_python(self):
        self.progress.emit("正在下载 Python 运行时 (Downloading Python runtime)...", 5)
        import tarfile
        
        try:
            # Download
            temp_tar = self.target_dir.parent / "python_runtime.tar.gz"
            
            # Simple reporthook for progress
            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent = readsofar * 100 / totalsize
                    self.progress.emit(f"下载 Python 中: {int(percent)}%", 5 + int(percent * 0.2))
            
            success = False
            for url in self.python_urls:
                try:
                    urllib.request.urlretrieve(url, temp_tar, reporthook)
                    success = True
                    break
                except Exception:
                    continue
            
            if not success:
                raise Exception("无法下载 Python 运行时 (Failed to download Python runtime)")
            
            # Extract
            self.progress.emit("正在解压 Python (Extracting)...", 25)
            with tarfile.open(temp_tar, "r:gz") as tar:
                tar.extractall(path=self.target_dir)
            
            # Cleanup
            os.remove(temp_tar)
            
            # Standalone structure: python.exe is in python/ directory usually or root depending on build
            # The URL used extracts to a 'python' folder. We need to move contents up if needed.
            extracted_root = self.target_dir / "python"
            if extracted_root.exists():
                for item in os.listdir(extracted_root):
                    shutil.move(str(extracted_root / item), str(self.target_dir))
                os.rmdir(extracted_root)
                
            # Update python path
            self.python_exe = self.target_dir / "python.exe"
            
            # Enable pip
            # Get get-pip.py if needed, or ensure ensurepip works
            # Standalone builds often need get-pip
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            get_pip_path = self.target_dir / "get-pip.py"
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run([str(self.python_exe), str(get_pip_path)], check=True, startupinfo=startupinfo)
            
            return True
        except Exception as e:
            self.progress.emit(f"下载失败: {str(e)}", 0)
            return False

    def install_env(self):
        try:
            # Log Python version
            import platform
            self.progress.emit(f"Python Version: {platform.python_version()} ({platform.architecture()[0]})", 5)
            
            # 1. Create env if not exists
            # First, check if existing env is invalid (Must be 3.10 ~ 3.12)
            if (self.target_dir / "Scripts" / "python.exe").exists():
                try:
                    check_ver = subprocess.check_output(
                        [str(self.target_dir / "Scripts" / "python.exe"), "--version"], 
                        text=True, stderr=subprocess.STDOUT
                    )
                    # Parse version string "Python 3.x.y"
                    import re
                    ver_match = re.search(r"Python (\d+\.\d+)", check_ver)
                    if ver_match:
                        major, minor = map(int, ver_match.group(1).split('.'))
                        if not (3, 10) <= (major, minor) <= (3, 12):
                            self.progress.emit(f"检测到 Python 版本 {major}.{minor} 不在 3.10-3.12 范围内，正在清理环境以重新安装...", 6)
                            import shutil
                            shutil.rmtree(self.target_dir, ignore_errors=True)
                            self.python_exe = self.target_dir / "python.exe"
                except Exception as e:
                    print(f"Version check failed: {e}")

            if not self.python_exe.exists() and not (self.target_dir / "Scripts" / "python.exe").exists():
                self.target_dir.mkdir(parents=True, exist_ok=True)
                
                # Force download standalone python
                # Skip system python check
                created = False
                sys_ver_valid = False
                
                # If system venv failed or skipped, download standalone (3.10)
                if not created:
                    if not self.download_python():
                        self.finished.emit(False, "无法安装 Python 环境，需要网络连接。")
                        return

            # Determine correct python path again
            if (self.target_dir / "python.exe").exists():
                self.python_exe = self.target_dir / "python.exe"
            elif (self.target_dir / "Scripts" / "python.exe").exists():
                self.python_exe = self.target_dir / "Scripts" / "python.exe"
            
            # 2. Explicitly install Torch FIRST (to ensure correct version/mirror)
            # This avoids pip installing a generic CPU version from requirements.txt first
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            torch_success = False
            
            # CPU Mode handling
            if self.cpu_mode:
                self.progress.emit("正在安装 PyTorch (CPU版)...", 15)
                
                # Uninstall current torch first
                subprocess.run(
                    [str(self.python_exe), "-m", "pip", "uninstall", "-y", "torch", "torchvision", "torchaudio"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    startupinfo=startupinfo
                )
                
                # Determine index URL for CPU
                index_url = "https://download.pytorch.org/whl/cpu"
                if "aliyun.com" in self.mirror:
                    index_url = "https://mirrors.aliyun.com/pytorch-wheels/cpu/"

                install_args = ["torch", "torchvision", "torchaudio", "--no-warn-script-location"]
                install_args.extend(["--index-url", index_url])
                install_args.append("--no-cache-dir")
                
                cpu_cmd = [str(self.python_exe), "-m", "pip", "install"] + install_args
                
                self.progress.emit(f"执行命令: {' '.join(cpu_cmd)}", 20)
                
                cpu_process = subprocess.Popen(
                    cpu_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    startupinfo=startupinfo
                )
                
                while True:
                    line = cpu_process.stdout.readline()
                    if not line and cpu_process.poll() is not None:
                        break
                    if line:
                        clean_line = line.strip()
                        if clean_line:
                            self.progress.emit(f"安装 Torch CPU: {clean_line[:150]}...", 25)
                            
                if cpu_process.returncode == 0:
                    torch_success = True
                else:
                    self.finished.emit(False, "Torch CPU 安装失败")
                    return

            else:
                # CUDA Mode (Default)
                self.progress.emit("正在安装 PyTorch (CUDA版) (这可能需要很长时间，请耐心等待)...", 15)
                
                # Uninstall current torch first
                subprocess.run(
                    [str(self.python_exe), "-m", "pip", "uninstall", "-y", "torch", "torchvision", "torchaudio"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    startupinfo=startupinfo
                )
                
                # 2a. Pre-install Torch dependencies from standard PyPI
                # This ensures we have dependencies met so we can install torch with --no-deps from CUDA mirror
                # to strictly enforce the wheel source.
                self.progress.emit("正在预安装 Torch 依赖...", 16)
                
                torch_deps = [
                    "numpy", "typing-extensions", "sympy", "networkx", "jinja2", 
                    "fsspec", "filelock", "pillow", "markupsafe", "mpmath", "setuptools"
                ]
                
                deps_cmd = [
                    str(self.python_exe), "-m", "pip", "install"
                ] + torch_deps + ["-i", self.mirror, "--no-warn-script-location"]
                
                self.progress.emit(f"执行命令: {' '.join(deps_cmd)}", 17)
                
                deps_process = subprocess.Popen(
                    deps_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    startupinfo=startupinfo
                )
                
                while True:
                    line = deps_process.stdout.readline()
                    if not line and deps_process.poll() is not None:
                        break
                    if line:
                        clean_line = line.strip()
                        if clean_line:
                            self.progress.emit(f"安装依赖: {clean_line[:150]}...", 18)
                
                # 2b. Install Torch/Vision/Audio from CUDA mirror with --no-deps
                install_args = ["torch", "torchvision", "torchaudio", "--no-warn-script-location"]
                
                # Use official CUDA index for all mirrors (as user requested)
                # This ensures we get the official cu130 (or similar) build
                install_args.extend(["--index-url", "https://download.pytorch.org/whl/cu124"])
                install_args.append("--no-cache-dir")
                install_args.append("--default-timeout=1000")
                
                # If using custom mirror (like Aliyun) for PyPI deps, we still use official for torch
                # but we need to ensure pip doesn't try to find torch in the custom mirror first if it's set as global
                # However, here we are passing --index-url explicitly, which overrides global/user config for this command.

                cuda_cmd = [str(self.python_exe), "-m", "pip", "install"] + install_args
                
                # Log command
                self.progress.emit(f"执行命令: {' '.join(cuda_cmd)}", 20)
                
                cuda_process = subprocess.Popen(
                    cuda_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    startupinfo=startupinfo
                )
                
                while True:
                    line = cuda_process.stdout.readline()
                    if not line and cuda_process.poll() is not None:
                        break
                    if line:
                        clean_line = line.strip()
                        if clean_line:
                            self.progress.emit(f"安装 Torch CUDA: {clean_line[:150]}...", 25)

                if cuda_process.returncode == 0:
                    torch_success = True
                else:
                    self.finished.emit(False, "Torch CUDA 安装失败")
                    return

            # 3. Install other dependencies
            if torch_success:
                self.progress.emit("正在安装其他依赖 (这可能需要一段时间)...", 60)
                
                req_file = ROOT_PATH / "requirements.txt"
                if not req_file.exists():
                    req_file = ROOT_PATH.parent / "requirements.txt"
                    
                if not req_file.exists():
                    self.finished.emit(False, f"requirements.txt 未找到")
                    return

                # Create a temp requirements file excluding torch packages
                # This prevents pip from overwriting our carefully installed GPU torch with a CPU one from the mirror
                temp_req_file = self.target_dir / "temp_requirements.txt"
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    filtered_lines = []
                    for line in lines:
                        # Exclude torch related packages
                        pkg_name = line.strip().split('==')[0].split('>=')[0].split('<')[0].strip().lower()
                        if pkg_name not in ['torch', 'torchvision', 'torchaudio']:
                            filtered_lines.append(line)
                            
                    with open(temp_req_file, 'w', encoding='utf-8') as f:
                        f.writelines(filtered_lines)
                        
                    cmd = [
                        str(self.python_exe), "-m", "pip", "install", 
                        "-r", str(temp_req_file),
                        "-i", self.mirror,
                        "--no-warn-script-location"
                    ]
                    
                    self.progress.emit(f"执行命令: {' '.join(cmd)}", 65)
                    
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        startupinfo=startupinfo
                    )
                    
                    while True:
                        line = process.stdout.readline()
                        if not line and process.poll() is not None:
                            break
                        if line:
                            clean_line = line.strip()
                            if clean_line:
                                self.progress.emit(f"正在安装: {clean_line[:150]}...", 70)
                    
                    if process.returncode == 0:
                        self.progress.emit("安装完成!", 100)
                        self.finished.emit(True, "安装成功")
                    else:
                        self.finished.emit(False, "依赖安装失败")
                        
                except Exception as e:
                    self.finished.emit(False, f"处理依赖文件失败: {str(e)}")
                finally:
                    if temp_req_file.exists():
                        try:
                            os.remove(temp_req_file)
                        except:
                            pass

        except Exception as e:
            self.finished.emit(False, str(e))
