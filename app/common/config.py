# coding:utf-8
import sys
import os
from enum import Enum

from PySide6.QtCore import Qt, QLocale
from qfluentwidgets import OptionsConfigItem, BoolValidator, OptionsValidator, Theme, ConfigSerializer, qconfig
from .resource import get_resource_path

class Language(Enum):
    """ Language enumeration """
    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    ENGLISH = QLocale(QLocale.English, QLocale.UnitedStates)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class ThemeSerializer(ConfigSerializer):
    """ Theme serializer """

    def serialize(self, theme):
        return theme.value

    def deserialize(self, value: str):
        return Theme(value)


class Config(qconfig.__class__):
    """ Config of application """

    # language
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.CHINESE_SIMPLIFIED, OptionsValidator(Language), LanguageSerializer(), restart=True)

cfg = Config()

# Define persistent config path
if hasattr(sys, 'frozen'):
    # Use absolute path to ensure it's in the same folder as the EXE
    exe_dir = os.path.abspath(os.path.dirname(sys.executable))
    CONFIG_PATH = os.path.join(exe_dir, 'config', 'config.json')
else:
    CONFIG_PATH = os.path.join(os.path.abspath("."), 'app', 'config', 'config.json')

# Ensure directory exists
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

# If config doesn't exist in persistent location but exists in resource, copy it
RESOURCE_CONFIG = get_resource_path('app/config/config.json')
if not os.path.exists(CONFIG_PATH) and os.path.exists(RESOURCE_CONFIG):
    import shutil
    try:
        shutil.copy(RESOURCE_CONFIG, CONFIG_PATH)
    except:
        pass

qconfig.load(CONFIG_PATH, cfg)
