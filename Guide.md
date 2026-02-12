# QwenTTS-Cyrene-GUI v1.0.0 - Initial Release / 初次发布
🎉 Welcome to the first release of QwenTTS-Cyrene-GUI! This is a modern, user-friendly GUI client for the powerful Qwen-TTS model, built with PySide6 and FluentUI. It allows you to run text-to-speech, voice cloning, and voice design tasks locally on your Windows machine with ease.

🎉 欢迎使用 QwenTTS-Cyrene-GUI 的首个版本！ 这是一个基于 PySide6 和 FluentUI 构建的现代化 Qwen3-TTS 桌面客户端。它让您可以轻松地在 Windows 本地运行文本转语音、声音克隆和声音设计任务，拥有精美的界面和便捷的操作体验。

<img width="2340" height="1019" alt="ScreenShot_2026-02-12_182542_491" src="https://github.com/user-attachments/assets/1781513f-9281-422e-9e37-e23723108fe6" />

## ✨ Key Features / 主要特性
- 🎨 Modern Fluent Design / 现代化 Fluent 设计
  
  - Beautiful and intuitive UI based on PySide6-Fluent-Widgets .
  - Bilingual Support : Fully supports both English and Simplified Chinese.
  - 基于 PySide6-Fluent-Widgets 构建的精美、直观的用户界面。
  - 双语支持 ：支持英文和简体中文。
- 🛠️ One-Click Environment Setup / 一键环境配置
  
  - Auto-Dependency Management : Automatically detects missing dependencies (PyTorch, CUDA) and installs them on the first run.
  - Smart Mirror Selection : Uses official sources for CUDA PyTorch to ensure stability, and Aliyun mirrors for PyPI to speed up downloads in China.
  - 自动依赖管理 ：首次运行自动检测并安装缺失的依赖（如 PyTorch, CUDA），无需手动配置 Python 环境。
  - 智能镜像选择 ：CUDA PyTorch 使用官方源以确保稳定性，PyPI 依赖使用阿里源加速国内下载。
- 🚀 Powerful TTS Capabilities / 强大的语音合成能力
  
  - Voice Generation : High-quality text-to-speech with Qwen-TTS models.
  - Voice Cloning : Clone any voice using a short reference audio clip.
  - Voice Design : Create custom voices using natural language prompts.
  - 语音生成 ：基于 Qwen-TTS 模型的高质量文本转语音。
  - 声音克隆 ：仅需一段简短的参考音频即可克隆任意声音。
  - 声音设计 ：通过自然语言提示词创造独一无二的声音。
<img width="2340" height="1019" alt="ScreenShot_2026-02-12_182551_249" src="https://github.com/user-attachments/assets/d1567049-41d7-4833-abd5-3acf72acabfc" />
<img width="2340" height="1019" alt="ScreenShot_2026-02-12_182617_628" src="https://github.com/user-attachments/assets/eea2df9c-1cd2-4fdc-90e8-9b81208c1f75" />


- 📂 Portable & Local / 便携与本地化
  
  - Portable Config : All configurations and model weights are saved in the application directory ( config/ and config/models/ ). No pollution to your C: drive.
  - Local Outputs : Generated audio files are automatically saved to the outputs/ folder with timestamped filenames.
  - 便携配置 ：所有配置文件和模型权重均保存在程序目录下（ config/ 和 config/models/ ），不占用系统盘空间。
  - 本地输出 ：生成的音频文件自动保存至 outputs/ 文件夹，并以时间命名，方便管理。
## 🔧 Improvements & Fixes / 改进与修复
- CUDA Detection : Fixed an issue where the backend process could not detect CUDA GPUs due to missing DLL paths.
  - CUDA 检测修复 ：修复了后端进程因缺失 DLL 路径而无法检测到 GPU 的问题。
- Audio Browser : Optimized the audio browser interface with auto-refresh, reverse chronological sorting (newest first), and direct playback.
  - 音频浏览优化 ：优化了音频浏览界面，支持自动刷新、按时间倒序排列（最新在最上）以及直接播放。
- Package Size : Optimized the executable size (~120MB) by excluding unnecessary libraries while maintaining full functionality.
  - 体积优化 ：优化了打包体积（约 120MB），剔除了不必要的库文件。
## 📥 Installation / 安装说明
We provide two download options based on your network conditions:
我们根据您的网络情况提供两种下载选项：

### Option 1: Standard Package (Recommended for fast internet) / 选项一：标准版（网速快推荐）
- File : QwenTTS-Cyrene-GUI.exe
- Description : Small size (~120MB). It will download the AI environment (PyTorch, etc.) automatically on the first run.
- 描述 ：体积小（约 120MB）。首次运行时会自动下载 AI 运行环境（PyTorch 等）。

<img width="2340" height="1019" alt="ScreenShot_2026-02-12_183221_615" src="https://github.com/user-attachments/assets/5a394ad2-c91a-4a44-84fc-4c31c76a1531" />

### Option 2: Full Package with Environment (Out-of-the-box) / 选项二：整合包（开箱即用推荐）
- Files : Qwen-TTS-Cyrene-GUIv0.1.0-withENV.zip & Qwen-TTS-Cyrene-GUIv0.1.0-withENV.z01
- Description : Large size. Includes the full AI environment.Download .zip and .z01 file, extract and run, no internet required for environment setup, what you should do is download model in QwenTTS-Cyrene-GUI.
- 描述 ：体积较大。 已集成完整 AI 运行环境。 下载.zip和.z01文件，解压即用，无需联网配置环境，仅需要下载需要的模型(modelscope国内速度很快，不用担心！)。
### 🚀 How to Run / 运行步骤
1. Download one of the files from Assets below.
   - 下载下方 Assets 中的文件。
2. Place it in a folder (e.g., D:\QwenTTS\ ). If using the Full Package, extract it first.
   - 将其放置在一个文件夹中（例如 D:\QwenTTS\ ）。如果是整合包，请先解压。
3. Run QwenTTS-Cyrene-GUI.exe .
   - 运行 QwenTTS-Cyrene-GUI.exe 。
   - Note for Standard Package: Follow the wizard to download dependencies.
   - 标准版注意：请跟随向导下载依赖。
4. Important : After the app starts, you will see a splash video. Please CLICK anywhere on the screen to enter the main interface. (It is waiting for your interaction, not loading!)
   - 重要提示 ：程序启动会播放开场视频， 请点击屏幕任意位置以进入主界面 。（程序正在等待您的点击，并非卡在加载中！）
### ⚠️ Troubleshooting / 故障排除
- Installation Interrupted? / 安装被中断？
  - If you accidentally close the program during the environment installation (Wizard), the app might fail to start next time.
  - Fix : Simply delete the QwenTTS-Cyrene-GUI-ENV folder in the application directory and restart the app.
  - 安装中断了怎么办？
  - 如果您在环境安装向导运行期间意外关闭了程序，下次启动时可能会无法运行。
  - 解决方法 ：请手动删除程序目录下的 QwenTTS-Cyrene-GUI-ENV 文件夹，然后重启程序。
<img width="2340" height="1019" alt="ScreenShot_2026-02-12_182641_683" src="https://github.com/user-attachments/assets/24078e88-0b43-4fcc-8edd-fdb50635c202" />
