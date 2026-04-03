<div align="center">

<image src="app/resource/images/Cyrene.ico" width="128" height="128" />

# Cyrene QwenTTS GUI

[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=for-the-badge&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/Cyrene2008/Cyrene-QwenTTS-GUI)

**Language** [ **✔English** | [简体中文](README_ZH_CN.md) ]

A modern GUI for Qwen-TTS, built with PySide6 and FluentUI.

[Download](https://github.com/Cyrene2008/Cyrene-QwenTTS-GUI/releases)|[Usage Guide](Guide.md)

</div>

## Features

- **Voice Generation**: Generate speech from text using Qwen-TTS models.
- **Voice Cloning**: Clone voices from reference audio.
- **Voice Design**: Create voices based on text descriptions (prompts).
- **Audio Browser**: Manage and play generated audio files.
- **Modern UI**: Fluent Design interface with theme support and animations.

## Requirements

The GUI provides two options for setting up the environment for Qwen-TTS models:
- **GPU**: For devices with CUDA support (Recommended).
- **CPU**: For devices without CUDA or if you prefer CPU execution.

## Installation

Download the latest version from [Releases](https://github.com/Cyrene2008/Cyrene-QwenTTS-GUI/releases).
Put [requirements.txt](https://gh-proxy.org/https://raw.githubusercontent.com/Cyrene2008/Cyrene-QwenTTS-GUI/refs/heads/main/requirements.txt) file in the same folder.

### Build from Source

Requirements: Python 3.10-3.12

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python package.py
   ```

## Usage

- **Generation**: Select model and speaker, enter text, and generate.
- **Design**: Describe the desired voice (e.g., "A young female voice, happy tone") and generate speech.
- **Clone**: Upload a reference audio file and enter text to clone the voice.
- **Browser**: View and play generated audio files.
- **Settings**: Change language, font scale, and theme.

## License

This project adopts a layered licensing architecture. Core rules are in the root [LICENSE](LICENSE) file:

- Core code (app/core/, etc.): Follows GPLv3 open source license;
- UI design scheme: All rights reserved (non-commercial use only with code display);
- Third-party materials: Non-commercial fair use only, copyright belongs to original rights holders.

Full GPLv3 license text: app/core/LICENSE

## Credits

Developed by [Cyrene2008](https://github.com/Cyrene2008).
