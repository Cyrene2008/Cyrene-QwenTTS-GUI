"""配置管理"""

import os
import sys
import logging
from pathlib import Path

LOGGER_NAME = os.getenv("QWEN_TTS_GUI_LOGGER_NAME", "Qwen TTS Cyrene GUI")
"""日志器名字"""

LOGGER_LEVEL = int(os.getenv("QWEN_TTS_GUI_LOGGER_LEVEL", str(logging.INFO)))
"""日志等级"""

LOGGER_COLOR = os.getenv("QWEN_TTS_GUI_LOGGER_COLOR") not in ["0", "False", "false", "None", "none", "null"]
"""日志颜色"""

# Determine ROOT_PATH
# Priority:
# 1. Environment Variable (Used by backend process to sync with frontend)
# 2. Frozen Executable Directory (Frontend/UI)
# 3. Source File Relative Path (Dev mode)

env_root = os.getenv("QWEN_TTS_ROOT_PATH")
if env_root and os.path.isdir(env_root):
    ROOT_PATH = Path(env_root)
elif getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    ROOT_PATH = Path(sys.executable).parent
else:
    # Running in a normal Python environment
    ROOT_PATH = Path(__file__).parent.parent.parent
"""Qwen TTS GUI 根目录"""

OUTPUT_PATH = ROOT_PATH / "outputs"
"""输出文件路径"""

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = ROOT_PATH / "app" / "config" / "config.json"
"""配置文件路径"""

MODEL_CACHE_DIR = ROOT_PATH / "config" / "models"
"""模型下载缓存目录"""

MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

QWEN_TTS_BASE_MODEL_LIST = [
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
]
"""Qwen TTS 声音克隆模型"""

QWEN_TTS_CUSTOM_VOICE_MODEL_LIST = [
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
]
"""Qwen TTS 声音生成模型"""

QWEN_TTS_VOICE_DESIGN_MODEL_LIST = [
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
]
"""Qwen TTS 声音设计模型"""

ATTN_IMPL_LIST = [
    "eager",
    "sdpa",
    "flash_attention_2",
]
"""注意力加速方案"""
