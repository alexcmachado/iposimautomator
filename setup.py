"""Setup for Iposim Automator."""

import sys
from cx_Freeze import setup, Executable  # type: ignore
from src.constants import BUILD_ICON_PATH, NAME, VERSION, DESCRIPTION, AUTHOR  # type: ignore

sys.path.append("./src")

include_files = [
    "./src/drivers/geckodriver.exe",
    "./example/input.xlsx",
    "./example/results.xlsx",
    "./src/config.json",
    BUILD_ICON_PATH,
    "./src/images/example.png",
    "./src/images/inverter.png",
    "./README.html",
]
include_files_pairs = [(file_path, file_path) for file_path in include_files]

build_exe_options = {"include_files": include_files_pairs}

shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        NAME,  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]iposim.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        False,  # ShowCmd
        "TARGETDIR",  # WkDir
    )
]

# controls what appears on control panel
bdist_msi_options = {
    "install_icon": BUILD_ICON_PATH,
    "data": {"Shortcut": shortcut_table},
}

# disable terminal when executing .exe file
BASE = None
if sys.platform == "win32":
    BASE = "Win32GUI"

SHORTCUT_NAME = NAME
SHORTCUT_DIR = "DesktopFolder"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[
        Executable(
            "./src/iposim.py",
            base=BASE,
            shortcutName=SHORTCUT_NAME,
            shortcutDir=SHORTCUT_DIR,
            icon=BUILD_ICON_PATH,
        )
    ],  # icon controls what shows up on desktop
)
