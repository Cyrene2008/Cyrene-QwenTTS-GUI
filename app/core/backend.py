"""Qwen TTS Backend Client (Stub)"""

import os
import time
import requests
import subprocess
import signal
import sys
from pathlib import Path
from typing import Optional, List
from app.core.logger import get_logger
from app.core.config import LOGGER_LEVEL, LOGGER_COLOR, ROOT_PATH

logger = get_logger(level=LOGGER_LEVEL, color=LOGGER_COLOR)

class QwenTTSBackend:
    """Client for QwenTTS Server"""
    
    def __init__(self, port=7951):
        self.port = port
        self.base_url = f"http://127.0.0.1:{port}"
        self.server_process = None
        
        # Check if server is running, if not, start it
        if not self._is_server_running():
            self._start_server()

    def _is_server_running(self):
        try:
            requests.get(f"{self.base_url}/speakers", timeout=1)
            return True
        except:
            return False

    def _start_server(self):
        # Locate python exe
        # Priority:
        # 1. Check for 'use_system_python' marker
        # 2. Check for QwenTTS-Cyrene-GUI-ENV (Root or Scripts)
        
        cwd = ROOT_PATH
        env_dir = cwd / "QwenTTS-Cyrene-GUI-ENV"
        
        # Check for system python override
        use_system_python = False
        
        # If frozen (EXE), disable use_system_python because sys.executable is the EXE itself
        if getattr(sys, 'frozen', False):
             use_system_python = False
        else:
            marker_file = cwd / "use_system_python.marker"
            if marker_file.exists():
                use_system_python = True
            
        python_exe = None
            
        if use_system_python:
            python_exe = Path(sys.executable)
            logger.info(f"Using System Python: {python_exe}")
        else:
            # List of possible python locations
            possible_locations = [
                env_dir / "python.exe",            # Standalone root
                env_dir / "Scripts" / "python.exe", # Venv/Standard Windows
                env_dir / "bin" / "python",         # Unix
            ]
            
            # Check current dir first
            for p in possible_locations:
                if p.exists():
                    python_exe = p
                    break
            
            # If not found, try parent directory (in case we are in dist)
            if not python_exe:
                 env_dir_parent = cwd.parent / "QwenTTS-Cyrene-GUI-ENV"
                 possible_locations_parent = [
                    env_dir_parent / "python.exe",
                    env_dir_parent / "Scripts" / "python.exe",
                    env_dir_parent / "bin" / "python",
                 ]
                 for p in possible_locations_parent:
                     if p.exists():
                         env_dir = env_dir_parent
                         python_exe = p
                         break
    
            if not python_exe:
                logger.error("Environment not found, cannot start backend server.")
                raise Exception("环境未找到 (Environment not found)，无法启动后端服务。")

        from app.common.resource import get_resource_path
        server_script = Path(get_resource_path("app/service/server.py"))
        
        # If server script not found in temp resource, try cwd (for dev mode)
        if not server_script.exists():
            server_script = cwd / "app" / "service" / "server.py"

        if not server_script.exists():
             logger.error(f"Server script not found at {server_script}")
             raise Exception(f"服务脚本未找到 (Server script not found): {server_script}")

        cmd = [str(python_exe), str(server_script), str(self.port)]
        
        logger.info(f"Starting backend server: {' '.join(cmd)}")
        
        # Start detached process but redirect output to file for debugging
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # Open log file
        log_file = cwd / "backend_server.log"
        self.log_fp = open(log_file, "w", encoding="utf-8")
        
        # Prepare environment variables
        env = os.environ.copy()
        
        # Add python environment to PATH to ensure DLLs (CUDA, etc.) are found
        path_list = []
        
        # Add Library/bin (for CUDA DLLs in Conda/Standalone envs)
        lib_bin = env_dir / "Library" / "bin"
        if lib_bin.exists():
            path_list.append(str(lib_bin))
            
        # Add Scripts (for pip etc)
        scripts_dir = env_dir / "Scripts"
        if scripts_dir.exists():
            path_list.append(str(scripts_dir))
            
        # Add root (for python.exe)
        path_list.append(str(env_dir))
        
        # Add torch/lib for CUDA DLLs
        torch_lib = env_dir / "Lib" / "site-packages" / "torch" / "lib"
        if torch_lib.exists():
            path_list.append(str(torch_lib))
        
        # Prepend to PATH
        if "PATH" in env:
            env["PATH"] = os.pathsep.join(path_list + [env["PATH"]])
        else:
            env["PATH"] = os.pathsep.join(path_list)

        # Inject ROOT_PATH for backend process to know the real root (dist folder)
        # This is critical for config.py to locate output folder and config.json correctly
        # when running from temporary _MEIPASS source.
        env["QWEN_TTS_ROOT_PATH"] = str(cwd)
        
        # Set Model Download Path to config/models
        # This prevents models from being downloaded to C:\Users\xxx\.cache
        from app.core.config import MODEL_CACHE_DIR
        model_cache = str(MODEL_CACHE_DIR)
        
        # For ModelScope
        env["MODELSCOPE_CACHE"] = model_cache
        
        # For HuggingFace
        env["HF_HOME"] = model_cache
        env["HF_HUB_CACHE"] = model_cache
        
        # Debug log paths
        self.log_fp.write(f"QWEN_TTS_ROOT_PATH: {cwd}\n")
        self.log_fp.write(f"MODEL_CACHE_DIR: {model_cache}\n")

        # Add PYTHONPATH so the external python can find the app package in temp folder
        if getattr(sys, 'frozen', False):
            mei_pass = sys._MEIPASS
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = os.pathsep.join([mei_pass, env["PYTHONPATH"]])
            else:
                env["PYTHONPATH"] = mei_pass
            
            # Debug log environment in backend log
            self.log_fp.write(f"MEIPASS: {mei_pass}\n")
            self.log_fp.write(f"PYTHONPATH: {env.get('PYTHONPATH', '')}\n")
            self.log_fp.write(f"PATH: {env.get('PATH', '')}\n")
            self.log_fp.flush()

        self.server_process = subprocess.Popen(
            cmd,
            stdout=self.log_fp,
            stderr=self.log_fp,
            cwd=str(cwd), # Ensure we run from the correct root
            startupinfo=startupinfo,
            env=env, # Use modified environment
            encoding='utf-8', # Force subprocess to use utf-8 for pipes if text mode used (though stdout is file)
            errors='replace' 
        )
        
        # Wait for server to be ready
        for _ in range(40): # Wait up to 20 seconds
            if self._is_server_running():
                logger.info("Backend server connected.")
                return
            
            # Check if process died
            if self.server_process.poll() is not None:
                # Close log file to read it
                self.log_fp.close()
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        log_content = f.read()
                except UnicodeDecodeError:
                    try:
                        # Try GBK for Chinese Windows
                        with open(log_file, "r", encoding="gbk") as f:
                            log_content = f.read()
                    except:
                        # Fallback to ignore errors
                        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                            log_content = f.read()
                
                logger.error(f"Backend server exited unexpectedly. Return code: {self.server_process.returncode}")
                logger.error(f"Server Log:\n{log_content}")
                raise Exception(f"后端服务启动失败 (Backend failed start)。请检查 backend_server.log")
                
            time.sleep(0.5)
        
        # If we get here, it timed out
        if self.server_process:
            self.server_process.terminate()
            self.log_fp.close()
            logger.error("Backend server timed out.")
            
        logger.error("Failed to connect to backend server.")
        raise Exception("连接后端服务超时 (Connection Timeout)。请检查 backend_server.log")

    def shutdown(self):
        """关闭后端服务"""
        if self.server_process:
            logger.info("正在关闭后端服务...")
            try:
                # Try graceful shutdown via API
                try:
                    requests.post(f"{self.base_url}/shutdown", timeout=1)
                except:
                    pass
                
                self.server_process.terminate()
                self.server_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            except Exception as e:
                logger.error(f"关闭后端服务时出错: {e}")
            finally:
                self.server_process = None
                if hasattr(self, 'log_fp') and self.log_fp:
                    self.log_fp.close()
                logger.info("后端服务已关闭")

    def load_model(self, model_name: str):
        # Increase timeout for model loading as it might involve download
        # Set a very long timeout (e.g., 30 minutes) for downloading
        try:
            resp = requests.post(f"{self.base_url}/load_model", json={"model_name": model_name}, timeout=1800)
            if resp.status_code != 200:
                raise Exception(resp.json().get("detail", "Unknown error"))
        except requests.Timeout:
            raise Exception("加载模型超时 (Model load timed out)，可能是下载过慢。请查看 backend_server.log 了解进度。")

    def get_supported_speakers(self) -> List[str]:
        try:
            resp = requests.get(f"{self.base_url}/speakers", timeout=5)
            if resp.status_code == 200:
                return resp.json().get("speakers", [])
            return []
        except:
            return []

    def get_device_info(self) -> dict:
        try:
            resp = requests.get(f"{self.base_url}/device_info", timeout=5)
            if resp.status_code == 200:
                return resp.json()
            return {}
        except:
            return {}

    def generate_custom_voice(
        self,
        text: str,
        speaker: str,
        language: str | None = None,
        **kwargs
    ) -> Path:
        payload = {
            "text": text,
            "speaker": speaker,
            "language": language
        }
        resp = requests.post(f"{self.base_url}/generate", json=payload, timeout=300)
        if resp.status_code == 200:
            return Path(resp.json()["path"])
        else:
            raise Exception(resp.json().get("detail", "生成失败 (Generation failed)"))

    def generate_voice_design(
        self,
        text: str,
        instruct: str,
        language: str | None = None,
        **kwargs
    ) -> Path:
        payload = {
            "text": text,
            "instruct": instruct,
            "language": language
        }
        resp = requests.post(f"{self.base_url}/generate_design", json=payload, timeout=300)
        if resp.status_code == 200:
            return Path(resp.json()["path"])
        else:
            raise Exception(resp.json().get("detail", "声音设计生成失败 (Voice design generation failed)"))

    def generate_voice_clone(
        self,
        text: str,
        ref_audio: Path | str,
        ref_text: str | None = None,
        language: str | None = None,
        x_vector_only_mode: bool = False,
        **kwargs
    ) -> Path:
        payload = {
            "text": text,
            "ref_audio": str(ref_audio),
            "ref_text": ref_text,
            "language": language,
            "x_vector_only_mode": x_vector_only_mode
        }
        resp = requests.post(f"{self.base_url}/generate_clone", json=payload, timeout=300)
        if resp.status_code == 200:
            return Path(resp.json()["path"])
        else:
            raise Exception(resp.json().get("detail", "声音克隆生成失败 (Voice clone generation failed)"))
