import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Stock visualizer",
        version = "0.1",
        description = "Web app to browse the stock market movements",
        options = {"build_exe": build_exe_options},
        executables = [Executable("stock_visual.py", base=base)])
