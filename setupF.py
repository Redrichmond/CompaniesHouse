import sys

from cx_Freeze import setup, Executable

path_drivers = ("C:\Python34\Lib\site-packages\PyQt5\plugins\sqldrivers\qsqlmysql.dll", "sqldrivers\qsqlmysql.dll")

includes = ["requests", "atexit", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.QtSql"]
includefiles = [path_drivers]

excludes = [
    '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
    'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
    'Tkconstants', 'Tkinter', 'gui'
]
packages = ["os"]
path = []

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "includes": includes,
    "include_files": includefiles,
    "excludes": excludes,
    "packages": packages,
    "path": path
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
exe = None
if sys.platform == "win32":
    exe = Executable(
        script="main.py",
        initScript=None,
        base=None,
        targetName="zeus.exe",
        compress=True,
        copyDependentFiles=True,
        appendScriptToExe=False,
        appendScriptToLibrary=False,
        icon=None
    )

setup(
    name="telll",
    version="0.1",
    author='me',
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
