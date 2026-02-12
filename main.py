import os
import sys
import ctypes

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTranslator, QLocale
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from qfluentwidgets import setThemeColor
from app.view.main_window import MainWindow
from app.common.config import cfg, Language
from app.common.resource import get_resource_path

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Cyrene.QwenTTS.GUI.1.0")
        except Exception:
            pass

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # Install Translator
    locale = cfg.get(cfg.language).value
    translator = QTranslator()
    
    # Debug print
    print(f"Loading language: {locale.name()}")
    
    # Try multiple paths for the translator
    search_paths = [
        get_resource_path(f"app/resource/i18n/{locale.name()}.qm"),
        os.path.join(os.path.dirname(sys.executable), "app/resource/i18n", f"{locale.name()}.qm"),
        os.path.join(".", "app/resource/i18n", f"{locale.name()}.qm")
    ]
    
    loaded = False
    for path in search_paths:
        if os.path.exists(path):
            if translator.load(path):
                app.installTranslator(translator)
                print(f"Successfully loaded translator from: {path}")
                loaded = True
                break
    
    if not loaded:
        print(f"Failed to load translator for {locale.name()}")
        # Fallback to standard Qt loading
        if translator.load(locale, "app/resource/i18n", ".qm", get_resource_path(".")):
             app.installTranslator(translator)
             print("Loaded translator using fallback method")

    # Set Window Icon
    app.setWindowIcon(QIcon(get_resource_path("app/resource/images/Cyrene.ico")))

    # Set Theme Color
    setThemeColor('#ffb7c6')

    # Load Global Font
    font_path = get_resource_path("app/resource/font/HarmonyOS_Sans_SC_Medium.ttf")
    if os.path.exists(font_path):
        fontId = QFontDatabase.addApplicationFont(font_path)
        if fontId != -1:
            fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
            font = QFont(fontName)
            QApplication.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
