<div align="center">

<image src="app/resource/images/Cyrene.ico" width="128" height="128" />

# Cyrene QwenTTS GUI

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
