import subprocess
import sys
import importlib

def ensure(module):
    try:
        return importlib.import_module(module)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
        importlib.invalidate_caches()
        return importlib.import_module(module)
