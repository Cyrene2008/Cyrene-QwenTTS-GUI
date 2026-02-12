<div align="center">

<image src="app/resource/images/Cyrene.png" width="128" height="128" />

# Cyrene QwenTTS Cyrene GUI

**语言选择** [ [English](README.md) | **简体中文** ]

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

请前往 [Releases](https://github.com/CyreneProject/QwenTTS-GUI/releases) 下载最新版本。

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

本项目采用 **GPLv3 许可证** 并附带额外声明。详情请参阅 [LICENSE](LICENSE) 文件。

本项目基于 **QFluentWidgets** Python 组件库构建。
- 源代码遵循 GNU General Public License v3.0 (GPLv3) 进行非商业用途发布。
- 任何衍生作品也必须在 GPLv3 下发布。

**UI 设计声明**
1. 本项目的用户界面设计（包括但不限于布局、功能模块排列、交互逻辑和综合样式）由 **Cyrene2008 (StarCyrene)** 设计。
   - 该设计的版权归作者所有，**不** 包含在 GPLv3 许可证范围内。
   - 未经授权，任何个人或组织不得复制、再现、改编或以其他方式使用上述 UI 设计。
2. 本项目中使用的第三方素材均遵循非商业环境下的合理使用原则。

## 开发者

由 [Cyrene2008](https://github.com/Cyrene2008) 开发。
