<div align="center">

<image src="app/resource/images/Cyrene.png" width="128" height="128" />

# Cyrene QwenTTS Cyrene GUI

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

Download the latest version from [Releases](https://github.com/Cyrene2008/QwenTTS-GUI/releases).

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

This project is licensed under the **GPLv3 License** with extra permissions. See the [LICENSE](LICENSE) file for details.

Built on the **QFluentWidgets** Python component library.
- The source code is released under the GNU General Public License v3.0 (GPLv3) for non-commercial use.
- Any derivative work must also be released under GPLv3.

**UI Design Copyright Notice**
1. The user-interface design (layout, interaction logic, styling) is designed by **Cyrene2008 (StarCyrene)**.
   - The copyright of this design is retained by the author and is **not** covered by the GPLv3 license.
   - No individual or organization may copy, reproduce, adapt, or otherwise use the UI design without prior authorization.
2. Third-party materials are used under fair-use principles for non-commercial contexts.

## Credits

Developed by [Cyrene2008](https://github.com/Cyrene2008).
