<div align="center">

<image src="https://gh-proxy.org/https://raw.githubusercontent.com/Cyrene2008/Cyrene-QwenTTS-GUI/refs/heads/main/app/resource/images/Cyrene.ico" width="128" height="128" />

# Cyrene QwenTTS GUI

[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=for-the-badge&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/Cyrene2008/Cyrene-QwenTTS-GUI)

**语言选择** [ [English](README.md) | **✔简体中文** ]

基于 PySide6 和 FluentUI 构建的 Qwen-TTS 现代化图形界面。

[前往下载](https://github.com/Cyrene2008/Cyrene-QwenTTS-GUI/releases)|[使用向导](Guide.md)

</div>

## 功能特性

- **语音生成**：使用 Qwen-TTS 模型将文本转换为语音。
- **声音克隆**：通过参考音频复刻（克隆）声音。
- **声音设计**：根据文本描述（提示词）设计并生成特定的声音。
- **音频浏览**：管理和播放生成的音频文件。
- **现代化 UI**：采用 Fluent Design 设计语言，支持主题切换和流畅动画。

## 环境要求

本程序提供两种 Qwen-TTS 模型环境配置方案：
- **GPU**：适用于支持 CUDA 的设备（推荐）。
- **CPU**：适用于无 CUDA 设备或仅使用 CPU 的情况。

## 安装指南

请前往 [Releases](https://github.com/CyreneProject/Cyrene-QwenTTS-GUI/releases) 下载最新版本。
随后将 [requirements.txt](https://gh-proxy.org/https://raw.githubusercontent.com/Cyrene2008/Cyrene-QwenTTS-GUI/refs/heads/main/requirements.txt) 跟程序放到同一个目录内。

### 编译

要求：Python 3.10-3.12

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行程序：
   ```bash
   python package.py
   ```

## 使用说明

- **语音生成**：选择模型和说话人，输入文本并生成语音。
- **声音设计**：描述想要的声音特征（例如：“年轻女性声音，开心的语气”），然后生成语音。
- **声音克隆**：上传参考音频并输入文本，克隆该声音。
- **音频浏览**：查看和播放已生成的音频文件。
- **设置**：更改语言、字体缩放。

## 许可证

本项目采用分层授权架构，核心规则见根目录 [LICENSE](LICENSE) 文件：

- 核心代码（app/core/等）：遵循 GPLv3 开源协议；
- UI 设计方案：保留所有权利（非商用仅可随代码展示）；
- 第三方素材：仅非商业合理使用，版权归原权利人所有。

完整 GPLv3 协议文本见：[app/core/LICENSE](app/core/LICENSE)

## 开发者

由 [Cyrene2008](https://github.com/Cyrene2008) 开发。
