from cx_Freeze import setup, Executable
import requests.certs
build_exe_options = \
    {"include_files":[
                        (requests.certs.where(),'cacert.pem'),
                        ('config.ini'),
                        ('input/'),
                        ('output/')
                        ]}

target = Executable(
    script="main.py",
    base="Win32GUI",
    compress=True,
    copyDependentFiles=True,
    appendScriptToExe=True,
    appendScriptToLibrary=False,
    icon="icon.ico"
    )

setup(
    name = "CH Scrappint Tool",
    version = "1.1",
    description = "Companies Hose UK Scrapping Tool",
    author = "Firesoft C.A",
    options = {"build_exe": build_exe_options},
    executables = [target])