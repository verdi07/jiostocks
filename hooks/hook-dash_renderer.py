# hooks/hook-dash_core_components.py

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('dash_renderer')
