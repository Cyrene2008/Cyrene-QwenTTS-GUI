import sys
import types
import pkgutil
import os
import importlib.util

if not hasattr(pkgutil, 'ImpImporter'):
    class DummyImpImporter:
        def __init__(self, *args, **kwargs): pass
    pkgutil.ImpImporter = DummyImpImporter

try:
    import packaging.version
    original_version_init = packaging.version.Version.__init__
    def patched_version_init(self, version):
        try:
            original_version_init(self, str(version))
        except Exception:
            original_version_init(self, "0.0.0")
    packaging.version.Version.__init__ = patched_version_init
    
    if hasattr(packaging.version, 'parse'):
        original_parse = packaging.version.parse
        def patched_parse(version):
            try:
                return original_parse(str(version))
            except Exception:
                return original_parse("0.0.0")
        packaging.version.parse = patched_parse
except Exception:
    pass

def create_dummy(name, attrs=None):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__version__ = '0.0.0'
        if attrs:
            for k, v in attrs.items():
                setattr(m, k, v)
        sys.modules[name] = m
        return m
    return sys.modules[name]

class DummyDevice:
    def __init__(self, type, index=None):
        self.type = type
        self.index = index
    def __str__(self):
        return f"{self.type}:{self.index}" if self.index is not None else self.type

torch_attrs = {
    'cuda': create_dummy('torch.cuda', {
        'is_available': lambda: False,
        'current_device': lambda: 0,
        'empty_cache': lambda: None,
        'ipc_collect': lambda: None,
        'memory_stats': lambda *a: {},
        'mem_get_info': lambda *a: (0, 0),
        'get_device_name': lambda *a: 'Mock GPU',
        'OutOfMemoryError': MemoryError,
    }),
    'backends': create_dummy('torch.backends', {
        'mps': create_dummy('torch.backends.mps', {'is_available': lambda: False})
    }),
    'float16': 'float16',
    'float32': 'float32',
    'bfloat16': 'bfloat16',
    'float8_e4m3fn': 'float8_e4m3fn',
    'float8_e5m2': 'float8_e5m2',
    'device': DummyDevice,
}
create_dummy('torch', torch_attrs)
create_dummy('torchaudio')
create_dummy('torchvision')
create_dummy('modelscope', {'hub': create_dummy('modelscope.hub', {'api': create_dummy('modelscope.hub.api', {'HubApi': type('HubApi', (), {'login': lambda *a, **k: None})})})})
create_dummy('transformers')
create_dummy('accelerate')
create_dummy('gradio')
create_dummy('qwen_tts')

try:
    import pkg_resources.py2_warn
except ImportError:
    sys.modules['pkg_resources.py2_warn'] = types.ModuleType('pkg_resources.py2_warn')

modules_to_inject = [
    ('six', 'six'),
    ('six.moves', 'six.moves'),
    ('appdirs', 'appdirs'),
    ('packaging', 'packaging'),
    ('packaging.version', 'packaging.version'),
    ('packaging.specifiers', 'packaging.specifiers'),
    ('packaging.requirements', 'packaging.requirements'),
    ('packaging.markers', 'packaging.markers'),
    ('packaging.utils', 'packaging.utils'),
]

for name, module_name in modules_to_inject:
    try:
        if module_name == 'six.moves':
             import six
             if hasattr(six, 'moves'):
                 actual_mod = six.moves
             else:
                 continue
        else:
            actual_mod = __import__(module_name, fromlist=['*'])

        extern_name = f'pkg_resources.extern.{name}'
        sys.modules[extern_name] = actual_mod

        if 'pkg_resources.extern' in sys.modules:
            setattr(sys.modules['pkg_resources.extern'], name, actual_mod)
    except Exception:
        pass

try:
    import psutil._psutil_windows
except ImportError:
    try:
        import psutil
        if hasattr(sys, '_MEIPASS'):
            pyd_path = os.path.join(sys._MEIPASS, 'psutil', '_psutil_windows.cp38-win_amd64.pyd')

            if not os.path.exists(pyd_path):
                 psutil_dir = os.path.join(sys._MEIPASS, 'psutil')
                 if os.path.exists(psutil_dir):
                     for f in os.listdir(psutil_dir):
                         if f.startswith('_psutil_windows') and f.endswith('.pyd'):
                             pyd_path = os.path.join(psutil_dir, f)
                             break

            if not os.path.exists(pyd_path):
                 if os.path.exists(sys._MEIPASS):
                     for f in os.listdir(sys._MEIPASS):
                         if f.startswith('_psutil_windows') and f.endswith('.pyd'):
                             pyd_path = os.path.join(sys._MEIPASS, f)
                             break
            
            if os.path.exists(pyd_path):
                spec = importlib.util.spec_from_file_location("psutil._psutil_windows", pyd_path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    sys.modules["psutil._psutil_windows"] = mod
                    spec.loader.exec_module(mod)
                    setattr(psutil, '_psutil_windows', mod)
    except Exception:
        pass
        
    except (ImportError, Exception):
        pass
